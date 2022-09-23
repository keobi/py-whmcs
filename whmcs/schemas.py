from marshmallow import Schema, fields, EXCLUDE
from fields import *


__all__ = [
    "DomainSchema", "DomainListSchema", "DomainUpdateResponseSchema",
]


class DomainSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(
        load_only=True
    )
    domainid = fields.Int(
        dump_only=True
    )
    domain = fields.Str(
        data_key="domainname"
    )
    registrar = fields.Str()
    registration_years = fields.Int(
        data_key="regperiod"
    )
    registration_date = WHMCSDate(
        format="%Y-%m-%d",
        data_key="regdate"
    )
    expiration_date = WHMCSDate(
        format="%Y-%m-%d",
        data_key="expirydate"
    )
    next_due_date = WHMCSDate(
        format="%Y-%m-%d",
        data_key="nextduedate"
    )
    status = fields.Str()
    has_dns_management = StrBool(
        data_key="dnsmanagement"
    )
    has_email_forwarding = StrBool(
        data_key="emailforwarding"
    )
    has_id_protection = StrBool(
        data_key="idprotection"
    )
    do_not_renew = StrBool(
        data_key="donotrenew"
    )


class DomainListSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    count = fields.Int(
        data_key="numreturned"
    )
    total = fields.Int(
        data_key="totalresults"
    )
    domains = NestedDomainField(
        fields.Nested(DomainSchema())
    )


class DomainUpdateResponseSchema(Schema):
    successful = SuccessField(
        data_key="result"
    )
    id = fields.Int(
        data_key="domainid"
    )
