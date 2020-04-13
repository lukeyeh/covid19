import re
from bs4 import BeautifulSoup
import requests

URL = "https://www.amherstma.gov/3519/"
CASESTRINGS = ['Amherst Total Cases', 'Hampshire County Cases', 'Massachusetts']

def get_num_cases(soup, case_string):
    case_html = soup.find('span', string=re.compile("{}:(.*)".format(case_string)))
    cases = re.findall(r'\d+', case_html.text)[0]
    return cases

def find_cases(soup): 
    return {case_string.split(' ')[0] : get_num_cases(soup, case_string) 
            for case_string in CASESTRINGS}

if __name__ == '__main__':
    req = requests.get(URL)
    soup = BeautifulSoup(req.text, "html.parser")
    print(find_cases(soup))
