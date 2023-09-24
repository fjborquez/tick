import json


class Station:
    def __init__(self, alias: str, uuid: str, name: str, url: str):
        self.alias = alias
        self.uuid = uuid
        self.name = name
        self.url = url

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __eq__(self, other):
        if isinstance(other, Station):
            return self.alias == other.alias and self.uuid == other.uuid and self.name == other.name \
                and self.url == other.url

        return False
