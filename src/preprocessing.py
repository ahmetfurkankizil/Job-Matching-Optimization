import pandas as pd
import ast

def parse_data(seekers_path, jobs_path, distances_path):
    seekers = pd.read_csv(seekers_path)
    jobs = pd.read_csv(jobs_path)
    location_distances = pd.read_csv(distances_path, index_col=0)

    for df, cols in [(seekers, ['Skills', 'Questionnaire']),
                     (jobs, ['Required_Skills', 'Questionnaire'])]:
        for col in cols:
            df[col] = df[col].apply(ast.literal_eval)

    return seekers, jobs, location_distances

# Fundamental requirements: All Fundamental Requirements are applied with this function for Part 1.
def is_compatible(seeker, job, distance_matrix):
    # Requirement 1 (Job Type): Seeker's desired type is compatible with the job's type, if not returns false
    if seeker['Desired_Job_Type'] != job['Job_Type']:
        return False
    # Requirement 2 (Salary): Seeker's minimum desired salary alighns with the job's salary offering
        # The logic is to compare the Seeker's Min_Desired_Salary with the Salary_Range_Max and return False if not.
        # Traversing each possible job-seeker combinations in the check_compatibilty function automatically filters
        # out the inappropriate ones from the model.
    if seeker['Min_Desired_Salary'] > job['Salary_Range_Max']:
        return False
    # Requirement 3 (Skills):  Seeker possesses all skills required by the job. Exact match for required skills is ensured
    if not set(job['Required_Skills']).issubset(seeker['Skills']):
        return False
    levels = ['Entry-level', 'Mid-level', 'Senior', 'Lead', 'Manager']
    # Requirement 4 (Experience): The experience levels are listed in levels array and simple index comparison is done satisfy.
    if levels.index(seeker['Experience_Level']) < levels.index(job['Required_Experience_Level']):
        return False
    # Requirement 5 (Location): If the job is not remote, then the distance between the job's nominal locaiton is compared
        # with the seeker's maximum commute distance. 
    if not job['Is_Remote']:
        distance = distance_matrix.loc[seeker['Location'], job['Location']]
        if distance > seeker['Max_Commute_Distance']:
            return False
    return True

def check_compatibility(seekers, jobs, location_distances):
    compatibility = {}
    for i, s in seekers.iterrows():
        for j, job in jobs.iterrows():
            compatibility[(i, j)] = is_compatible(s, job, location_distances)
    return compatibility

def calculate_dissimilarities(seekers, jobs, compatible_pairs):
    dissimilarity = {}
    for (i, j), valid in compatible_pairs.items():
        if valid:
            si = seekers.loc[i, 'Questionnaire']
            sj = jobs.loc[j, 'Questionnaire']
            dissimilarity[(i, j)] = sum(abs(a - b) for a, b in zip(si, sj)) / 20
    return dissimilarity
