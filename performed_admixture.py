@app.route('/perform_admixture', methods=['GET'])
def perform_admixture():
    populations = request.args.get('Populations', '').split(',')
    superpopulations = request.args.get('SuperPopulations', '').split(',')
    
    # Filter out empty strings if no selections are made
    populations = [p for p in populations if p]
    superpopulations = [sp for sp in superpopulations if sp]

    # Construct the title based on selected populations or superpopulations
    selected_items = populations if populations else superpopulations
    title = 'Admixture Analysis Plot'

    # Construct the query to fetch data from both tables
    query = db.session.query(AdmixtureAnalysis, SamplePopulation)\
                      .join(SamplePopulation, AdmixtureAnalysis.SampleID == SamplePopulation.SampleID)
    
    
    # Filter data based on selected populations or superpopulations
    if populations:
        query = query.filter(SamplePopulation.Population.in_(populations))
    if superpopulations:
        query = query.filter(SamplePopulation.SuperPopulation.in_(superpopulations))

    # Execute the query and fetch data
    admixture_data = query.all()
    
    # Check if data is empty and return an appropriate response
    if not admixture_data:
        return jsonify({'error': 'No data found for the selected populations or superpopulations'}), 400
    
    # Extract ancestry proportions from the data
    ancestry_columns = ['Ancestry1', 'Ancestry2', 'Ancestry3', 'Ancestry4', 'Ancestry5', 'Ancestry6']
    ancestry_proportions = [[getattr(entry.AdmixtureAnalysis, col) for col in ancestry_columns] for entry in admixture_data]

    # Create a DataFrame for the ancestry proportions
    df = pd.DataFrame(ancestry_proportions, columns=[f'Ancestry {i}' for i in range(1, 7)])

    # Create a stacked bar plot
    plt.figure(figsize=(10, 6))
    bottom = None
    for i in range(df.shape[1]):
        if bottom is None:
            plt.bar(range(len(df)), df.iloc[:, i], label=f'Ancestry {i+1}')
            bottom = df.iloc[:, i].values
        else:
            plt.bar(range(len(df)), df.iloc[:, i], bottom=bottom, label=f'Ancestry {i+1}')
            bottom += df.iloc[:, i].values

    # Customize plot
    plt.xlabel('Individuals')
    plt.ylabel('Ancestry Proportion')
    plt.title(title)
    plt.legend(title='Ancestry')

    # Save the plot to a bytes buffer
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)

    # Encode the plot to base64 string and prepare for JSON response
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Send back the response
    return jsonify({"image": f"data:image/png;base64,{image_base64}", "title": title})
