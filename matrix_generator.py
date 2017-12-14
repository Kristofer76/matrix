import random
import csv

N = 3


def generate_matrix(matrix_file):
    with open(matrix_file, 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for i in range(0, N):
            row = []
            for j in range(0, N):
                row.append(random.randint(0, 9))
            writer.writerow(row)

generate_matrix("a.csv")
generate_matrix("b.csv")
