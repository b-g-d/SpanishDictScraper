import re
from time import sleep

import requests
from bs4 import BeautifulSoup, Tag
import numpy as np


class SpanishDictScraper:
    BAD_RESULT_STRING = "baddy bad"
    CONJUGATION_TYPES = {"presentSubjunctive", "futurePerfectSubjunctive", "imperative", "imperfectSubjunctive2",
                         "pastPerfect", "preteritIndicative", "conditionalContinuous", "imperfectContinuous",
                         "futurePerfect", "futureSubjunctive", "conditionalIndicative", "preteritPerfect",
                         "conditionalPerfect", "futureContinuous", "imperfectIndicative", "presentContinuous",
                         "pastPerfectSubjunctive", "presentIndicative", "futureIndicative", "presentPerfectSubjunctive",
                         "presentPerfect", "imperfectSubjunctive", "negativeImperative", "preteritContinuous"}

    @staticmethod
    def get_conjugation_batch(iteratable, conjugation=None):

        if conjugation is None:
            conjugation = ["presentIndicative"]

        results = {}

        for word in iteratable:
            for conj in conjugation:
                results[word + conj] = SpanishDictScraper.get_conjugation(word, conj)
                sleep(.5)

        return results

    @staticmethod
    def get_definition_batch(iteratable):
        results = {}

        for word in iteratable:
            results[word] = SpanishDictScraper.get_definition_with_examples(word)
            sleep(.1)

        return results

    @staticmethod
    def _is_good_result(soup):
        if soup.find('div', {'class': 'mismatch'}) or soup.find("div", {'class': 'spelling'}):
            return False
        return True

    @staticmethod
    def _transform_conjugation_string(conj):
        return " ".join([x.title() for x in re.split("([a-z]*[a-z])([A-Z][a-z]*)", conj) if x != ""])

    @staticmethod
    def get_conjugation(spanish_verb, conjugation="presentIndicative"):
        assert (conjugation in SpanishDictScraper.CONJUGATION_TYPES)

        url = 'http://www.spanishdict.com/conjugate/' + spanish_verb
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html5lib")
        edited_conjugation = SpanishDictScraper._transform_conjugation_string(conjugation)
        results_dict = {'spanish': "", 'english': "<div><b>Conjugation</b>: {0} ({1}) </div><div><b>" + edited_conjugation + "</b></div>"}

        if SpanishDictScraper._is_good_result(soup):
            try:
                english_translation = SpanishDictScraper.get_translation_from_conjugation_result(soup)
                conjugation_list = SpanishDictScraper.get_conjugation_table_elements(soup)[conjugation]

                results_dict['spanish'] = "<div>"+"</div><div>".join([x for x in conjugation_list]) + "</div>"
                results_dict['english'] = results_dict['english'].format(spanish_verb, english_translation)
                return results_dict
            except AttributeError:
                print("verb I'm having trouble with:\t" + spanish_verb + "\nat url:\t" + url)
                return {'spanish': "", 'english':SpanishDictScraper.BAD_RESULT_STRING}

        return {'spanish': "", 'english':SpanishDictScraper.BAD_RESULT_STRING}

    @staticmethod
    def get_translation_from_conjugation_result(conjugation_result_soup):
        """
        :return: str
        :type conjugation_result_soup: BeautifulSoup
        """
        return " ".join([x.contents[0] for x in conjugation_result_soup.find("div", {"class": "el"}).contents if isinstance(x, Tag)])

    @staticmethod
    def get_conjugation_table_elements(conjugation_result_soup):
        """
        :return: str
        :type conjugation_result_soup: BeautifulSoup
        """
        all_conjugations = conjugation_result_soup.find_all("div", {"class": "vtable-word-text"})

        result = dict((el, []) for el in SpanishDictScraper.CONJUGATION_TYPES)

        for entry in all_conjugations:
            k = entry.attrs['data-tense']
            entry_content = ["".join(x.string for x in entry.contents)] if len(entry.contents)>1 else entry.contents
            result[k] += entry_content

        return result

    @staticmethod
    def get_definition_with_examples(spanish_word: str, seed=None) -> dict:
        if seed:
            np.random.seed(seed)

        url = 'http://www.spanishdict.com/translate/' + spanish_word
        r = requests.get(url)

        if r is None:
            print("sleeping")
            sleep(3)
            r = requests.get(url)

        soup = BeautifulSoup(r.content, "html5lib")

        if SpanishDictScraper._is_good_result(soup):


            search_result_neodict_element = soup.find('div', {'class': "dictionary-neodict"})

            if search_result_neodict_element:
                return SpanishDictScraper.get_results_from_neodict_element(search_result_neodict_element, spanish_word)

            search_result_velazquez_element = soup.find('div', {'class': "dictionary-velazquez"})
            if search_result_velazquez_element:
                return SpanishDictScraper.get_results_from_velazquez_element(search_result_velazquez_element, spanish_word)

            else:
                return {'spanish': spanish_word, 'english': SpanishDictScraper.BAD_RESULT_STRING}
        else:

            return {'spanish': spanish_word, 'english': SpanishDictScraper.BAD_RESULT_STRING}

    @staticmethod
    def get_results_from_velazquez_element(velazquez_soup, spanish_word):
        """
        :type velazquez_soup: BeautifulSoup
        :rtype: dict
        """

        #< span class ="part_of_speech" > adjective < / span >
        #< span class ="def" > Applied to showy or tawdry colors.< / span >

        part_of_speech = velazquez_soup.find('span', {'class':"part_of_speech"})

        assert isinstance(part_of_speech, Tag)

        list_of_defs = velazquez_soup.find_all('span', {'class':'def'})
        english_results = "<div>(" + part_of_speech.string + ")</div>"

        for d in list_of_defs:
            english_results += "<div>" + d.contents[0] + "</div>"

        return {'spanish': spanish_word, 'english': english_results}


    @staticmethod
    def get_results_from_neodict_element(neodict_soup, spanish_word):

        results_dict = {'spanish': "<div>" + spanish_word + "</div><br>", 'english': ""}

        if neodict_soup is not None:
            different_definitions = neodict_soup.find_all('div',{'class': "dictionary-neodict-indent-1"})

            for definition in different_definitions:
                list_of_translations_for_each_definition = definition.find_all('a', {
                    "class": "dictionary-neodict-translation-translation"})
                list_of_examples_for_each_definition = definition.find_all('div',{"class": "dictionary-neodict-example"})

                random_one = np.random.randint(0, len(list_of_translations_for_each_definition), 1)[0]

                word_second_language = list_of_translations_for_each_definition[random_one].string if len(list_of_translations_for_each_definition[random_one]) > 0 else ""

                example_sentence_original_language = \
                    list_of_examples_for_each_definition[random_one].contents[0].contents[0]
                example_sentence_second_language = \
                    list_of_examples_for_each_definition[random_one].find('em', {'class': 'exB'}).contents[0]

                contexts_for_translation = definition.find_all('span', {'class': 'context'})
                context_string = "".join(["".join(x.contents) for x in contexts_for_translation if
                                          'dictionary-neodict-translation' not in x.parent.get('class')])
                if context_string is None:
                    context_string = ""

                results_dict['spanish'] += "<div>" + example_sentence_original_language + "</div><br>"

                results_dict['english'] += "<div>" + word_second_language + " " + context_string + "</div><div>" + example_sentence_second_language + "</div><br>"

            return results_dict
