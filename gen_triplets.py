if __name__ == "__main__":
    filename = 'data/pairs.txt'
    with open(filename, 'r') as file:
        lines = file.readlines()

    pairs = []
    used = set()
    for i in range(1, len(lines)):
        line = lines[i]
        tokens = line.split()
        if len(tokens) == 3:
            name = tokens[0]
            id1 = int(tokens[1])
            id2 = int(tokens[2])
            pairs.append({'name1': name, 'id1': id1, 'name2': name, 'id2': id2, 'same_person': True})
        elif len(tokens) == 4:
            name1 = tokens[0]
            id1 = int(tokens[1])
            name2 = tokens[2]
            id2 = int(tokens[3])
            pairs.append({'name1': name1, 'id1': id1, 'name2': name2, 'id2': id2, 'same_person': False})

    triplets_raw = []
    same = [p for p in pairs if p['same_person']]
    not_same = [p for p in pairs if not p['same_person']]
    for p in same:
        a_name = p['name1']
        a_id = p['id1']
        p_name = p['name2']
        p_id = p['id2']
        left_match = [np for np in not_same if
                      np['name1'] == a_name and np['id1'] == a_id and np['name1'] not in used and np[
                          'name2'] not in used]
        if len(left_match) > 0:
            np = left_match[0]
            used.add(a_name)
            used.add(p_name)
            used.add(np['name1'])
            used.add(np['name2'])
            triplets_raw.append(
                {'a_name': a_name, 'a_id': a_id, 'p_name': p_name, 'p_id': p_id, 'n_name': np['name2'],
                 'n_id': np['id2']})
            continue

        right_match = [np for np in not_same if
                       np['name2'] == a_name and np['id2'] == a_id and np['name1'] not in used and np[
                           'name2'] not in used]
        if len(right_match) > 0:
            np = right_match[0]
            used.add(a_name)
            used.add(p_name)
            used.add(np['name1'])
            used.add(np['name2'])
            triplets_raw.append(
                {'a_name': a_name, 'a_id': a_id, 'p_name': p_name, 'p_id': p_id, 'n_name': np['name1'],
                 'n_id': np['id1']})
            continue

        a_name = p['name2']
        a_id = p['id2']
        p_name = p['name1']
        p_id = p['id1']
        left_match = [np for np in not_same if
                      np['name1'] == a_name and np['id1'] == a_id and np['name1'] not in used and np[
                          'name2'] not in used]
        if len(left_match) > 0:
            np = left_match[0]
            used.add(a_name)
            used.add(p_name)
            used.add(np['name1'])
            used.add(np['name2'])
            triplets_raw.append(
                {'a_name': a_name, 'a_id': a_id, 'p_name': p_name, 'p_id': p_id, 'n_name': np['name2'],
                 'n_id': np['id2']})
            continue

        right_match = [np for np in not_same if
                       np['name2'] == a_name and np['id2'] == a_id and np['name1'] not in used and np[
                           'name2'] not in used]
        if len(right_match) > 0:
            np = right_match[0]
            used.add(a_name)
            used.add(p_name)
            used.add(np['name1'])
            used.add(np['name2'])
            triplets_raw.append(
                {'a_name': a_name, 'a_id': a_id, 'p_name': p_name, 'p_id': p_id, 'n_name': np['name1'],
                 'n_id': np['id1']})
            continue

    remain_same = [p for p in pairs if p['same_person'] and p['name1'] not in used and p['name2'] not in used]
    remain_not_same = [p for p in pairs if not p['same_person'] and p['name1'] not in used and p['name2'] not in used]

    print('len(remain_same): ' + str(len(remain_same)))
    print('len(remain_not_same): ' + str(len(remain_not_same)))

    for p in remain_same:
        a_name = p['name1']
        a_id = p['id1']
        p_name = p['name2']
        p_id = p['id2']
        no_match_1 = [np for np in remain_not_same if np['name1'] != a_name and np['name1'] not in used]
        if len(no_match_1) > 0:
            np = no_match_1[0]
            used.add(a_name)
            used.add(p_name)
            used.add(np['name1'])
            triplets_raw.append(
                {'a_name': a_name, 'a_id': a_id, 'p_name': p_name, 'p_id': p_id, 'n_name': np['name1'],
                 'n_id': np['id1']})
            continue

        no_match_2 = [np for np in remain_not_same if np['name2'] != a_name and np['name2'] not in used]
        if len(no_match_2) > 0:
            np = no_match_2[0]
            used.add(a_name)
            used.add(p_name)
            used.add(np['name2'])
            triplets_raw.append(
                {'a_name': a_name, 'a_id': a_id, 'p_name': p_name, 'p_id': p_id, 'n_name': np['name2'],
                 'n_id': np['id2']})
            continue

    triplets = []
    for t in triplets_raw:
        a = '{0}/{0}_{1}.jpg'.format(t['a_name'], str(t['a_id']).zfill(4))
        p = '{0}/{0}_{1}.jpg'.format(t['p_name'], str(t['p_id']).zfill(4))
        n = '{0}/{0}_{1}.jpg'.format(t['n_name'], str(t['n_id']).zfill(4))
        triplets.append({'a': a, 'p': p, 'n': n})

    print('len(triplets): ' + str(len(triplets)))
    print(triplets)

    import json

    with open('lfw_val_triplets.json', 'w') as file:
        json.dump(triplets, file, indent=4)
