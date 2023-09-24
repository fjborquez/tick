from pyradios import RadioBrowser

from discoverable import Discoverable


class DiscovererByAlias(Discoverable):
    def discover(self, a_word, api_client: RadioBrowser):
        # TODO Buscar la radio que tenga el alias en la lista de guardados
        pass
