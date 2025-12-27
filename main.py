import os
from dotenv import load_dotenv
from tdns_helper import tdns_api
from fortigate_api import FortiGate, FortiGateAPI
from netaddr import EUI
load_dotenv()

TDNS_API_KEY=os.getenv('tdns_api_key')
TDNS_URL=os.getenv('tdns_url')
FORTIGATE_API_KEY=os.getenv('fortigate_api_key')
FORTIGATE_URL=os.getenv('fortigate_url')
DHCP_SEARCH_DOMAIN = os.getenv('dhcp_search_domain')
TDNS = tdns_api(api_key=TDNS_API_KEY, api_url=TDNS_URL)
FGT = FortiGateAPI(FORTIGATE_URL, token=FORTIGATE_API_KEY, verify=False)

def normalize_mac(mac):
    mac = EUI(mac)
    return str(mac)

def sync_tdns_to_fgt(tdns_reserved, fgt_reserved, fgt_dhcp_scope):
    tdns_mac_list = [normalize_mac(i['hardwareAddress']) for i in tdns_reserved]
    fgt_mac_list = [normalize_mac(i['mac']) for i in fgt_reserved]
    for tdns_lease in tdns_reserved:
        if normalize_mac(tdns_lease['hardwareAddress']) not in fgt_mac_list:
            print(f"Adding lease to FGT - {tdns_lease['address']}/{tdns_lease['hardwareAddress']}")
            dhcp_config = FGT.cmdb.system_dhcp.server.get(filter=f"id=={fgt_dhcp_scope['id']}")[0]
            lease = {
                'type': 'mac',
                'ip': tdns_lease['address'],
                'mac': tdns_lease['hardwareAddress'].replace('-',':'),
                'description': tdns_lease['comments']
            }
            dhcp_config['reserved-address'].append(lease)
            FGT.cmdb.system_dhcp.server.update(dhcp_config)

def main():
    scopes = TDNS.get_dhcp_scopes()

    # Get TDNS DHCP Scope
    tdns_main_scope = None
    for scope in scopes:
        scope_details = TDNS.get_dhcp_scope(scope['name'])
        if scope_details.get('domainName') == DHCP_SEARCH_DOMAIN:
            tdns_main_scope = scope

    tdns_main_scope = TDNS.get_dhcp_scope(tdns_main_scope['name'])
    tdns_reserved = tdns_main_scope['reservedLeases']

    # Get FGT DHCP Scope
    fgt_dhcp_servers = FGT.cmdb.system_dhcp.server.get()
    for server in fgt_dhcp_servers:
        if server['domain'] == DHCP_SEARCH_DOMAIN:
            fgt_dhcp_server = server

    sync_tdns_to_fgt(tdns_reserved, fgt_dhcp_server['reserved-address'], fgt_dhcp_server)

if __name__ == '__main__':
    main()
