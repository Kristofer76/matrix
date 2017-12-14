# -*- coding: utf-8 -*-
import mincemeat
import csv
import collections


def get_matrix(matrix_file):
    with open(matrix_file, 'rb') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    return your_list


def write_to_csv(a ,b, results):
    od = collections.OrderedDict(sorted(results.items()))

    firstRow = ["матрица", "строка", "столбец", "значение"]

    with open('matrix.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(firstRow)

        # write a
        for i in range(0, len(a)):
            for j in range(0, len(a)):
                writer.writerow(["a", i, j, a[i][j]])

        # write b
        for i in range(0, len(b)):
            for j in range(0, len(b)):
                writer.writerow(["b", i, j, b[i][j]])

        # write c
        for key, value in od.items():
            writer.writerow(["c", key[0], key[1], value])


def mapfn(k, v):
    if k == 0:
        for i in range(0, v['size']):
            for j in range(0, v['size']):
                for k in range(0, v['size']):
                    key = (i, k)
                    value = (j, int(v['matrix'][i][j]))
                    yield key, value

    else:
        for j in range(0, v['size']):
            for k in range(0, v['size']):
                for i in range(0, v['size']):
                    key = (i, k)
                    value = (j, int(v['matrix'][j][k]))
                    yield key, value


def reducefn(k, vs):
    tmp = {}
    result = 0

    for tupl in vs:
        if tupl[0] not in tmp.keys():
            tmp.update({tupl[0]: tupl[1]})
        else:
            tmp[tupl[0]] *= tupl[1]

    for elem in tmp.values():
        result += elem

    res = result % 97

    return res


a = get_matrix("a.csv")
b = get_matrix("b.csv")

data_dict = {0: {'size': len(a), 'matrix': a}, 1: {'size': len(b), 'matrix': b}}


s = mincemeat.Server()
s.datasource = data_dict
s.mapfn = mapfn
s.reducefn = reducefn

results = s.run_server(password="changeme")
write_to_csv(a, b, results)

