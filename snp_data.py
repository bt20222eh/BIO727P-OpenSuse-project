input_file_path = 'output_header.tsv'
snp_info = []

with open(input_file_path, mode='r', newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    next(reader)  # Skip the header row
    for row in reader:
        sample_id = row[0]
        snp_id = row[1]
        chromosomal_location = row[2]  # Assuming the location is in the third column
        snp_info.append((snp_id, chromosomal_location))
def fetch_gene_for_snp(chromosomal_location):
    url = f'https://rest.ensembl.org/overlap/region/human/{chromosomal_location}?feature=gene'
    headers = { 'Content-Type' : 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        genes = [gene['external_name'] for gene in data if gene.get('external_name')]
        return genes
    else:
        print(f'Error fetching gene for location {chromosomal_location}: {response.status_code} - {response.text}')
        return None
output_file_path = 'snp_genes.tsv'

with open(output_file_path, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    
    # Write the header
    writer.writerow(['Sample_ID', 'SNP_ID', 'ChromosomalLocation', 'Genes'])
    
    # Iterate over SNP info
    for snp_id, chromosomal_location in snp_info:
        genes = fetch_gene_for_snp(chromosomal_location)
        writer.writerow([snp_id, chromosomal_location, ';'.join(genes or ['No gene information found'])])
