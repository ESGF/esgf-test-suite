import requests

server_base = "https://esgf-dev1.llnl.gov/"

mod_lst = ["esg-orp", "esgf-nm", "esgf-idp", "esg-search/search"]

resp = requests.get(server_base)

print "COG", resp.status_code

for n in mod_lst:
    
    resp = requests.get(server_base + n + '/')

    print n, resp.status_code




    

