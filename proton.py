#test
from urllib.request import urlopen
import json
import pandas as pd
url = "https://api.protonmail.ch/vpn/logicals"
response = urlopen(url)
data_json = json.loads(response.read())


proton_ip_list = []

for i in data_json['LogicalServers']:
    for j in i['Servers']:
        proton_ip_list.append(j['EntryIP'])

        proton_ip_list.append(j['ExitIP'])

duplicates_removed = [*set(proton_ip_list)]
duplicates_removed.sort()
df = pd.DataFrame(duplicates_removed)
df.to_csv('protonvpn.csv',  index=False,   header=['PROTON_IP'])
