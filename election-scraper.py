"""
projekt_3.py: treti projekt do Engeto Online Python Akademie
autor:Charles Kinyonge Kakese
email: kkakese2@yahoo.com
discord: Charles#4490
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

def get_data():
    r = requests.get(sys.argv[1])
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def get_cod(r):
    codes = []
    links = []
    lines = r.find_all("a")
    for line in lines:
        if line.text.isnumeric() and len(line.text) == 6:
            codes.append(line.text)
            links.append("https://www.volby.cz/pls/ps2017nss/" + line["href"])
    return codes, links

def build_header(line):
    head = ["code", "location", "registered", "valid"]
    r = requests.get(line)
    parsing = BeautifulSoup(r.text, "html.parser")
    for entity in parsing.find_all("td")[10::5]:
        if entity.text != "-":
            head.append(entity.text)
    return head

def ground_integrity(gr_line, gr_cod):
    ground_integrit = [gr_cod]
    gr_data_r = requests.get(gr_line)
    gr_data_soup = BeautifulSoup(gr_data_r.text, "html.parser")
    ground_integrit.append("".join(str(gr_data_soup.find_all("h3")[2].text).split(":")[1].strip()))
    ground_integrit.append("".join(str(gr_data_soup.find_all("td")[3].text).split()))
    ground_integrit.append("".join(str(gr_data_soup.find_all("td")[4].text).split()))
    ground_integrit.append("".join(str(gr_data_soup.find_all("td")[7].text).split()))
    for karl in gr_data_soup.find_all("td")[11::5]:
        ground_integrit.append(karl.text)
    return ground_integrit

def file_csv():
    data = get_data()
    print("I am downloading data from the address", sys.argv[1])
    codes, links = get_cod(data)
    header = build_header(links[0])
    with open(sys.argv[2] + ".csv", "w", newline="") as file:
        print("Export to", file.name)
        file_writer = csv.writer(file, delimiter=";")
        file_writer.writerow(header)
        for c in range(len(codes)):
            file_writer.writerow(ground_integrity(links[c], codes[c]))
    print("finished.")

file_csv()





