from .models import db, SNPData, SampleData, SamplePopulation

def calculate_fst(avg_freqs_pop1, avg_freqs_pop2):
    """
    Calculate FST using precalculated average REF and ALT frequencies for two populations.
    """
    # Unpack the avgREF_Freq and avgALT_Freq for both populations
    p1_avg_ref, p1_avg_alt = avg_freqs_pop1
    p2_avg_ref, p2_avg_alt = avg_freqs_pop2

    # The rest of the calculation remains the same as in your existing calculate_fst function
    # Calculate average allele frequencies across populations for both alleles
    p_avg_ref = (p1_avg_ref + p2_avg_ref) / 2
    p_avg_alt = (p1_avg_alt + p2_avg_alt) / 2

    # Calculate the variance of allele frequencies among populations
    sigma_sq_ref = ((p1_avg_ref - p_avg_ref) ** 2 + (p2_avg_ref - p_avg_ref) ** 2) / 2
    sigma_sq_alt = ((p1_avg_alt - p_avg_alt) ** 2 + (p2_avg_alt - p_avg_alt) ** 2) / 2

    # Calculate FST for reference and alternate alleles
    fst_ref = sigma_sq_ref / (p_avg_ref * (1 - p_avg_ref)) if p_avg_ref * (1 - p_avg_ref) > 0 else 0
    fst_alt = sigma_sq_alt / (p_avg_alt * (1 - p_avg_alt)) if p_avg_alt * (1 - p_avg_alt) > 0 else 0

    # Combine or select FST value; here we simply average them
    fst = (fst_ref + fst_alt) / 2

    return fst

def get_population_avg_frequencies():
    """
    Fetch precalculated average REF and ALT frequencies for each population.
    Returns a dictionary with population names as keys and a tuple of (avgREF_Freq, avgALT_Freq) as values.
    """
    query = db.session.query(
        SamplePopulation.Population,
        SamplePopulation.avgREF_Freq,
        SamplePopulation.avgALT_Freq
    ).distinct()
    
    # Execute the query and fetch results
    results = query.all()

    # Convert results to a dictionary
    avg_freqs = {result.Population: (result.avgREF_Freq, result.avgALT_Freq) for result in results}
    return avg_freqs
