import pandas as pd
import pprint
import json
import sys
import pprint
import os.path
import os

from docx.api import Document
from docx.api import Document
from os import path

CATEGORIES = ['county', 'sex', 'age_group', 'deaths', 'long_term_care', 'hospitalization', 'labs']


def parse_table(table):
    ndata = []
    keys = None
    data_cat = []
    data = []
    num_table = 0
    for i, row in enumerate(table.rows):
        text = (cell.text for cell in row.cells)
        if i == 0:
            keys = tuple(text)
            continue
        row_data = dict(zip(keys, text))

        if list(row_data.values())[0] == list(row_data.values())[1] or i == len(table.rows)-1:
            data_cat.append(pd.DataFrame(ndata))
            ndata = []
            num_table += 1
        else:
            ndata.append(row_data)

        data.append(row_data)

    return data_cat


def process_data(document_name, save=False):
    document = Document(document_name)
    tables = document.tables
    del tables[1]
    data = []
    for table in tables:
        data.extend(parse_table(table))

    del data[0]
    data_dict = {CATEGORIES[i]: table for i, table in enumerate(data)}

    if save:
        save_dict(document_name, data_dict)

    return data_dict

def save_dict(document_name, data_dict):
    for table_name, table in data_dict.items():
        directory_to_save = "data/" + strip_file_extension(document_name)
        if not path.exists(directory_to_save):
            os.mkdir(directory_to_save)

        table.to_csv(
            'data/{}/{}.csv'.format(document_name.split('.')[0], table_name), index=True)

def strip_file_extension(file_name):
    return file_name.split('.')[0]


if __name__ == '__main__':
    print(len(CATEGORIES))
    input_document = sys.argv[1]

    final_data_dict = process_data(input_document, save=True)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(final_data_dict)
