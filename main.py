import os
import requests
from dotenv import load_dotenv
from tdns_helper import tdns_api
load_dotenv()

TDNS_API_KEY=os.getenv('tdns_api_key')
TDNS_URL=os.getenv('tdns_url')
FORTIGATE_API_KEY=os.getenv('fortigate_api_key')
FORTIGATE_URL=os.getenv('fortigate_url')

def main():
    tdns = tdns_api(api_key=TDNS_API_KEY, api_url=TDNS_URL)
    scopes = tdns.get_dhcp_scopes()

    main_scope = None
    for scope in scopes:
        if scope.get('networkAddress') == '10.1.2.0':
            main_scope = scope

    reserved_leases = tdns.get_dhcp_scope(main_scope['name'])['reservedLeases']
    ...

if __name__ == '__main__':
    main()
