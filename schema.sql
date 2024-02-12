CREATE TABLE SNPData (
    SNP_ID VARCHAR(255) PRIMARY KEY,
    Chromosome_Number INT,
    Chromosome_Position INT,
    GTFreq_00 FLOAT,
    GTFreq_01 FLOAT,
    GTFreq_11 FLOAT,
    AlleleFrequency FLOAT,
    Genes VARCHAR(255),
    ClinicalRelevance VARCHAR(1024)
);
CREATE TABLE SamplePopulation (
    SampleID VARCHAR(255) PRIMARY KEY,
    Population VARCHAR(255),
    SuperPopulation VARCHAR(255)
);

CREATE TABLE ClusteringAnalysis (
    SampleID VARCHAR(255),
    PC1 FLOAT,
    PC2 FLOAT,
    PRIMARY KEY (SampleID),
    FOREIGN KEY (SampleID) REFERENCES SamplePopulation(SampleID)
);

CREATE TABLE AdmixtureAnalysis (
    SampleID VARCHAR(255),
    Ancestry1 FLOAT,
    Ancestry2 FLOAT,
    Ancestry3 FLOAT,
    Ancestry4 FLOAT,
    Ancestry5 FLOAT,
    PRIMARY KEY (SampleID),
    FOREIGN KEY (SampleID) REFERENCES SamplePopulation(SampleID)
);

CREATE TABLE SampleData (
    SampleID VARCHAR(255),
    SNP_ID VARCHAR(255),
    PRIMARY KEY (SampleID, SNP_ID),
    FOREIGN KEY (SampleID) REFERENCES SamplePopulation(SampleID),
    FOREIGN KEY (SNP_ID) REFERENCES SNPData(SNP_ID)
);
