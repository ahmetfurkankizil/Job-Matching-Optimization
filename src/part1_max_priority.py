import gurobipy as gp
from gurobipy import GRB

def solve_part1(seekers, jobs, p, pairs):
    """
    Solves the job matching problem to maximize total priority weight.
    
    Args:
        seekers (DataFrame): DataFrame containing seeker information
        jobs (DataFrame): DataFrame containing job information with columns:
                         - 'Priority_Weight': Weight for priority calculation
                         - 'Num_Positions': Available positions per job
        p (dict): Dictionary of compatibility values (keys: (i,j) tuples)
        
    Returns:
        tuple: (optimal objective value, solution dictionary)
        
    Raises:
        ValueError: If input data is inconsistent
        Exception: If no optimal solution found
    """
    model = gp.Model("Job_Matching_Priority")

    # ========== Data Validation ==========
    # Check for valid (i,j) pairs that exist in both the indices and compatibility matrix
    
    # ========== Decision Variables ==========
    # x[i,j] = 1 means seeker i is matched to job j.
    x = model.addVars(pairs, vtype=GRB.BINARY, name="x")

    # ========== Objective Function ==========
    # gurobipy quickly sums up the Total Priority-Weights and maximizes it
    model.setObjective(
        gp.quicksum(jobs.loc[j, 'Priority_Weight'] * x[i, j] for i, j in pairs),
        GRB.MAXIMIZE
    )

    # ========== Constraints ==========
    # 1. Each seeker gets at most one job
    model.addConstrs(
        (x.sum(i, '*') <= 1 for i in seekers.index 
         if any((i, j) in pairs for j in jobs.index)),
        name="seeker_assignment_limit"
    )

    # 2. Job positions cannot be exceeded
    model.addConstrs(
        (x.sum('*', j) <= jobs.loc[j, 'Num_Positions'] for j in jobs.index 
         if any((i, j) in pairs for i in seekers.index)),
        name="job_capacity"
    )

    # 3. Seeker i must be compatible with job j
    #    (i.e., x[i,j] can only be 1 if p[i,j] is 1)
    model.addConstrs(
        (x[i, j] <= p[i, j] for i, j in pairs),
        name="compatibility"
    )

    # ========== Solve Model ==========
    model.optimize()

    # ========== Handle Results ==========
    if model.status == GRB.OPTIMAL:
        return model.objVal, {k: v.X for k, v in x.items()}
    else:
        raise Exception(f"No optimal solution found. Status: {model.status}")
