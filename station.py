import json


class Station:
    def __init__(self, alias: str, uuid: str, name: str, url: str):
        self.alias = alias
        self.uuid = uuid
        self.name = name
        self.url = url

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)