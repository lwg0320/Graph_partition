import pandas as pd

# inputs_path = "inputs_sub/"
inputs = open('invalids.txt', 'r').readlines()



# for file in range(len(inputs)):

inputs_file = pd.read_csv("{0}0.in".format(inputs[25][:-1]), header = None)
inputs_file = pd.DataFrame(inputs_file)
df = inputs_file
df = pd.DataFrame([x.split() for x in df[0].tolist() ])
df = df.loc[2:,:]
df["i"] = df.loc[:,0]
df["j"] = df.loc[:,1]
df["sadness"] = df.loc[:,3]
df["happiness"] = df.loc[:,2]
df = df[["i", "j", "sadness", "happiness"]]
print(df)
# print(df.sort_values(by = ["i", "j"]))