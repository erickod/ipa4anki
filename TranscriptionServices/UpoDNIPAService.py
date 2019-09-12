import re
import urllib
import bs4
from .IpaTranscriptionService import IpaTranscriptionService


class UpoDNIPAService(IpaTranscriptionService):
    def __init__(self, text_to_translate_to_ipa: str):
        super().__init__('UpoDN.com', 'http://upodn.com/phon.php')
        self.form_fields = self.set_form_fields(text_to_translate_to_ipa)
        self.headers = self.set_headers({})
        self.ipa_text = self.translate_to_ipa()

    def set_form_fields(self, text_to_translate_to_ipa: str, mark_word_stress=False) -> dict:
        self.works_with_forms = True
        service_dict = {
            'intext': text_to_translate_to_ipa,
            'ipa': 0,
            'stress': 'checked' if mark_word_stress else 'unchecked'
        }

        return urllib.parse.urlencode( service_dict).encode()

    def translate_to_ipa(self) -> 'any':
        soup = self.fetch_target_page(self.url)
        return re.sub(r"  ", '', soup.find_all('td')[1].text)
