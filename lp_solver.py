import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import networkx as nx
from parse import *
from utils  import *
from pulp import *
from math import comb


graph, budget = read_input_file("inputs/small/small-1.in")
pos = nx.kamada_kawai_layout(graph)  # positions for all nodes
nx.draw(graph, pos, with_labels=True)
prob = LpProblem("proj",LpMaximize)


inputs = pd.read_csv("inputs/small/small-1.in", header = None)
n = int(list(inputs[0])[0])
s_max = float(list(inputs[0])[1])
K = 3

# Parsing input data 
df = inputs
df = pd.DataFrame([x.split() for x in df[0].tolist() ])
df = df.loc[2:,:]
df["i"] = df.loc[:,0]
df["j"] = df.loc[:,1]
df["sadness"] = df.loc[:,3]
df["happiness"] = df.loc[:,2]
df = df[["i", "j", "sadness", "happiness"]]
i_id = [int(i) for i in list(df["i"])]
j_id = [int(i) for i in list(df["j"])]
sadness = [float(i) for i in list(df["sadness"])]*K
happiness = [float(i) for i in list(df["happiness"])]*K

sadness_1 = [float(i) for i in list(df["sadness"])]
happiness_1 = [float(i) for i in list(df["happiness"])]
len(sadness) == len(happiness)

prob = LpProblem("solver",LpMaximize)

# edges 
d_e = {}
for k in range(K):
    for i in range(comb(n,2)):
        d_e["e_{0}_{1}_{2}".format(i_id[i],j_id[i],k)] = LpVariable("e_{0}_{1}_{2}".format(i_id[i],j_id[i],k), cat="Binary")
edges_1 = list(d_e.values())


# Create another edge array with different sort
edges_2 = [d_e.get(i) for i in sorted(d_e.keys(), key=lambda x: (x[2], x[4]))]

# Create another edge array for constraint 4 
edges_3 = [d_e.get(i) for i in sorted(d_e.keys(), key=lambda x: (x[2], x[6]))]

# Check
len(edges_1) == comb(n,2)*K

# vertices 
d_v = {}
for j in range(K):
    for i in range(n):
        d_v["v_{0}_{1}".format(i,j)] = LpVariable("v_{0}_{1}".format(i,j), cat="Binary")
vertices_1 = list(d_v.values())

# Create another edge array with different sort
vertices_2 = [d_v.get(i) for i in sorted(d_v.keys(), key=lambda x: x[2])]

# Check
len(vertices_1) == n*K

# Linearization of quadratic variables 1 
v_list = np.array(np.array_split(vertices_1, K)).tolist()
v_big = []
for i in range(K):
    j = 0
    while j != n:
        for _ in range(j,n-1):
            v_big.append(v_list[i][j])
        j += 1
        
print(len(edges_1) == len(v_big))

# Linearization of quadratic variables 2
v_list_2 = [i[1:] for i in v_list]
v_big_2 = []
for h in range(K):
    j = 0
    while j != n:
        for i in range(j,n-1):
            v_big_2.append(v_list_2[h][i])
        j += 1
        i = j
print(len(edges_1) == len(v_big_2))

##LP Solver 
# Objective function 
prob += sum(edges_1[i] * happiness[i] for i in range(len(happiness)))

# Constraint 1
# Each rooms has sadness levels <= s_max / K 
aa = []
h = 0
for i in range(K):
    for j in range(comb(n,2)):
        aa.append(edges_1[h] * sadness_1[j])
        h += 1
constraint_2 = [sum(aa[i:i+ comb(n,2)]) for i in range(0, len(aa), comb(n,2))]
for i in range(len(constraint_2)):
    prob += constraint_2[i] <= s_max / K
# Constraint 2
# Each person belongs to only one room
constraint_3 = [sum(vertices_2[i:i + K]) for i in range(0, len(vertices_2), K)]
for i in range(len(constraint_3)):
    prob += constraint_3[i] == 1
# Linearization of quadratic variables
# Constraint 3.1
for i in range(len(edges_1)):
    prob += edges_1[i] <= v_big[i]    
# Constraint 3.2
for i in range(len(edges_1)):
    prob += edges_1[i] <= v_big_2[i]
# Constraint 3.3
for i in range(len(edges_1)):
    prob += edges_1[i] >= v_big[i] + v_big_2[i] - 1 

prob.solve()

variables = [v.varValue for v in prob.variables()[len(prob.variables()) - n*K : len(prob.variables())]]
locations = list(np.mod(np.nonzero(variables)[0], K))
output_dict = dict(list(enumerate(locations)))
print(output_dict)
print(is_valid_solution(output_dict, graph, s_max, K))
# write_output_file(output_dict, "path")

