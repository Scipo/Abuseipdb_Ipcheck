import requests

class AbuseIP(object):
    CATEGORIS= {
        '1' :  'DNS Compromise', 
        '2':  'DNS Poisoning', 
        '3':  'Fraud Orders', 
        '4':  'DDoS Attack', 
        '5':  'FTP Brute-Force',
        '6':  'Ping of Death', 
        '7':  'Phishing', 
        '8':  'Fraud VoIP',
        '9':  'Open Proxy', 
        '10': 'Web Spam', 
        '11': 'Email Spam',
        '12': 'Blog Spam', 
        '13': 'VPN IP',  
        '14': 'Port Scan',
        '15': 'Hacking',
        '16': 'SQL Injection', 
        '17': 'Spoofing', 
        '18': 'Brute-Force', 
        '19': 'Bad Web Bot', 
        '20': 'Exploited Host', 
        '21': 'Web App Attack', 
        '22': 'SSH', 
        '23': 'IoT Targeted', 
        
    }
    class Default(object):
        confidance_minimum = 100
        LIMIT = 1000
        DEFAULT_DAYS = 30

    def __init__(self, api_key, subscriber = False) -> None:
        if not api_key:
            raise ValueError("API Key is missing!")
        self._api_key = api_key
        self._ubscriber = subscriber
    
    def _get_responce(self, endpoint, query):
        Base_url = f"https://api.abuseipdb.com/api/v2/{endpoint}"
        Known_endpoints = {       
            'check': 'GET',
        }
        if endpoint not in Known_endpoints.keys():
            msg = 'Unkown endpoint "{}"'
            raise NotImplementedError(msg.format(endpoint))
        headers = {
                'Accept': 'application/json',
                'Key': self._api_key
            }
        response = requests.request(method=Known_endpoints[endpoint], url=Base_url.format(endpoint=endpoint), headers=headers, params=query)
        if response.status_code == 422 or  response.status_code == 429:
            return response.json()['errors']
        response.raise_for_status()
        return response.json()['data']
    
    def check(self, ip_addresses, days=None):
        query ={
            'ipAddress': ip_addresses,
            'maxAgeInDays': str(days or self.Default.DEFAULT_DAYS),
        }
        return self._get_responce('chek',query)
    
    def report(self, ip_addresses, categories):
        query = {
            'ip' : ip_addresses,
            'categories' : categories,
        }
        return self._get_responce('report', query)        