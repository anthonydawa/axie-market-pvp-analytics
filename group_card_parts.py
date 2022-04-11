import json
from re import L
 

def getClassParts(classes):

    f = open('C:/Users/antho/Desktop/breed-bot/db/parts.json')

    data = json.load(f)

    l = []

    for cls in classes:

        for parts in data:
            if cls == data[parts]['class'] and data[parts]['specialGenes'] == "":
                l.append(data[parts]['partId'])
   
    f.close()

    return l 

def getClassEyeEars(arr):

    f = open('C:/Users/antho/Desktop/breed-bot/db/parts.json')

    data = json.load(f)

    eyes_ears = []


    for part in arr:
        if data[part]['type'] == 'eyes':
            eyes_ears.append(part)
        if data[part]['type'] == 'ears':
            eyes_ears.append(part)

    f.close()

    return eyes_ears



if __name__ == "__main__": 
    print(getClassEyeEars(getClassParts(['aquatic','beast'])))
    