from SpanishDictScraper import SpanishDictScraper
import sys
import pandas as pd


MOST_IMPORTANT_TENSES = ["preteritIndicative", "imperative", "presentIndicative"]


if __name__ == '__main__':
    args = sys.argv

    input_filename = args[1]

    df = pd.read_csv(input_filename).fillna("")
    result_df = pd.DataFrame(columns=["english", "spanish"])

    definitions = SpanishDictScraper.get_definition_batch(df[df['definition'] != "n"]['vocab'].tolist())

    conjugations = SpanishDictScraper.get_conjugation_batch(df[df['conjugation'] == "y"]['vocab'].tolist(), MOST_IMPORTANT_TENSES)

    for k in definitions.keys():
        if definitions[k]['english'] != SpanishDictScraper.BAD_RESULT_STRING:
            result_df = result_df.append({'spanish':definitions[k]['spanish'], 'english':definitions[k]['english']}, ignore_index=True)

    for k in conjugations.keys():
        if conjugations[k]['english'] == SpanishDictScraper.BAD_RESULT_STRING:
            continue
        result_df = result_df.append({'spanish':conjugations[k]['spanish'], 'english':conjugations[k]['english']}, ignore_index=True)

    first_part, second_part = input_filename.split('.c')

    result_df.to_csv(first_part + "_READY.csv", index=False, sep=";", header=False)


