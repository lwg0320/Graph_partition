## Modular Gurobi Solver 

import numpy as np 
import pandas as pd
from parse_aws import *
from utils_aws  import *
from math import *
import gurobipy as gp
from gurobipy import GRB

# import networkx as nx


# ## Solver


def parse_inputs(inputs, K):
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
    
    return i_id, j_id, sadness, happiness, sadness_1, happiness_1 


# In[3]:


def create_variables(N, K, dict_e, dict_v):
    # edges 
    edges_1 = list(dict_e.values())

    # Create another edge array with different sort
    edges_2 = [dict_e.get(i) for i in sorted(dict_e.keys(), key=lambda x: (x[2], x[4]))]

    # Create another edge array for constraint 4 
    edges_3 = [dict_e.get(i) for i in sorted(dict_e.keys(), key=lambda x: (x[2], x[6]))]


    # vertices 
    vertices_1 = list(dict_v.values())

    # Create another edge array with different sort
#     vertices_2 = [dict_v.get(i) for i in sorted(dict_v.keys(), key=lambda x: x[2])]
    vertices_2 = [dict_v.get(i) for i in sorted(dict_v.keys())]
    
    # Quadratic variables 1 
    v_list = np.array(np.array_split(vertices_1, K)).tolist()
    v_big = []
    for i in range(K):
        j = 0
        while j != N:
            for _ in range(j,N-1):
                v_big.append(v_list[i][j])
            j += 1

    # Quadratic variables 2
    v_list_2 = [i[1:] for i in v_list]
    v_big_2 = []
    for h in range(K):
        j = 0
        while j != N:
            for i in range(j,N-1):
                v_big_2.append(v_list_2[h][i])
            j += 1
            i = j
    
    return edges_1, edges_2, edges_3, vertices_1, vertices_2, v_big, v_big_2


# In[4]:


def constraint_helper(edges_1, sadness_1, vertices_2, N, K):
    aa = []
    h = 0
    for i in range(K):
        for j in range(comb(N,2)):
            aa.append(edges_1[h] * sadness_1[j])
            h += 1
    constraint_1 = [sum(aa[i:i+ comb(N,2)]) for i in range(0, len(aa), comb(N,2))]
    constraint_2 = [sum(vertices_2[i:i + K]) for i in range(0, len(vertices_2), K)]
    return constraint_1, constraint_2


# In[43]:


def gurobi_solver(path, rooms, time_limit):
    '''
    Main solver function 
    
    path = location of the input file 
    rooms = number of rooms to open 
    time_limit = time limit for model runtime
    '''
    # Parsing input data 
    inputs = pd.read_csv(path, header = None)
    N = int(list(inputs[0])[0])
    s_max = float(list(inputs[0])[1])
    K = rooms
    i_id, j_id, sadness, happiness, sadness_1, happiness_1 = parse_inputs(inputs, K)

    # Initialize model
    m = gp.Model("proj")
    m.setParam('OutputFlag', 0)
    m.setParam("TuneOutput", 0)

    # Create arrays to help with methods 
    dict_e = {}
    for k in range(K):
        for i in range(comb(N, 2)):
            dict_e["e_{0}_{1}_{2}".format(i_id[i],j_id[i],k)] = m.addVar(name= "e_{0}_{1}_{2}".format(i_id[i],j_id[i],k), vtype = GRB.BINARY)

    dict_v = {}
    for j in range(K):
        for i in range(N):
            dict_v["v_{0}_{1}".format(i,j)] = m.addVar(name = "v_{0}_{1}".format(i,j),  vtype = GRB.BINARY)


    edges_1, edges_2, edges_3, vertices_1, vertices_2, v_big, v_big_2 = create_variables(N, K, dict_e, dict_v)

    # Set Object function 
    m.setObjective(sum(edges_1[i] * happiness[i] for i in range(len(happiness))), GRB.MAXIMIZE)

    # Helper method to create constraints 
    constraint_1, constraint_2 = constraint_helper(edges_1, sadness_1, vertices_2, N, K)

    # Add constraints 
    # Constraint 1 
    for i in range(len(constraint_1)):
        m.addConstr(constraint_1[i] <=  s_max / K) # Changes from float division 
    # Constraint 3
    for i in range(len(constraint_2)):
        m.addConstr(constraint_2[i] == 1)
    # Constraint 3 
    for i in range(len(edges_1)):
        m.addConstr(edges_1[i] == v_big[i] * v_big_2[i])

    # Optimize model 
    m.setParam('TimeLimit', time_limit)
    m.optimize()

    # Get outputs 
    pairs = m.getVars()[0 : len(m.getVars()) - N*K]
    people = m.getVars()[len(m.getVars()) - N*K : len(m.getVars())]
    try:
        people_values = [v.X for v in people]
        people_values = np.array_split(people_values, K)
        pair_values = [v.X for v in pairs]
        output_dict = {}
        for k in range(K):
            arr = []
            for i in range(N):
                if people_values[k][i] == 1: 
                    arr += [i]
                    output_dict[k] = arr
                            
    # Outputs 
        total_happiness = np.sum(np.multiply(pair_values, happiness))
        total_sadness = np.sum(np.multiply(pair_values, sadness))
        print("Total Happiness =", total_happiness)
        print(output_dict)
        return total_happiness, output_dict 
    except:
        print("No/Infeasible Solution with {0} rooms".format(rooms))
        return 0, {}



def optimal_solver(room_start, room_end, path, higher_time_limit, lower_time_limit):
    max_total_happiness = 0
    output_dict = {}
    for room in range(room_start, room_end):
        if max_total_happiness == 0:
            happiness, D = gurobi_solver(path, room, higher_time_limit)
            if happiness > max_total_happiness:
                max_total_happiness = happiness
                output_dict = D
        else: 
            happiness, D = gurobi_solver(path, room, lower_time_limit)
            if happiness > max_total_happiness:
                max_total_happiness = happiness
                output_dict = D

    return output_dict


def write_files(size, input_start, input_end, higher_time_limit, lower_time_limit, room_start, room_end):
    for i in range(input_start, input_end + 1):
        D = optimal_solver(room_start, room_end, "/home/ec2-user/170proj/phase2/inputs/{0}/{0}-{1}.in".format(size, i), higher_time_limit, lower_time_limit)
        output_dict = convert_dictionary(D)
        write_output_file(output_dict, "/home/ec2-user/170proj/phase2/outputs/{0}/{0}-{1}.out".format(size, i))




##########################

inputs = open('invalids.txt', 'r').readlines()


def run(size, index_start, index_end, higher_time_limit, lower_time_limit, room_start, room_end):
    for i in range(index_start, index_end + 1):
        D = optimal_solver(room_start, room_end, "/home/ec2-user/170proj/inputs_new/{0}.in".format(inputs[i][:-1]), higher_time_limit, lower_time_limit)
        output_dict = convert_dictionary(D)
        write_output_file(output_dict, "/home/ec2-user/170proj/outputs_new/{0}.out".format(inputs[i][:-1]))




def ru(higher_time_limit, lower_time_limit, room_start, room_end):
    D = optimal_solver(room_start, room_end, "small-148.in" ,higher_time_limit, lower_time_limit)
    output_dict = convert_dictionary(D)
    write_output_file(output_dict, "small-148.out")
























































