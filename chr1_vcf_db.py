import cyvcf2
import sqlite3
import csv

# Connect to your SQL database
conn = sqlite3.connect('variants.db')
cursor = conn.cursor()

# Enable foreign key support
conn.execute('PRAGMA foreign_keys = ON;')

# Create the Variants table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Variants (
        POS integer,
        ID text PRIMARY KEY,
        REF text,
        ALT text
    )
''')

# Create the SamplePopulation table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SamplePopulation (
        id text PRIMARY KEY,
        population text
    )
''')

# Create a new associative table VariantSample
cursor.execute('''
    CREATE TABLE IF NOT EXISTS VariantSample (
        VariantID text,
        SampleID text,
        PRIMARY KEY (VariantID, SampleID),
        FOREIGN KEY (VariantID) REFERENCES Variants(ID),
        FOREIGN KEY (SampleID) REFERENCES SamplePopulation(id)
    )
''')

# Populate the SamplePopulation table from tsv file
tsv_file_path = 'sample_pop.tsv'
with open(tsv_file_path, 'r') as tsvfile:
    tsvreader = csv.DictReader(tsvfile, delimiter='\t')
    for row in tsvreader:
        # Extract id and population
        id = row['id']
        population = row['population']
        # Insert data into the SamplePopulation table
        cursor.execute('''
            INSERT INTO SamplePopulation (id, population) VALUES (?, ?)
        ''', (id, population))

# Open the VCF file using cyvcf2
vcf_reader = cyvcf2.VCF('chr1.vcf.gz')

# Read sample IDs from the VCF file header assuming they are in the header
sample_ids = vcf_reader.samples

for record in vcf_reader:
    # Convert the ALT field which might be a list to a string
    alt = ','.join(record.ALT) if record.ALT else None
    
    # Insert variant data
    cursor.execute('''
        INSERT INTO Variants (POS, ID, REF, ALT) VALUES (?, ?, ?, ?)
    ''', (record.POS, record.ID, record.REF, alt))

    # Get the genotype for each sample
    genotypes = record.genotypes

    # Insert relationships into VariantSample table
    for i, genotype in enumerate(genotypes):
        if genotype[:2] != [0, 0]:  # Check if the sample has the SNP based on your criteria
            cursor.execute('''
                INSERT OR IGNORE INTO VariantSample (VariantID, SampleID) 
VALUES (?, ?)
            ''', (record.ID, sample_ids[i]))

# Commit and close
conn.commit()
conn.close()

