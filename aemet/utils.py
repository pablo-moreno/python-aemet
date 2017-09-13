import csv
import json
import os

def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r') as f:
        fields = f.readline().strip().split(',')
        reader = csv.reader(f)
        data = list(reader)
    array = [dict(zip(fields, element)) for element in data]
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(array, indent=4))

if __name__ == '__main__':
    csv_to_json(
        os.path.join('data', 'cod_costas.csv'),
        os.path.join('data', 'cod_costas.json'),
    )
