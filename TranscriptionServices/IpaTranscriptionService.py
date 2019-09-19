# -*- coding: utf-8 -*-

import re
import requests
import bs4


class GenericTranscriptionService:
    def __init__(self, name, url):
        self.name = name;
        self.url = url

    def translate(self, ) -> 'any':
        raise NotImplemented

    def __str__(self):
        return 'IPA Translator Service: ' + self.name + '\nURL: ' + self.url

    def __repr__(self):
        return self.__str__()


class IpaTranscriptionService(GenericTranscriptionService):
    def __init__(self, name, url):
        super().__init__(name, url);
        self.headers = None
        self.translated_text = None


    def set_headers(self, headers: dict) -> dict:
        return headers

    def fetch_target_page(self, url: str, method='get') -> bs4.BeautifulSoup:
        raise NotImplemented



