import gurobipy as gp
from gurobipy import GRB

def solve_part2(omega, M_w, seekers, jobs, compatible_pairs, dissimilarities):
    model = gp.Model("Job_Matching_Dissimilarity")

    # Decision Variable
    # x[i,j] = 1 means seeker i is matched to job j.
    x = model.addVars([k for k in compatible_pairs if compatible_pairs[k]], vtype=GRB.BINARY, name="x")

    # The variable "z" captures the maximum dissimilarity value
    z = model.addVar(vtype=GRB.CONTINUOUS, name="max_dissimilarity")

    # Objective Function
    # gurobipy quickly sums up the dissimilarity value "z" and minimizes it
    model.setObjective(z, GRB.MINIMIZE)

    # Less than <=1 constraint: Each seeker can be assigned to at most 1 job opening
    for i in seekers.index:
        model.addConstr(gp.quicksum(x[i, j] for (si, j) in x if si == i) <= 1)

    # Second constraint: The number of seekers assigned to a job opening cannot exceed its available positions (Pj)
    # This constraint ensures that the total number of seekers assigned to job j less than or equal to the job's capacity
    for j in jobs.index:
        model.addConstr(gp.quicksum(x[i, j] for (i, sj) in x if sj == j) <= jobs.loc[j, 'Num_Positions'])

    # This constraint is the special constraint which is only for Part 2: The total priority weight achieved by the matches
        # in the model is at least (omega)% of the maximum value found in Part 1.
    model.addConstr(gp.quicksum(jobs.loc[j, 'Priority_Weight'] * x[i, j] for (i, j) in x) >= omega * M_w)

    # This forces z to be at least as big as any dissimilarity for an assigned pair (i,j).
    for (i, j) in x:
        model.addConstr(z >= dissimilarities[(i, j)] * x[i, j])

    # We capture the maximum dissimilarity by the value of z and then try to optimize it with the model to minimize the Maximum Dissimilarity

    model.optimize()

    if model.status == GRB.OPTIMAL:
        return model.objVal, {k: v.X for k, v in x.items()}
    else:
        raise Exception("No optimal solution found.")
