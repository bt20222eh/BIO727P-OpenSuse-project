import cyvcf2
import sqlite3
import csv

# Connect to your SQL database
conn = sqlite3.connect('variants.db')
cursor = conn.cursor()

# Enable foreign key support
conn.execute('PRAGMA foreign_keys = ON;')

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Variants (
        VAR_ID text PRIMARY KEY,
        POS integer,
        REF text,
        ALT text,
        AN integer,
        AC integer,
        Genotypes text
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sample (
        SAMPLE_ID text PRIMARY KEY,
        POPULATION text
    )
''')

# Populate the Sample table from tsv file
tsv_file_path = 'sample_pop.tsv'
with open(tsv_file_path, 'r') as tsvfile:
    tsvreader = csv.DictReader(tsvfile, delimiter='\t')
    for row in tsvreader:
        cursor.execute('INSERT INTO Sample (SAMPLE_ID, POPULATION) VALUES (?, ?)', (row['id'], row['population']))

# Open the VCF file using cyvcf2
vcf_reader = cyvcf2.VCF('chr1.vcf.gz')

# Process VCF records
for record in vcf_reader:
    # Extract AN and AC from INFO field or use default value of 0 if not present
    an = record.INFO.get('AN', 0)
    ac = record.INFO.get('AC', 0)

    # Collect genotypes for each sample, excluding missing data and reference genotypes
    genotypes = []
    for sample_id, genotype in zip(vcf_reader.samples, record.genotypes):
        genotype_str = '|'.join(map(str, genotype[:2]))  # Convert genotype tuple to string
        if genotype_str in ['0|1', '1|1', '1|0']:
            genotypes.append(f"{sample_id}:{genotype_str}")
    
    if genotypes:  # If there are any non-reference genotypes
        genotypes_str = ';'.join(genotypes)  # Serialize the list of genotypes to a string
        cursor.execute('''
            INSERT INTO Variants (VAR_ID, POS, REF, ALT, AN, AC, Genotypes) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (record.ID, record.POS, record.REF, ','.join(record.ALT) if record.ALT else None, an, ac, genotypes_str))

# Commit and close
conn.commit()
conn.close()
