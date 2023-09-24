import time

import questionary
from pyradios import RadioBrowser
from questionary import Choice

from discoverable import Discoverable
from discoverers.by_country import DiscovererByCountry
from discoverers.by_language import DiscovererByLanguage
from discoverers.by_state import DiscovererByState
from discoverers.by_tag import DiscovererByTag
from player import Player
from station import Station


class App:
    def __init__(self):
        self.api_client = RadioBrowser()
        self.player = Player(api_client=self.api_client)
        self.stations = []

    def simulate(self):
        print(self.player.get_stations())
        discoverer: Discoverable = DiscovererByCountry()
        self.player.set_discoverer(discoverer)
        self.player.discover("GB")
        for station in self.player.get_stations():
            if station.uuid == "624aff3e-2de1-4dde-b98f-6c1e8964345e":
                selected_station = station
            print(station.name + " - (" + station.uuid + ") - " + station.url)
        self.player.play(selected_station)
        time.sleep(30)
        self.player.stop()

    def search_stations(self, discoverer: Discoverable, a_word: str):
        self.player.set_discoverer(discoverer)
        self.player.discover(a_word)
        self.stations = self.player.get_stations()

    def play(self, station: Station):
        self.player.play(station)

    def stop(self):
        self.player.stop()

    def get_stations(self):
        return self.player.get_stations()


def main():
    app = App()
    discoverer: Discoverable = None

    while True:
        selected = questionary.select(
            "¿Qué quieres hacer?",
            choices=["Buscar una radio", "Cambiar volumen", "Detener", "Salir"],
        ).ask()

        if selected == "Buscar una radio":
            buscar_selected = questionary.select(
                "Reproducir una radio",
                choices=["Reproducir una radio", "Ver favoritas"]
            ).ask()

            if buscar_selected == "Reproducir una radio":
                search_criteria = questionary.select(
                    "Reproducir una radio",
                    choices=["Por pais", "Por idioma", "Por etiqueta", "Por estado"]
                ).ask()

                search_keyword = questionary.text("La busqueda necesita una palabra clave").ask()

                if search_criteria == "Por pais":
                    discoverer = DiscovererByCountry()

                if search_criteria == "Por idioma":
                    discoverer = DiscovererByLanguage()

                if search_criteria == "Por estado":
                    discoverer = DiscovererByState()

                if search_criteria == "Por etiqueta":
                    discoverer = DiscovererByTag()

                app.search_stations(discoverer, search_keyword)
                stations = app.get_stations()
                stations_choices = create_choices_from_stations(stations)

                selected_station = questionary.select("Selecciona una radio para su reproduccion",
                                                      choices=stations_choices).ask()
                station_selected = questionary.select("Radio seleccionada",
                                                      choices=["Reproducir", "Guardar en favoritos"]).ask()
                if station_selected == "Reproducir":
                    app.play(selected_station)

                if station_selected == "Guardar en favoritos":
                    app.player.add_station_to_favorites(selected_station)

            if buscar_selected == "Ver favoritas":
                favorites = app.player.read_favorites()
                choices = create_choices_from_stations(favorites)
                selected_station = questionary.select("Selecciona una radio para su reproduccion", choices=choices).ask()
                station_selected = questionary.select("Radio seleccionada", choices=["Reproducir", "Quitar de favoritos"]).ask()

                if station_selected == "Reproducir":
                    app.play(selected_station)

                if station_selected == "Quitar de favoritos":
                    pass

        if selected == "Cambiar volumen":
            volume = questionary.text("Ingresa el nuevo volumen").ask()
            app.player.set_volume(int(volume))

        if selected == "Detener":
            app.stop()

        if selected == "Salir":
            app.stop()
            break


def create_choices_from_stations(stations):
    choices = []
    for station in stations:
        title = "name: " + station.name + " - uuid: " + station.uuid
        choices.append(Choice(title=title, value=station))

    return choices


if __name__ == "__main__":
    main()
