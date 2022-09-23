import datetime
import urllib.parse
import requests
from .endpoints import *


class WHMCSAPIClient(object):
    def __init__(self, domain, api_key, api_secret, response_type=None):
        self.url = f"{domain}/includes/api.php"
        
        self.api_key = api_key
        self.api_secret = api_secret 
        self.response_type = response_type or "json"

        self.endpoints = {
            "get_domains": GetClientsDomainsEndpoint(),
            "update_domain": UpdateClientDomainEndpoint(),
        }

    def __getattr__(self, key):
        if key not in self.endpoints:
            raise AttributeError(f"Endpoint not found: {key}")

        self.endpoint = self.endpoints[key]

        return self

    def __call__(self, *args, **kwargs):
        self.endpoint.load(*args, **kwargs)

        payload = self.execute()

        return self.endpoint._process_response(payload)

    def get_url(self):
        params = {}

        endpoint_params = self.endpoint.get_url_params()

        if endpoint_params:
            params.update(
                endpoint_params
            )

        for key in params.keys():
            params[key] = urllib.parse.quote(params[key])

        url = f"{self.url}{self.endpoint.get_url()}"

        if params:
            url += f"?{'&'.join(f'{k}={v}' for k, v in params.items())}"

        return url
        
    def execute(self):
        method = self.endpoint.get_method()

        kwargs = {
            "url": self.get_url()
        }

        data = {
            "username": self.api_key,
            "password": self.api_secret,
            "responsetype": self.response_type,
            "action": self.endpoint.action
        }

        data.update(
            self.endpoint.get_request_data() or dict()
        )

        if len(data):
            kwargs["json" if self.endpoint.is_request_data_json else "data"] = data
        
        print(f"Making {method.upper()} call to {kwargs['url']}")

        r = getattr(requests, method.lower())(
            **kwargs
        )

        return r.json()
    
    # def get_domains(self, domain=None, domain_id=None, client_id=None):
    #     data = {}
    #
    #     if domain:
    #         data["domain"] = domain
    #
    #     if domain_id:
    #         data["domainid"] = int(domain_id)
    #
    #     if client_id:
    #         data["clientid"] = int(client_id)
    #
    #     payload = self.execute("GetClientsDomains", **data)
    #
    #     print(f"Request returned {payload['totalresults']} domains")
    #
    #     for domain in payload["domains"]["domain"]:
    #         yield Domain(**domain)
    #
    # def get_domain(self, domain=None, domain_id=None, client_id=None):
    #     if not domain and not domain_id and not client_id:
    #         raise KeyError("Must pass domain, domain_id, or client_id")
    #
    #     return list(self.get_domain(domain, domain_id, client_id))[0]
    #
    # def update_domain(self, domain_id, **data):
    #     data.update({
    #         "domainid": domain_id
    #     })
    #
    #     payload = self.execute(
    #         "UpdateClientDomain",
    #         **data
    #     )
    #
    #     if payload.get("result") != "success":
    #         print(f"[!!] {payload}")
    #         return False
    #
    #     return True
