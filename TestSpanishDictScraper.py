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
        soup = BeautifulSoup(r.content, "html5lib")
        x = self.spanishDictScraper.get_translation_from_conjugation_result(soup)
        self.assertTrue(x == "to vibrate to shake")

    def test_get_definition_with_examples(self):
        expected_result = {'english': "to vibrate (to move vigorously)\nPlay the chord and let the strings vibrate for the whole measure.\n\nto shake (to rattle)\nThe earth shook when the cannons fired.\n\nto quiver (to tremble)\nThe speaker's voice quivered because she was nervous.\n\nto be thrilled (to be moved)\nMariano was thrilled to hear that his daughter won the award.\n\n", 'spanish': 'vibrar\n\nToca el acorde y deja que las cuerdas vibren todo el compás.\n\nLa tierra vibró cuando dispararon los cañones.\n\nA la oradora le vibraba la voz porque estaba nerviosa.\n\nMariano vibró al escuchar que su hija había ganado el premio.'}
        x = self.spanishDictScraper.get_definition_with_examples("vibrar", seed=0)

        self.assertTrue(x == expected_result)


    def test_get_conjugation_batch(self):
        expected_result = {'vibrar': {'english': 'Conjugation: vibrar (to vibrate to shake) \npresentIndicative', 'spanish': 'vibro\nvibras\nvibra\nvibramos\nvibráis\nvibran'}, 'cocinar': {'english': 'Conjugation: cocinar (to cook) \npresentIndicative', 'spanish': 'cocino\ncocinas\ncocina\ncocinamos\ncocináis\ncocinan'}}
        x = SpanishDictScraper.get_conjugation_batch(['vibrar', 'cocinar'])
        self.assertTrue(x == expected_result)


    def test_get_conjugation_table_elements(self):
        expected = {
            'pastPerfectSubjunctive': ['hubiera vibrado', 'hubieras vibrado', 'hubiera vibrado', 'hubiéramos vibrado',
                                       'hubierais vibrado', 'hubieran vibrado'],
            'presentIndicative': ['vibro', 'vibras', 'vibra', 'vibramos', 'vibráis', 'vibran'],
            'preteritContinuous': ['estuve vibrando', 'estuviste vibrando', 'estuvo vibrando', 'estuvimos vibrando',
                                   'estuvisteis vibrando', 'estuvieron vibrando'],
            'presentSubjunctive': ['vibre', 'vibres', 'vibre', 'vibremos', 'vibréis', 'vibren'],
            'futurePerfect': ['habré vibrado', 'habrás vibrado', 'habrá vibrado', 'habremos vibrado', 'habréis vibrado',
                              'habrán vibrado'],
            'futureIndicative': ['vibraré', 'vibrarás', 'vibrará', 'vibraremos', 'vibraréis', 'vibrarán'],
            'presentContinuous': ['estoy vibrando', 'estás vibrando', 'está vibrando', 'estamos vibrando',
                                  'estáis vibrando',
                                  'están vibrando'],
            'conditionalIndicative': ['vibraría', 'vibrarías', 'vibraría', 'vibraríamos', 'vibraríais', 'vibrarían'],
            'imperfectIndicative': ['vibraba', 'vibrabas', 'vibraba', 'vibrábamos', 'vibrabais', 'vibraban'],
            'negativeImperative': ['no vibres', 'no vibre', 'no vibremos', 'no vibréis', 'no vibren'],
            'conditionalPerfect': ['habría vibrado', 'habrías vibrado', 'habría vibrado', 'habríamos vibrado',
                                   'habríais vibrado', 'habrían vibrado'],
            'pastPerfect': ['había vibrado', 'habías vibrado', 'había vibrado', 'habíamos vibrado', 'habíais vibrado',
                            'habían vibrado'],
            'imperfectSubjunctive': ['vibrara', 'vibraras', 'vibrara', 'vibráramos', 'vibrarais', 'vibraran'],
            'imperfectContinuous': ['estaba vibrando', 'estabas vibrando', 'estaba vibrando', 'estábamos vibrando',
                                    'estabais vibrando', 'estaban vibrando'],
            'futurePerfectSubjunctive': ['hubiere vibrado', 'hubieres vibrado', 'hubiere vibrado', 'hubiéremos vibrado',
                                         'hubiereis vibrado', 'hubieren vibrado'],
            'preteritPerfect': ['hube vibrado', 'hubiste vibrado', 'hubo vibrado', 'hubimos vibrado',
                                'hubisteis vibrado',
                                'hubieron vibrado'],
            'preteritIndicative': ['vibré', 'vibraste', 'vibró', 'vibramos', 'vibrasteis', 'vibraron'],
            'presentPerfect': ['he vibrado', 'has vibrado', 'ha vibrado', 'hemos vibrado', 'habéis vibrado',
                               'han vibrado'],
            'imperfectSubjunctive2': ['vibrase', 'vibrases', 'vibrase', 'vibrásemos', 'vibraseis', 'vibrasen'],
            'imperative': ['vibra', 'vibre', 'vibremos', 'vibrad', 'vibren'],
            'futureContinuous': ['estaré vibrando', 'estarás vibrando', 'estará vibrando', 'estaremos vibrando',
                                 'estaréis vibrando', 'estarán vibrando'],
            'futureSubjunctive': ['vibrare', 'vibrares', 'vibrare', 'vibráremos', 'vibrareis', 'vibraren'],
            'conditionalContinuous': ['estaría vibrando', 'estarías vibrando', 'estaría vibrando',
                                      'estaríamos vibrando',
                                      'estaríais vibrando', 'estarían vibrando'],
            'presentPerfectSubjunctive': ['haya vibrado', 'hayas vibrado', 'haya vibrado', 'hayamos vibrado',
                                          'hayáis vibrado',
                                          'hayan vibrado']}
        word = "vibrar"

        url = 'http://www.spanishdict.com/conjugate/' + word
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
        x = self.spanishDictScraper.get_conjugation_table_elements(soup)

        self.assertTrue(x == expected)


if __name__ == '__main__':
    unittest.main()
