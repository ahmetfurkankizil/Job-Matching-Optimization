import gurobipy as gp
from gurobipy import GRB

def solve_part1(seekers, jobs, compatible_pairs):
    model = gp.Model("Job_Matching_Priority")

    # Decision Variable
    # x[i,j] = 1 means seeker i is matched to job j.
    x = model.addVars([k for k in compatible_pairs if compatible_pairs[k]], vtype=GRB.BINARY, name="x")

    # Objective Function
    # gurobipy quickly sums up the Total Priority-Weights and maximizes it
    model.setObjective(gp.quicksum(jobs.loc[j, 'Priority_Weight'] * x[i, j]
                                   for (i, j) in x), GRB.MAXIMIZE)

    # Less than <=1 constraint: Each seeker can be assigned to at most 1 job opening
    for i in seekers.index:
        model.addConstr(gp.quicksum(x[i, j] for (si, j) in x if si == i) <= 1)

    # Second constraint: The number of seekers assigned to a job opening cannot exceed its available positions (Pj)
    # This constraint ensures that the total number of seekers assigned to job j less than or equal to the job's capacity
    for j in jobs.index:
        model.addConstr(gp.quicksum(x[i, j] for (i, sj) in x if sj == j) <= jobs.loc[j, 'Num_Positions'])

    model.optimize()

    if model.status == GRB.OPTIMAL:
        return model.objVal, {k: v.X for k, v in x.items()}
    else:
        raise Exception("No optimal solution found.")
