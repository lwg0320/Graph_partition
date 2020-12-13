# CS 170 Project Fall 2020

## Problem Statement

Your job is to place n students into Zoom breakout rooms. For each pair of students i and j, there is one value h_{i,j} quantifying how much happiness these two students give each other and one value s_{i,j} quantifying how much stress they give each other. The total happiness value of a room H_{room} is the sum of the happiness values h_{i,j} of every student pair in that room, and the total stress value of a room S_room is the sum of the stress values s_{i,j}  of every student pair in that room. Knowing that trying to eliminate student stress is impossible, we have settled with keeping total student stress low enough so that it does not surpass S_max/k in each room, where k is the number of breakout rooms you choose to open. Your goal is to maximize total happiness H_{total} across all rooms, while keeping the total stress below the threshold S_max/k in each room.

### Input parameters:
• n = Number of students in the class 

• h_{i,j} = Happiness student i and j give each other 

• s_{i,j} = Stress student i and j induce on each other
 
• S_max = Maximum total stress across all breakout rooms 



### Output values:
• H_r = Happiness of breakout room r 

• S_r = Stress of breakout room r 

• H_{total} = Total happiness across all breakout rooms 

• k = Total number of breakout rooms opened 


### Files 
• algorithm.pdf: pseudocode for QILP and ILP algorithms
• solver.py: Main solver used to generate outputs 