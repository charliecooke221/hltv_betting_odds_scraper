import csv
import sys


def get_existing_data(csv_file, col_num):
    # Add the values in colNum in csvFile to an array
    array = []
    print(f"Reading data from {csv_file}.csv.")
    with open(f"csv/{csv_file}.csv", encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            array.append(row[col_num])
    return array