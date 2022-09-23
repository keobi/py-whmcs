class RequestError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
    
    def __str__(self):
        return f"[{self.code}] {self.message}"


class MissingRequiredParameter(Exception):
    def __init__(self, place, required_param):
        self.required_param = required_param
        self.place = place

    def __str__(self):
        return f"Missing required parameter in {self.place}: {self.required_param}"

