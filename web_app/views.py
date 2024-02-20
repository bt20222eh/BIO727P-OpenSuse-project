from flask import Blueprint, render_template, request, jsonify, send_file, send_from_directory, url_for
from .models import SamplePopulation, ClusteringAnalysis, SNPData, SampleData, AdmixtureAnalysis  # Import your models
from .extensions import db
from .genetics import get_allele_frequencies_for_population, calculate_fst
from .utils import save_matrix_to_csv, generate_heatmap
from sqlalchemy import select
from sqlalchemy import or_
from sqlalchemy import func
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import json
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Create a Blueprint object
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/clustering')
def clustering():
    return render_template('clustering.html')

@bp.route('/admixture')
def admixture():
    # Assume data for admixture is pre-loaded or fetched from the database
    return render_template('admixture.html')

@bp.route('/data_retrieval')
def data_retrieval():
    return render_template('dataretrieval.html')

@bp.route('/get_populations')
def get_populations():
    populations = SamplePopulation.query.with_entities(SamplePopulation.Population).distinct().all()
    return jsonify([pop.Population for pop in populations])

@bp.route('/get_superpopulations')
def get_superpopulations():
    superpopulations = SamplePopulation.query.with_entities(SamplePopulation.SuperPopulation).distinct().all()
    return jsonify([superpop.SuperPopulation for superpop in superpopulations])

@bp.route('/get_sample_ids_from_populations')
def get_sample_ids_from_populations(selected_populations):
    # Query the SamplePopulation table for the SampleID of the selected populations
    sample_ids_result = SamplePopulation.query.with_entities(SamplePopulation.SampleID)\
                           .filter(SamplePopulation.Population.in_(selected_populations)).all()
    # Extract the SampleIDs from the result
    sample_ids = [result.SampleID for result in sample_ids_result]
    return sample_ids

@bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(f'static/{filename}', as_attachment=True)
    
@bp.route('/pca', methods=['GET'])
def perform_pca():
    populations = request.args.get('populations', '').split(',')
    superpopulations = request.args.get('superpopulations', '').split(',')
    
    # Filter out empty strings if no selections are made
    populations = [p for p in populations if p]
    superpopulations = [sp for sp in superpopulations if sp]
    
    # Construct the query based on selected populations and/or superpopulations
    query = db.session.query(SamplePopulation, ClusteringAnalysis)\
                     .join(ClusteringAnalysis, SamplePopulation.SampleID == ClusteringAnalysis.SampleID)
    filters = []   
    if populations:
        filters.append(SamplePopulation.Population.in_(populations))
    if superpopulations:
        filters.append(SamplePopulation.SuperPopulation.in_(superpopulations))
    query = query.filter(or_(*filters))
    
    # Execute the query
    filtered_data = query.all()
    
    # Check if filtered data is empty and return an appropriate response
    if not filtered_data: 
        return jsonify({'error': 'No matching data found for the selected populations or superpopulations'}), 400

    pca_data_with_labels = [
        (
            data.SamplePopulation.Population if populations else data.SamplePopulation.SuperPopulation,
            data.ClusteringAnalysis.PC1, 
            data.ClusteringAnalysis.PC2
        ) 
        for data in filtered_data
    ]
    
    # Extract the data for PCA
    df = pd.DataFrame(pca_data_with_labels, columns=['Label', 'PC1', 'PC2'])

    # Assign colors to each label
    unique_labels = df['Label'].unique()
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))
    color_dict = dict(zip(unique_labels, colors))    
    
    # Create a plot
    plt.figure(figsize=(8, 6))
    for label, color in color_dict.items():
        label_df = df[df['Label'] == label]
        plt.scatter(label_df['PC1'], label_df['PC2'], alpha=0.5, color=color, label=label)

    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA of Selected Labels')
    plt.legend()

    # Save the plot to a bytes buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Encode the plot to base64 string and prepare for JSON response
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Send back the response
    return jsonify({"image": f"data:image/png;base64,{image_base64}"})

@bp.route('/search_snps', methods=['POST'])
def search_snps(): 
    data = request.json
    search_type = data.get('searchType')
    search_input = data.get('searchInput')
    selected_populations = data.get('populations', [])

    # Begin constructing the base query
    base_query = db.session.query(SNPData.SNP_ID, SNPData.Genes, SNPData.ClinicalRelevance,
                                  func.avg(SamplePopulation.GTFreq_00).label('avg_GTFreq_00'),
                                  func.avg(SamplePopulation.GTFreq_01).label('avg_GTFreq_01'),
                                  func.avg(SamplePopulation.GTFreq_11).label('avg_GTFreq_11'),
                                  func.avg(SamplePopulation.REF_Freq).label('avg_REF_Freq'),
                                  func.avg(SamplePopulation.ALT_Freq).label('avg_ALT_Freq'))\
        .join(SampleData, SNPData.SNP_ID == SampleData.SNP_ID)\
        .join(SamplePopulation, SampleData.SampleID == SamplePopulation.SampleID)\
        .group_by(SNPData.SNP_ID)

    if selected_populations:
        base_query = base_query.filter(SamplePopulation.Population.in_(selected_populations))

    # Filter the query based on the search type
    if search_type == 'id':
        snp_ids = search_input.split(',')
        base_query = base_query.filter(SNPData.SNP_ID.in_(snp_ids))
    elif search_type == 'region':
        chrom, start, end = search_input.split(':')
        start, end = int(start), int(end)
        base_query = base_query.filter(SNPData.Chromosome_Number == chrom,
                                       SNPData.Chromosome_Position >= start,
                                       SNPData.Chromosome_Position <= end)
    elif search_type == 'gene':
        genes = search_input.split(',')
        base_query = base_query.filter(SNPData.Genes.in_(genes))

    # Execute the aggregated query
    aggregated_results = base_query.all()

    # Serialize results
    results = [{
        'SNP_ID': snp.SNP_ID,
        'Genes': snp.Genes,
        'ClinicalRelevance': snp.ClinicalRelevance,
        'AverageGTFreq_00': snp.avg_GTFreq_00,
        'AverageGTFreq_01': snp.avg_GTFreq_01,
        'AverageGTFreq_11': snp.avg_GTFreq_11,
        'AverageREF_Freq': snp.avg_REF_Freq,
        'AverageALT_Freq': snp.avg_ALT_Freq,
    } for snp in aggregated_results]

    return jsonify(results)

@bp.route('/compute_fst', methods=['POST'])
def compute_fst():
    data = request.json
    populations = data['populations']
    
    # Get allele frequencies for all populations first to avoid repeated database calls
    all_allele_freqs = {pop: get_allele_frequencies_for_population(pop) for pop in populations}
    
    # Initialize a matrix filled with zeros
    fst_matrix = [[0 for _ in populations] for _ in populations]
    
    # Calculate pairwise FST values
    for i, pop1 in enumerate(populations):
        allele_freqs_pop1 = all_allele_freqs[pop1]
        for j, pop2 in enumerate(populations):
            if i < j:  # Only compute upper triangle
                allele_freqs_pop2 = all_allele_freqs[pop2]
                fst_values = calculate_fst(allele_freqs_pop1, allele_freqs_pop2)
                fst = np.mean(list(fst_values.values()))
                fst_matrix[i][j] = fst
                fst_matrix[j][i] = fst  # Symmetric cell

    # Assume you have functions save_matrix_to_csv and generate_heatmap implemented
    save_matrix_to_csv(fst_matrix, populations)  # You need to define this function
    generate_heatmap(fst_matrix, populations)    # You need to define this function
    
    # Generate URLs for the heatmap and matrix download
    heatmap_download_url = url_for('static', filename='fst_heatmap.png')  # Adjust as needed
    matrix_download_url = url_for('static', filename='fst_matrix.csv')    # Adjust as needed
                
    return jsonify({
        'heatmapPath': heatmap_download_url,
        'matrixDownloadPath': matrix_download_url
    })

@bp.route('/fetch_admixture_data', methods=['POST'])
def fetch_admixture_data():
    # Retrieve JSON-encoded selections and decode them
    selected_populations = json.loads(request.form.get('populations', '[]'))
    selected_superpopulations = json.loads(request.form.get('superpopulations', '[]'))
        
    query = db.session.query(AdmixtureAnalysis)
                
    # Filter by multiple populations if any are selected
    if selected_populations:
        query = query.join(SamplePopulation).filter(SamplePopulation.Population.in_(selected_populations))
    # Filter by multiple superpopulations if any are selected
    if selected_superpopulations:
        query = query.join(SamplePopulation).filter(SamplePopulation.SuperPopulation.in_(selected_superpopulations))
    
    results = query.all()
    
    # Prepare datasets for the stacked bar plot
    datasets = []
    ancestries = ['Ancestry1', 'Ancestry2', 'Ancestry3', 'Ancestry4', 'Ancestry5', 'Ancestry6']
    colors = ["#ffcc00", "#ff6600", "#ff0000", "#6600cc", "#009900", "#00ccff"]
    
    for i, ancestry in enumerate(ancestries):
        # Aggregate ancestry data for each selected population/superpopulation
        ancestry_data = [getattr(result, f'Ancestry{i+1}') for result in results]
        datasets.append({
            'label': ancestry,
            'data': ancestry_data,
            'backgroundColor': colors[i]
        })

    # Use SampleIDs as labels for the chart
    labels = [result.SampleID for result in results]
    
    data = {
        'labels': labels,
        'datasets': datasets
    }           
    
    return jsonify(data)