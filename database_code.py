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
