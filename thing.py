import subprocess
import csv
from parse_doc import process_data
from datetime import datetime, timedelta
import os
import pandas as pd
from tabulate import tabulate


COUNTIES = {
    "Barnstable": 0,
    "Berkshire": 1,
    "Bristol": 2,
    "Dukes": 3,
    "Essex": 4,
    "Franklin": 5,
    "Hampden": 6,
    "Hampshire": 7,
    "Middlesex": 8,
    "Nantucket": 9,
    "Norfolk": 10,
    "Plymouth": 11,
    "Suffolk": 12,
    "Worcester": 13,
    "Unknown": 14,
}


def today():
    return datetime.today().strftime('%Y-%m-%d')


def yesterday():
    return (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')


def get_total_cases_by_day(day):
    today_county_file = "data/{}/county.csv".format(day)
    today_county_df = pd.read_csv(today_county_file)

    return today_county_df['NUMBER OF CONFIRMED CASES'].sum()


def get_cases_diffs(day1, day2):
    deaths_day1 = get_total_cases_by_day(day1)
    deaths_day2 = get_total_cases_by_day(day2)

    return abs(deaths_day1 - deaths_day2)


def get_cases_by_county_by_day(county, day):
    today_county_file = "data/{}/county.csv".format(day)
    today_county_df = pd.read_csv(today_county_file)

    return today_county_df.at[county, 'NUMBER OF CONFIRMED CASES']


def get_total_deaths_by_day(day):
    today_county_file = "data/{}/deaths.csv".format(day)
    today_county_df = pd.read_csv(today_county_file)

    return today_county_df.at[0, 'NUMBER OF CONFIRMED CASES']


def get_deaths_diffs(day1, day2):
    deaths_day1 = get_total_deaths_by_day(day1)
    deaths_day2 = get_total_deaths_by_day(day2)

    return abs(deaths_day1 - deaths_day2)

def daily_digest():
    total_cases = get_total_cases_by_day(today())
    total_deaths = get_total_deaths_by_day(today())
    num_of_new_cases = get_cases_diffs(today(), yesterday())
    num_of_new_deaths = get_deaths_diffs(today(), yesterday())

    return "TOTAL CASES: {}, TOTAL DEATHS: {}, NUMBER OF NEW CASES: {} NUMBER OF NEW DEATHS: {}".format(
        total_cases, total_deaths, num_of_new_cases, num_of_new_deaths)

def all_tables():
    table_output = ""
    directory = 'data/' + today()
    for filename in os.listdir(directory):
        if filename.split('.')[-1] == "csv":
            data_name = 'data/{}/{}'.format(today(), filename)
            with open(data_name, 'r') as csv_file:
                table = list(csv.reader(csv_file, delimiter=','))
                table_form = tabulate(table, tablefmt='github', headers='firstrow')
                table_output += "# " + filename + '\n' + table_form + '\n'

    return table_output

if __name__ == '__main__':
    rc = subprocess.call("./download.sh", shell=True)
    process_data(today() + ".docx", save=True)

    print(daily_digest())
    print(all_tables())

