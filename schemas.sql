CREATE TABLE PopulationData ( Population VARCHAR(255) PRIMARY KEY, SuperPopulation VARCHAR(255) ); 

CREATE TABLE SampleData ( SAMPLE_ID VARCHAR(255) PRIMARY KEY, Population VARCHAR(255), FOREIGN KEY (Population) REFERENCES PopulationData(Population) );

CREATE TABLE SNPData ( SNP_ID VARCHAR(255) PRIMARY KEY, GENE_NAME VARCHAR(255), CHROMOSOMAL_POSITION INT );

CREATE TABLE ClinicalRelevanceData (
    SNP_ID VARCHAR(255),
    ClinicalTraits VARCHAR(255),
    PRIMARY KEY (SNP_ID, ClinicalTraits),
    FOREIGN KEY (SNP_ID) REFERENCES SNPData(SNP_ID)
);

CREATE TABLE GenotypeData (
    SAMPLE_ID VARCHAR(255),
    SNP_ID VARCHAR(255),
    Genotype VARCHAR(255),
    GenotypeFrequency FLOAT,
    PRIMARY KEY (SAMPLE_ID, SNP_ID, Genotype),
    FOREIGN KEY (SAMPLE_ID) REFERENCES SampleData(SAMPLE_ID),
    FOREIGN KEY (SNP_ID) REFERENCES SNPData(SNP_ID)
);

CREATE TABLE VariantData (
    SAMPLE_ID VARCHAR(255),
    SNP_ID VARCHAR(255),
    AlleleFrequency FLOAT,
    PRIMARY KEY (SAMPLE_ID, SNP_ID),
    FOREIGN KEY (SAMPLE_ID) REFERENCES SampleData(SAMPLE_ID),
    FOREIGN KEY (SNP_ID) REFERENCES SNPData(SNP_ID)
);

-- to create indexes for faster retrevial of frequent queries from bigger tables
CREATE INDEX idx_variantdata_snp_id ON VariantData(SNP_ID);
CREATE INDEX idx_genotypedata_snp_id ON GenotypeData(SNP_ID);
CREATE INDEX idx_snpdata_chromosome ON SNPData(CHROMOSOMAL_POSITION);
CREATE INDEX idx_snpdata_gene_name ON SNPData(GENE_NAME);
CREATE INDEX idx_sampledata_population ON SampleData(Population);
CREATE INDEX idx_variantdata_snp_sample ON VariantData(SNP_ID, SAMPLE_ID);
CREATE INDEX idx_genotypedata_snp_sample ON GenotypeData(SNP_ID, SAMPLE_ID);
