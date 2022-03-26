


def tally_parts():

    with open('db/parts_tally', 'r') as f:
        data = f.readlines()
        l = []
        for line in data:
            parsed = line.split(',')
            l.append([parsed[0],parsed[1].replace('\n','')])
        d = {x[0]:x[1] for x in l}

    with open('db/axie_details', 'r') as f:
        data = f.readlines()
        for line in data:
            c = line.replace('\n','')
            n = c.split(',')
        nd = 
            