import gurobipy as gp
from gurobipy import GRB

def solve_part1(seekers, jobs, compatible_pairs):
    model = gp.Model("Job_Matching_Priority")

    x = model.addVars([k for k in compatible_pairs if compatible_pairs[k]], vtype=GRB.BINARY, name="x")

    model.setObjective(gp.quicksum(jobs.loc[j, 'Priority_Weight'] * x[i, j]
                                   for (i, j) in x), GRB.MAXIMIZE)

    for i in seekers.index:
        model.addConstr(gp.quicksum(x[i, j] for (si, j) in x if si == i) <= 1)

    for j in jobs.index:
        model.addConstr(gp.quicksum(x[i, j] for (i, sj) in x if sj == j) <= jobs.loc[j, 'Num_Positions'])

    model.optimize()

    if model.status == GRB.OPTIMAL:
        return model.objVal, {k: v.X for k, v in x.items()}
    else:
        raise Exception("No optimal solution found.")
