# -*- coding: utf-8 -*-

import re
import urllib
import bs4


class GenericTranscriptionService:
    def __init__(self, name, url):
        self.name = name;
        self.url = url

    def translate_to_ipa(self, ) -> 'any':
        raise NotImplemented

    def __str__(self):
        return 'IPA Translator Service: ' + self.name + '\nURL: ' + self.url

    def __repr__(self):
        return self.__str__()


class IpaTranscriptionService(GenericTranscriptionService):
    def __init__(self, name, url):
        super().__init__(name, url);
        self.work_with_forms = False
        self.headers = None

    def set_form_fields(self, text_to_translate_to_ipa: str) -> None:
        self.works_with_forms = True

    def set_headers(self, headers: dict) -> dict:
        return headers

    def fetch_target_page(self, url: str) -> bs4.BeautifulSoup:
        if not self.headers:
            req = urllib.request.Request(url, data=self.form_fields)
        else:
            req = urllib.request.Request(url=self.url, fields=self.form_fields, header=self.header)
        page_result = urllib.request.urlopen(req).read()
        soup = bs4.BeautifulSoup(page_result, 'html.parser')
        return soup



