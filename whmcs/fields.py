from marshmallow import fields


__all__ = [
    "WHMCSDate", "NestedDomainField", "SuccessField", "StrBool",
]


class WHMCSDate(fields.Date):
    def _deserialize(self, value, attr, data, **kwargs):
        if value.startswith("0"):
            return None

        return super()._deserialize(value, attr, data, **kwargs)


class NestedDomainField(fields.List):
    def _deserialize(self, value, attr, data, **kwargs):
        value = value["domain"]
        return super()._deserialize(value, attr, data, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        value = super()._serialize(value, attr, obj, **kwargs)
        return {"domain": value}


class SuccessField(fields.Str):
    def _deserialize(self, value, attr, data, **kwargs):
        return value.lower() == "success"

    def _serialize(self, value, attr, obj, **kwargs):
        return "success" if value else "error"


class StrBool(fields.Bool):
    def _serialize(self, value, attr, obj, **kwargs):
        return str(int(value)) if value is not None else ""
