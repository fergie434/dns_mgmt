import requests
import os
from urllib.parse import urljoin

class tdns_api():
    api_key=''
    api_url=''
    
    def __init__(self, api_key, api_url):
        if not self.api_key:
            self.api_key = os.getenv('tdns_api_key')
        if not self.api_url:
            self.api_url = os.getenv('tdns_url')

    def get_dhcp_scopes(self):
        return self._get('/api/dhcp/scopes/list')['scopes']
    
    def get_dhcp_scope(self, scope_name):
        params = {'name': scope_name}
        return self._get('/api/dhcp/scopes/get', params)

    def _build_request_url(self, path, extra_params=None):
        req = requests.models.PreparedRequest()
        params = {'token': self.api_key}
        if extra_params:
            params = params | extra_params

        req.prepare_url(urljoin(self.api_url, path), params)
        return req.url

    def _get(self, api_path, extra_params=None):
        request_url = self._build_request_url(api_path, extra_params)
        response = requests.get(request_url)

        response.raise_for_status()
        return response.json().get("response", [])
