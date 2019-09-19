from os.path import join, abspath, dirname
import re
import requests
import sqlite3
import bs4
from .IpaTranscriptionService import IpaTranscriptionService
from .utils import install


class CMULexiconTool(IpaTranscriptionService):
    def __init__(self, word: str):
        super().__init__('CMU Lexicon Tool', 'http://www.speech.cs.cmu.edu/cgi-bin/tools/logios/lextool.pl')
        try:
            import requests
        except ModuleNotFoundError as e:
            if e == "No module named 'requests'":
                install("requests")
            import requests
            pass

        self.conn = self.db_connect()
        try:
            self.create_cmu_cache_db_table()
        except sqlite3.OperationalError as e:
            if e == 'table dictionary already exists':
                pass
        self.search_term = re.split(" ", word)
        self.headers = self.set_headers({})
        self.file_to_upload = {'wordfile': word.encode()}
        self.cmu_list = self.translate()
        self.search_on_cmu_cache(word)

    def translate(self):
        term = self.search_term[0]
        cache_result = self.search_on_cmu_cache(term)
        if not cache_result:
            ws_result = self.fetch_target_page()
            cmu_list = [ws_result[1]] # -> cmu_list -> formato => [['G R IY T']]

            for el in cmu_list:
                for e in el:
                    self.insert_on_cmu_cache([term, e])
        else:
            temp_list =[]
            for el in cache_result:
                temp_list.append(el[0])
            cmu_list = [temp_list]

        return cmu_list #[['G R IY T']]

    def fetch_target_page(self,):
        dict_url = self.get_custom_dict_link(self.url)
        req = requests.get(url=dict_url)
        final_list = []
        ws_response = [l for l in re.split("\n", req.text) if l]
        temp_list = []
        for el in ws_response:
            final_list.append(el.split("\t")[0].lower())
            temp_list.append(el.split("\t")[1].lower())
        final_list.append(temp_list)
        return final_list

    def get_custom_dict_link(self, url,):
        req = requests.post(url=url, files=self.file_to_upload)
        page_result = req.text
        soup = bs4.BeautifulSoup(page_result, 'html.parser')
        return soup.findAll(text=lambda text: isinstance(text, bs4.Comment))[0].extract()[6:-2]

    def db_connect(self):
        return sqlite3.connect(join(abspath(dirname(__file__)),"cmu_dict_cache.db"))

    def get_word_using_local_db(self):
        ""

    def create_cmu_cache_db_table(self):
        create_table_query = """
                CREATE TABLE "dictionary" (
                    "id"	INTEGER PRIMARY KEY AUTOINCREMENT,
                    "word"	text NOT NULL,
                    "phonemes"	text NOT NULL
                );
                """
        self.conn.cursor().execute(create_table_query)

    def search_on_cmu_cache(self, word):
        query = """
        SELECT phonemes FROM dictionary WHERE word = ?;
        """
        cursor = self.conn.cursor()
        cursor.execute(query, (word,))
        query_result = cursor.fetchall()
        if not query_result:
            return []
        return query_result

    def insert_on_cmu_cache(self, term):
        query = """
        INSERT INTO dictionary ('word', 'phonemes')
        VALUES (?, ?)
        """
        cursor = self.conn.cursor()
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute(query, (term[0].lower(), term[1].lower()))
        self.conn.commit()


