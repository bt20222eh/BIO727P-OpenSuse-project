from .models import db, SNPData, SampleData, SamplePopulation

def calculate_fst(allele_freqs_pop1, allele_freqs_pop2):
    fst_values = {}
    for snp_id, freqs1 in allele_freqs_pop1.items():
        # Unpack the REF_Freq and ALT_Freq from each population for the SNP
        p1_ref, p1_alt = freqs1
        p2_ref, p2_alt = allele_freqs_pop2[snp_id]

        # Calculate average allele frequencies across populations for both alleles
        p_avg_ref = (p1_ref + p2_ref) / 2
        p_avg_alt = (p1_alt + p2_alt) / 2

        # Calculate the variance of allele frequencies among populations
        sigma_sq_ref = ((p1_ref - p_avg_ref) ** 2 + (p2_ref - p_avg_ref) ** 2) / 2
        sigma_sq_alt = ((p1_alt - p_avg_alt) ** 2 + (p2_alt - p_avg_alt) ** 2) / 2

        # Calculate FST for reference and alternate alleles
        fst_ref = sigma_sq_ref / (p_avg_ref * (1 - p_avg_ref)) if p_avg_ref * (1 - p_avg_ref) > 0 else 0
        fst_alt = sigma_sq_alt / (p_avg_alt * (1 - p_avg_alt)) if p_avg_alt * (1 - p_avg_alt) > 0 else 0

        # Combine or select FST value; here we simply average them
        fst = (fst_ref + fst_alt) / 2

        fst_values[snp_id] = fst

    return fst_values


def get_allele_frequencies_for_population(population_name):
    # Adjusted to join SampleData with SamplePopulation to fetch SNP_ID and its frequencies
    query = db.session.query(SampleData.SNP_ID,
                             SamplePopulation.REF_Freq,
                             SamplePopulation.ALT_Freq)\
                      .join(SamplePopulation, SampleData.SampleID == SamplePopulation.SampleID)\
                      .filter(SamplePopulation.Population == population_name)

    # Execute the query and fetch results
    results = query.all()

    # Convert results to a dictionary {SNP_ID: (REF_Freq, ALT_Freq)}
    allele_freqs = {result.SNP_ID: (result.REF_Freq, result.ALT_Freq) for result in results}
    return allele_freqs
