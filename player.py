import json
import os
from signal import SIGTERM
from subprocess import Popen

from pyradios import RadioBrowser

from discoverable import Discoverable
from station import Station


class Player:
    def __init__(self, api_client: RadioBrowser):
        self.stations = []
        self.status = None
        self.discoverer: Discoverable = None
        self.last_station: Station = None
        self.api_client = api_client
        self.process = None
        self.volume: int = 50

    def play(self, station: Station):
        self.process = Popen(
            ["ffplay", "-nodisp", "-nostats", "-loglevel", "0", "-volume", str(self.volume), station.url],
            shell=False,
        )
        self.last_station = station

    def stop(self):
        if self.process is not None:
            os.kill(self.process.pid, SIGTERM)

    def discover(self, a_word):
        stations = self.discoverer.discover(a_word, self.api_client)
        for station in stations:
            new_station = Station(name=station['name'], alias=station['name'], uuid=station['stationuuid'], url=station['url'])
            self.stations.append(new_station)

    def set_discoverer(self, discoverer: Discoverable):
        self.discoverer = discoverer

    def set_volume(self, volume: int):
        if volume < 0 or volume > 100:
            raise ValueError("Volume must be between 0 to 100")

        self.volume = volume

        if self.last_station:
            self.stop()
            self.play(self.last_station)

    def get_stations(self):
        return self.stations

    def add_station_to_favorites(self, station: Station):
        stations = self.read_favorites()

        if station in stations:
            raise ValueError("La radio ya está en la lista de favoritos")

        with open("db/favorites.db", "a+") as file:
            file.write(json.dumps(station.to_json()))
            file.write("\n")
            file.close()

    def read_favorites(self):
        with open("db/favorites.db", "r") as outfile:
            lines = outfile.readlines()
            favorites = []
            for line in lines:
                favorite = json.loads(line)
                favorite = json.loads(favorite)
                station = Station(name=favorite["name"], alias=favorite["name"], uuid=favorite["uuid"], url=favorite["url"])
                favorites.append(station)
            return favorites

    def remove_station_from_favorites(self, station: Station):
        stations = self.read_favorites()

        if station not in stations:
            raise ValueError("La radio no está en la lista de favoritos")

        stations.remove(station)

        with open("db/favorites.db", "w") as file:
            for to_add in stations:
                file.write(json.dumps(to_add.to_json()))
                file.write("\n")
            file.close()

