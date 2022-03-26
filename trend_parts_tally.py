def trend_tally_parts():

    with open('db/parts_tally', 'r') as f:
        data = f.readlines()
        l = []
        for line in data:
            parsed = line.split(',')
            l.append([parsed[0],parsed[1].replace('\n','')])
        d = {x[0]:int(x[1]) for x in l}

    with open('db/axie_details', 'r') as f:
        data = f.readlines()
        for line in data:
            c = line.replace('\n','')
            n = c.split(',')

            for ns in n:
                if ns in d:
                    d[ns] += 1


    ordered_parts = {k: v for k, v in sorted(d.items(), key=lambda item: item[1],reverse=True)}             

    with open('db/parts_tally', 'w') as f:
        my_str = ""
        for values in ordered_parts:
            my_str += f"{values},{ordered_parts[values]}\n"
        f.write(my_str)

if __name__ == "__main__":
    trend_tally_parts()