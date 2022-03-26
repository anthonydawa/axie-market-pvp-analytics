import json
 
# Opening JSON file
f = open('part.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
x = []
for i in data:
    if data[i]['specialGenes'] == "":
        x.append(i)
print(len(x))
 
# Closing file
f.close()


with open('db/parts', 'w') as f:
    my_str = ','.join(x)
    f.write(my_str)