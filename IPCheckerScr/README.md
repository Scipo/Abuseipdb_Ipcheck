# IPchecker

Ipchecker is a Python script for checking if an IP address is malicious or not. 

The script uses AbuseIPDB api and registration on [AbuseIPDB](https://www.abuseipdb.com/) is required.

## Installation

The run the script from src directory.

```bash
python parser.py -f <file location>
```
## Help
  
```bash
python parser.py -h
```
It will list all available options 
 
## Examples

```python
# default output does not generate a report. It returns the output in the console in json format.
python parser.py -f <file location>
 
# return report in .csv file 
python parser.py -f <file location> -c 

# returns report in .json file
python parser.py -f <file location> -j

# Number of days can be set from 1 to 365. The default option is set to 30 days. 
python parser.py -f <file location> -j -d <number of days>
```
