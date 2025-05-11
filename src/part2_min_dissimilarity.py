import gurobipy as gp
from gurobipy import GRB

def solve_part2(omega, M_w, seekers, jobs, p, pairs, dissimilarities):
    model = gp.Model("Job_Matching_Dissimilarity")

    
    # ========== Decision Variables ==========
    # x[i,j] = 1 means seeker i is matched to job j.
    x = model.addVars(pairs, vtype=GRB.BINARY, name="x")
    z = model.addVar(vtype=GRB.CONTINUOUS, name="max_dissimilarity")
    
     # ========== Objective Function ==========
    model.setObjective(z, GRB.MINIMIZE)
    
    # ========== Constraints ==========
    # Constraints only for valid pairs
    # 1. This constraint is the special constraint which is only for Part 2: The total priority weight achieved by the matches
    # in the model is at least (omega)% of the maximum value found in Part 1.
    model.addConstr(
        gp.quicksum(jobs.loc[j, 'Priority_Weight'] * x[i,j] for i,j in pairs) >= omega * M_w,
        name="min_priority"
    )

    # 2. This forces z to be at least as big as any dissimilarity for an assigned pair (i,j).
    model.addConstrs(
        (z >= dissimilarities[i,j] * x[i,j] for i,j in pairs),
        name="dissimilarity_bound"
    )
    # Constrainsts from Part 1 
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
    
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        return model.objVal, {k: v.X for k, v in x.items()}
    else:
        raise Exception(f"No solution found. Status: {model.status}")