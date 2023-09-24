from pyradios import RadioBrowser

from discoverable import Discoverable


class DiscovererByState(Discoverable):
    def discover(self, a_word, api_client: RadioBrowser):
        return api_client.search(state=a_word)
