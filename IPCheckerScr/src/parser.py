import codecs
import argparse
from banner import baner
from getCategories import get_categories
import json
import csv
import re
import os
import requests
import ipaddress
import time
import pathlib

parser = argparse.ArgumentParser(description=baner())
required = parser.add_argument_group('required arguments')

#Required 
required.add_argument("-f", "--file",help = "Parse IP address from a given file",action = "store", required = True,)
required.add_argument("-d", "--days", help = "Number of days to look back for alerts",action = "store", required = False,)
    
    
#Outputs
parser.add_argument("-j", "--json", help="outputs items in json format",  action="store_true")
parser.add_argument("-jl", "--jsonl", help="outputs items in json format",  action="store_true")
parser.add_argument("-t", "--tsv", help="outputs items in tab separated values", action="store_true")
parser.add_argument("-c", "--csv", help="outputs items in comma separated values", action="store_true")

args = parser.parse_args()


def check_ip(ip,days):
    try:
        if ipaddress.ip_network(ip, False).is_private is False:
                headers = {
                'Accept': 'application/json',
                'Key': API_KEY
            }
        
                querystring = {
                'ipAddress': ip,
                'maxAgeInDays': days
                }

                url = f"https://api.abuseipdb.com/api/v2/check"
            
                r = requests.request(method='GET', url=url, headers=headers, params=querystring)
                response = r.json()
                
                if 'errors' in response:
                    print(f"Error: {response['errors'][0]['detail']}")
                    exit(1)               
                if response['data']['totalReports'] > 0:             
                    return response['data']
        else:
            return (f"{ip} is private. No Resuls")
    except:
        pass

def check_file(file_f,day):
    logs = []
    dump = []
    regex = r'(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))' 
    #regex = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    time.sleep(1)
    if args.file:
        file_f = get_file(args.file)
        matches = re.finditer(regex, file_f, re.MULTILINE)
        [dump.append(match.group())for _ , match in enumerate(matches, start=1)]
        dump = set(dump)
    for match in dump:
        logs.append(check_ip(match,day))
    return logs


def get_report(logs):
    if logs:
        if args.csv:
            try:
                keys = logs[0].keys()
            except KeyError:
                keys = logs.keys()
           
            with open('report.csv', 'w') as file:
                writer = csv.DictWriter(file, keys, quoting=csv.QUOTE_ALL)
                writer.writeheader()
                writer.writerows(logs)
                print("Report was safe")
        elif args.tsv:
            keys = logs[0].keys()
            with open('report.tsv', 'w') as file:
                    writer = csv.DictWriter(file, keys, delimiter='\t')
                    writer.writeheader()
                    writer.writerows(logs)
                    print("Report was safe")
        elif args.json:
            with open('report.json', 'w') as file:
                json.dump(logs, file,sort_keys=True, indent=4)
                print("Report was safe")
        elif args.jsonl:
            with open('report.json', 'w') as file:
                for i in logs:
                    json.dump(i, file)
                    file.write('\n')
                print("Report was safe")    
        else:
            print(json.dumps(logs, indent=4, sort_keys=True))


def create_file(filename, key):
    filecreate = open(filename, mode="w+")
    filecreate.write(key)
    filecreate.close()

def get_file(infile):
    with codecs.open(infile, "r", encoding='utf-8', errors='ignore') as filetoget:
        return filetoget.read()

if __name__ == '__main__':
      
    api_key_check = os.path.dirname(os.path.realpath(__file__)) + "\\"
    scripfile = api_key_check + "api_key.api"
    if os.path.exists(scripfile):

        if os.stat(scripfile).st_size == 0:
            my_key = input("Please endter your API key: ")
            create_file(scripfile, str(my_key))
            exit(1)
        with open(scripfile) as f:
            line = f.readline()
        API_KEY = line
    else:
        print("No API_KEY file exist. The file will be created...")
        try:
            my_key = input("Please endter your API key: ")
            create_file(scripfile, str(my_key))
        except FileExistsError:
            pass
            exit(1)
    
    if args.days:
        days = args.days
    else:
        days = 30
    if args.file:
        get_report(check_file(args.file,days))