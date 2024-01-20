import json
import csv

import ijson
import csv


def convert_json(file_path):
    did_write_headers = False
    headers = []
    row = []

    iterable_json = ijson.parse(open(file_path, 'r'))

    with open(file_path + '.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file, 
                                delimiter= ',',
                                quotechar= '"',
                                quoting= csv.QUOTE_MINIMAL)

        for prefix, event, value in iterable_json:
            if event == 'end_map':
                if not did_write_headers:
                    csv_writer.writerow(headers)
                did_write_headers = True
                csv_writer.writerow(row)
                row = []
            if event == 'map_key' and not did_write_headers:
                headers.append(value)
            if event == 'string':
                row.append(value)
file_path='./docs/dev.jsonl'
convert_json(file_path) 
'''
with open('./docs/dev.jsonl', 'r') as json_file:
    json_list = list(json_file)

for json_str in json_list:
    jsondata = json.loads(json_str)


data_file = open('output.csv', 'w', newline='')
csv_writer = csv.writer(data_file)
 
count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
 
data_file.close()
'''

def export_to_csv():
    with open("docs/dev.jsonl") as f:
        list1 =[]
        data = json.loads(f.read())
        temp = data[0]
        header_items =[]
        get_header_items(header_items, temp)
        list1.append(header_items)

        for obj in data:
            d=[]
            add_items_to_data(d,obj)
            list1.append(d)
        with open('output.csv','w') as output_file:
            for a in list1:
                output_file.write(','.join(map(str,a))+"\r")

def get_header_items(items,obj):
    for x in obj:
        if isinstance(obj[x], dict):
            items.append(x)
            get_header_items(items,obj[x])
        else:
            items.append(x)

def add_items_to_data(items,obj):
    for x in obj:
        if isinstance(obj[x], dict):
            items.append("")
            add_items_to_data(items,obj[x])
        else:
            items.append(obj[x])
# export_to_csv()           