import unittest
import requests
from bs4 import BeautifulSoup


from SpanishDictScraper import SpanishDictScraper


class TestSpanishDictScraper(unittest.TestCase):
    def setUp(self):
        self.spanishDictScraper = SpanishDictScraper

    def test_get_translation_from_conjugation_result(self):
        word = "vibrar"
        url = 'http://www.spanishdict.com/conjugate/' + word
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        x = self.spanishDictScraper.get_translation_from_conjugation_result(soup)
        print(x)
        self.assertTrue(x == "to vibrate")

    def test_get_definitions_with_examples(self):
        x = self.spanishDictScraper.get_definitions_with_examples("vibrar")

        self.assertTrue(len(x) == 5)

    def test_get_definitions_batch(self):
        sample_words = ['vibrar', 'arre']

        x = self.spanishDictScraper.get_definitions_batch(sample_words)

        self.assertTrue(len(x) == 8)

    def test_get_conjugation(self):
        self.spanishDictScraper.get_conjugation("vibrar")


if __name__ == '__main__':
    unittest.main()
