import json


class Payload:
    def __init__(self, func, parameters):
        self.func = func
        self.parameter = parameters

    @property
    def payload(self):
        return {
            'm': self.func,
            'p': self.parameter
        }

    @property
    def payload_len(self):
        return len(self.set_payload)

    @property
    def set_payload(self):
        return json.dumps(self.payload, separators=(",", ":"))

    @property
    def _set_payload_header(self):
        return "~m~" + str(self.payload_len) + "~m~"

    def get_payload(self):
        return self._set_payload_header + self.set_payload

    def __len__(self): return self.payload_len
