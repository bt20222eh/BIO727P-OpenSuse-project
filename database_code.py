import cyvcf2
import sqlite3
import csv

# Connect to your SQL database
conn = sqlite3.connect('variants.db')
cursor = conn.cursor()

# Enable foreign key support
conn.execute('PRAGMA foreign_keys = ON;')

# Drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS SampleVariants')
cursor.execute('DROP TABLE IF EXISTS Variants')
cursor.execute('DROP TABLE IF EXISTS Samples')

# Create Variants table
cursor.execute('''
    CREATE TABLE Variants (
        VAR_ID text PRIMARY KEY,
        POS integer,
        REF text,
        ALT text,
        AN integer,
        AC integer
    )
''')

# Create Samples table
cursor.execute('''
    CREATE TABLE Samples (
        SAMPLE_ID text PRIMARY KEY,
        POPULATION text
    )
''')

# Create SampleVariants table (junction table)
cursor.execute('''
    CREATE TABLE SampleVariants (
        SAMPLE_ID text,
        VAR_ID text,
        Genotype text,
        FOREIGN KEY (SAMPLE_ID) REFERENCES Samples(SAMPLE_ID),
        FOREIGN KEY (VAR_ID) REFERENCES Variants(VAR_ID)
    )
''')

# Populate the Samples table from tsv file
tsv_file_path = 'sample_pop.tsv'
# Populate the Samples table from tsv file
with open(tsv_file_path, 'r') as tsvfile:
    tsvreader = csv.DictReader(tsvfile, delimiter='\t')
    for row in tsvreader:
        cursor.execute('INSERT INTO Samples (SAMPLE_ID, POPULATION) VALUES (?, ?)', (row['id'], row['population']))

# Open the VCF file using cyvcf2
vcf_reader = cyvcf2.VCF('chr1.vcf.gz')

# Process VCF records
for record in vcf_reader:
    # Extract AN and AC from INFO field or use default value of 0 if not present
    an = record.INFO.get('AN', 0)
    ac = record.INFO.get('AC', 0)

    # Insert data into Variants table
    cursor.execute('''
        INSERT INTO Variants (VAR_ID, POS, REF, ALT, AN, AC) VALUES (?, ?, ?, ?, ?, ?)
    ''', (record.ID, record.POS, record.REF, ','.join(record.ALT) if record.ALT else None, an, ac))

    # Collect genotypes for each sample and insert into SampleVariants
    for sample_id, genotype in zip(vcf_reader.samples, record.genotypes):
        genotype_str = '|'.join(map(str, genotype[:2]))  # Convert genotype tuple to string
        if genotype_str in ['0|1', '1|1', '1|0']:
            cursor.execute('''
                INSERT INTO SampleVariants (SAMPLE_ID, VAR_ID, Genotype) VALUES (?, ?, ?)
            ''', (sample_id, record.ID, genotype_str))

# Commit and close
conn.commit()
conn.close()



