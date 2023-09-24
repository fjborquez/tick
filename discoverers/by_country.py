from pyradios import RadioBrowser

from discoverable import Discoverable


class DiscovererByCountry(Discoverable):
    def discover(self, a_word, api_client: RadioBrowser):
        return api_client.search(countrycode=a_word)

