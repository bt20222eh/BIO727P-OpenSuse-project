from . import db

class SNPData(db.Model):
    __tablename__ = 'SNPData'
    SNP_ID = db.Column(db.String(255), primary_key=True)
    Chromosome_Number = db.Column(db.Integer)
    Chromosome_Position = db.Column(db.Integer)
    Genes = db.Column(db.String(255))
    ClinicalRelevance = db.Column(db.String(1024))

class SamplePopulation(db.Model):
    __tablename__ = 'SamplePopulation'
    SampleID = db.Column(db.String(255), primary_key=True)
    Population = db.Column(db.String(255))
    SuperPopulation = db.Column(db.String(255))
    GTFreq_00 = db.Column(db.Float)
    GTFreq_01 = db.Column(db.Float)
    GTFreq_11 = db.Column(db.Float)
    REF_Freq = db.Column(db.Float)
    ALT_Freq = db.Column(db.Float)

class SampleData(db.Model):
    __tablename__ = 'SampleData'
    SampleID = db.Column(db.String(255), db.ForeignKey('SamplePopulation.SampleID'), primary_key=True)
    SNP_ID = db.Column(db.String(255), db.ForeignKey('SNPData.SNP_ID'), primary_key=True)
    sample = db.relationship('SamplePopulation', back_populates='sample_data')
    snp = db.relationship('SNPData', back_populates='sample_data')

SNPData.sample_data = db.relationship('SampleData', back_populates='snp')
SamplePopulation.sample_data = db.relationship('SampleData', back_populates='sample')

class ClusteringAnalysis(db.Model):
    __tablename__ = 'ClusteringAnalysis'
    SampleID = db.Column(db.String(255), db.ForeignKey('SamplePopulation.SampleID'), primary_key=True)
    PC1 = db.Column(db.Float)
    PC2 = db.Column(db.Float)
    sample_population = db.relationship('SamplePopulation', backref=db.backref('clustering_analysis', lazy=True))

class AdmixtureAnalysis(db.Model):
    __tablename__ = 'AdmixtureAnalysis'
    SampleID = db.Column(db.String(255), db.ForeignKey('SamplePopulation.SampleID'), primary_key=True)
    Ancestry1 = db.Column(db.Float)
    Ancestry2 = db.Column(db.Float)
    Ancestry3 = db.Column(db.Float)
    Ancestry4 = db.Column(db.Float)
    Ancestry5 = db.Column(db.Float)
    Ancestry6 = db.Column(db.Float)
    sample_population = db.relationship('SamplePopulation', backref=db.backref('admixture_analysis', lazy=True))
