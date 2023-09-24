from pyradios import RadioBrowser

from discoverable import Discoverable


class DiscovererByLanguage(Discoverable):
    def discover(self, a_word, api_client: RadioBrowser):
        return api_client.search(language=a_word)
