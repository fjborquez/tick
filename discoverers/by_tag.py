from pyradios import RadioBrowser

from discoverable import Discoverable


class DiscovererByTag(Discoverable):
    def discover(self, a_word, api_client: RadioBrowser):
        return api_client.search(tag=a_word)
