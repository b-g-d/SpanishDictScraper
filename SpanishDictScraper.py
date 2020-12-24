import re
import sys
from time import sleep

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


class SpanishDictScraper:
    BAD_RESULT_STRING = "baddy bad"
    CONJUGATION_TYPES = {"presentSubjunctive", "futurePerfectSubjunctive", "imperative", "imperfectSubjunctive2",
                         "pastPerfect", "preteritIndicative", "conditionalContinuous", "imperfectContinuous",
                         "futurePerfect", "futureSubjunctive", "conditionalIndicative", "preteritPerfect",
                         "conditionalPerfect", "futureContinuous", "imperfectIndicative", "presentContinuous",
                         "pastPerfectSubjunctive", "presentIndicative", "futureIndicative", "presentPerfectSubjunctive",
                         "presentPerfect", "imperfectSubjunctive", "negativeImperative", "preteritContinuous"}

    @staticmethod
    def get_conjugation_batch(list_of_spanish_words):

        results = pd.DataFrame(columns=["back", "front"])

        for word in list_of_spanish_words:
            r = SpanishDictScraper.get_conjugation(word)
            results = results.append(r, ignore_index=True)
            sleep(.1)

        return results

    @staticmethod
    def get_definition_batch(list_of_spanish_words):

        list_of_dfs = [SpanishDictScraper.get_definitions_with_examples(x) for x in list_of_spanish_words]

        final_results = pd.concat(list_of_dfs, ignore_index=True).reset_index(drop=True)

        return final_results

    @staticmethod
    def _is_good_result(soup):
        if soup.find('div', {'class': 'mismatch'}) or soup.find("div", {'class': 'spelling'}):
            return False
        return True

    @staticmethod
    def _transform_conjugation_string(conj):
        return " ".join([x.title() for x in re.split("([a-z]*[a-z])([A-Z][a-z]*)", conj) if x != ""])

    @staticmethod
    def get_conjugation(verb_es):
        verb_form_class = "_2v8iz7Ez"
        prompt = "<div><b>Conjugation</b>: {verb_es} ({verb_en}) </div><div><b>{conjugation}</b></div>"

        url = 'http://www.spanishdict.com/conjugate/' + verb_es
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        if SpanishDictScraper._is_good_result(soup):
            try:
                verb_en = SpanishDictScraper.get_translation_from_conjugation_result(soup)
                sections_of_interest = soup.find_all("div", {"class": verb_form_class})
                verb_cases = [x.text for x in sections_of_interest]
                tables = [x.find_next("table") for x in sections_of_interest]

                dfs = []

                for i, t in enumerate(tables):
                    t_df = SpanishDictScraper.convert_html_table_to_dataframe(t, True)
                    t_df.columns = [prompt.format(verb_es=verb_es, verb_en=verb_en, conjugation=verb_cases[i] + " " + x) for x in t_df.columns]
                    t_df.drop(t_df.columns[0], axis=1, inplace=True)
                    t_df = t_df.transpose()
                    t_df["back"] = t_df.apply(SpanishDictScraper._combine_conjugation_cols, axis=1)
                    t_df["front"] = t_df.index
                    dfs.append(t_df[["front", "back"]].reset_index(drop=True))

                if len(dfs) > 0:
                    return pd.concat(dfs, axis=0)
                else:
                    print("no conjugations for " + verb_es)
            except AttributeError:
                print("verb I'm having trouble with:\t" + verb_es + "\nat url:\t" + url)

        else:
            print("bad soup with:\t" + verb_es + "\nat url:\t" + url)

    @staticmethod
    def convert_html_table_to_dataframe(t, with_headers=True):
        the_data = []
        col_names = None
        rows = t.find_all("tr")

        for i, r in enumerate(rows):
            if with_headers == True:
                if i == 0:
                    col_names = [d.text for d in r.find_all("td")]
                else:
                    the_data.append([d.text for d in r.find_all("td")])
            else:
                the_data.append([d.text for d in r.find_all("td")])

        result = pd.DataFrame(the_data)

        if col_names is not None:
            result.columns = col_names
        return result

    @staticmethod
    def get_translation_from_conjugation_result(conjugation_result_soup):
        """
        :return: str
        :type conjugation_result_soup: BeautifulSoup
        """
        div_class_for_translations = "quickdef1-es"
        definition_element = conjugation_result_soup.find("div", {"id" : div_class_for_translations})
        return definition_element.text

    @staticmethod
    def _combine_conjugation_cols(row):
        """
        :return: str
        :type row: Series
        """
        return "</br>".join([x for x in row])

    @staticmethod
    def get_definitions_with_examples(spanish_word: str, seed=None):
        if seed:
            np.random.seed(seed)

        url = 'http://www.spanishdict.com/translate/' + spanish_word
        r = requests.get(url)

        if r is None:
            print("sleeping")
            sleep(3)
            r = requests.get(url)

        soup = BeautifulSoup(r.content, "lxml")

        es_word_span_class = '_3QFIA64h'

        example_box_div_class = '_1IN7ttrU'
        translation_span_marker_class = 'OxB8M-Y_'
        es_example_span_class = '_1f2Xuesa'
        en_example_span_class = '_3WrcYAGx'

        if SpanishDictScraper._is_good_result(soup):
            try:
                es_word = soup.find("span", {'class': es_word_span_class}).text

                example_spans = [x for x in soup.find_all('div', {'class': example_box_div_class})]
                en_translations = [x.find('span', {'class': translation_span_marker_class}).find_next_sibling().text
                                   for x in example_spans]
                es_sentences = [x.find('span', {'class': es_example_span_class}) for x in example_spans]
                en_sentences = [x.find('span', {'class': en_example_span_class}) for x in example_spans]

                result_dict = {'es_word': [es_word] * len(en_translations),
                               'en_translation': en_translations,
                               'es_sentence': [x.text if x is not None else None for x in es_sentences],
                               'en_sentence': [x.text if x is not None else None for x in en_sentences]}

                r = pd.DataFrame(result_dict).dropna(axis=0, how='any')

                r['front'] = r['es_word'] + "</br></br>" + r['es_sentence']
                r['back'] = r['en_translation'] + "</br></br>" + r['en_sentence']

                return r[['front', 'back']]
            except AttributeError:
                print("definition I'm having trouble with:\t" + spanish_word + "\nat url:\t" + url)
        else:
            print("bad soup with:\t" + spanish_word + "\nat url:\t" + url)


if __name__ == '__main__':
    args = sys.argv

    input_filename = args[1]

    df = pd.read_csv(input_filename).fillna("")
    result_df = pd.DataFrame(columns=["front", "back"])

    words_to_define = df[df['definition'] != "n"]['vocab'].tolist()
    definitions = SpanishDictScraper.get_definition_batch(words_to_define)

    words_to_conjugate = df[df['conjugation'] == "y"]['vocab'].tolist()
    conjugations = SpanishDictScraper.get_conjugation_batch(words_to_conjugate)

    result_df = result_df.append([definitions, conjugations])

    first_part, second_part = input_filename.split('.c')

    result_df.to_csv(first_part + "_READY.csv", index=False, sep=";", header=False)
    print("Complete")