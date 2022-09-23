from .schemas import *
from .exceptions import *


__all__ = [
    "GetClientsDomainsEndpoint", "UpdateClientDomainEndpoint",
]


class EndpointBase(object):
    url = None
    request_schema_class = None
    response_schema_class = None
    required_params = list()
    required_data = list()
    data_mapping = dict()
    method = "POST"
    url_params = None
    request_data = None
    is_request_data_json = False
    action = None

    def load(self, *args, **kwargs):
        for required_param in self.required_params:
            if required_param in self.url_params:
                continue
            raise MissingRequiredParameter("url_params", required_param)

        for required_param in self.required_data:
            if required_param in self.request_data:
                continue
            raise MissingRequiredParameter("request_data", required_param)

    def get_url(self):
        return self.url or ""

    def get_method(self):
        return self.method

    def get_url_params(self):
        return self.url_params

    def get_request_data(self):
        return self.request_data

    def get_response_schema(self, *args, **kwargs):
        if not self.response_schema_class:
            return

        return self.response_schema_class(*args, **kwargs)

    def get_request_schema(self, *args, **kwargs):
        if not self.request_schema_class:
            return

        return self.request_schema_class(*args, **kwargs)

    def get_data_mapping(self):
        if not self.data_mapping:
            self.data_mapping = {}

        self.data_mapping.update({
            "start": ("limitstart", int),
            "limit": ("limitnum", int),
        })

        return self.data_mapping

    def process_response(self, payload):
        return payload

    def _process_response(self, payload):
        if not self.get_response_schema():
            return self.process_response(payload)
        else:
            return self.get_response_schema().load(payload)


class GetClientsDomainsEndpoint(EndpointBase):
    action = "GetClientsDomains"
    response_schema_class = DomainListSchema
    data_mapping = {
        "domain": (None, str),
        "domain_id": ("domainid", int),
        "client_id": ("clientid", int),
    }

    def load(self, *args, **kwargs):
        if len(args):
            raise AttributeError("Data must be passed as keywords")

        for key, value in self.get_data_mapping().items():
            request_name, data_type = value

            if key not in kwargs:
                continue

            if not request_name:
                request_name = key

            if not self.request_data:
                self.request_data = {}

            self.request_data[request_name] = data_type(kwargs[key])

        super().load(*args, **kwargs)


class UpdateClientDomainEndpoint(EndpointBase):
    action = "UpdateClientDomain"
    request_schema_class = DomainSchema
    response_schema_class = DomainUpdateResponseSchema
    required_data = [
        "domainid"
    ]

    def load(self, *args, **kwargs):
        kwargs["domainid"] = kwargs["id"]
        self.request_data = self.get_request_schema().dump(kwargs)

        print(self.request_data)

        super().load(*args, **kwargs)
