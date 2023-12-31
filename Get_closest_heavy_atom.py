def read_pdb_file(filename : str) -> dict:
    # function purpose: read all the heavy atom coordinate from pdb file
    heavy_atom = dict()
    res_id = None
    each_res = list()
    with open(filename, 'r') as f:
        for line in f:
            if line:
                m = line.split()
                if m[0] == "ATOM":
                    # filter out hydrogen atoms
                    if m[2][0] != 'H':
                        coordinate = [float(m[6]), float(m[7]), float(m[8])]
                        if res_id == None:
                            res_id = int(m[5])
                            each_res.append(coordinate)
                        else:
                            if int(m[5]) == res_id:
                                each_res.append(coordinate)
                            else:
                                heavy_atom[res_id] = each_res
                                each_res = list()
                                res_id = int(m[5])
                                each_res.append(coordinate)
    heavy_atom[res_id] = each_res                            
    return heavy_atom


def cal_distance(list1 : list, list2 : list) -> float:
    x1, y1, z1 = list1
    x2, y2, z2 = list2
    distance = ((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)**0.5
    return distance


def cal_min_distance(res1 : list, res2 : list) -> float:
    min_distance = None
    for i in res1:
        for j in res2:
            if min_distance == None:
                min_distance = cal_distance(i, j)
            else:
                min_distance = min(min_distance, cal_distance(i, j))
  
    return min_distance
    


if __name__ == "__main__":
    heavy_atom = read_pdb_file("assemble_11313233.pdb")
    print(f"There are {len(heavy_atom.keys())} residues")
    
    cutoff = 5
    fit_cutoff_pair = set()
    for i in heavy_atom.keys():
        for j in heavy_atom.keys():
            if i != j:
                if cal_min_distance(heavy_atom[i], heavy_atom[j]) < cutoff:
                    fit_cutoff_pair.add((min(i, j), max(i, j)))

    print(f"There are {len(fit_cutoff_pair)} pairs that fit cutoff.")
    temp_list = list(fit_cutoff_pair)
    temp_list.sort(key = lambda K : K[0])

    print(temp_list)            










