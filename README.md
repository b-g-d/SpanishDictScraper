# SpanishDictScraper

Takes an input csv with three labeled columns ["vocab", "definition", "conjugation"],
and converts it into a csv with two unlabeled columns ["english", "spanish"], for input into Anki. 
Each field of the resulting csv is formatted with html.  

Definitions are retrieved by default and not retrieved if the "definition" column is marked with a "n". 
Conjugations are retrieved if the "conjugation" column is marked with a "y".

The definitions and conjugations are scraped from SpanishDict.com

## Desired Changes
* Always fetch the infinitive form of verbs for definitions
* Enable lookup of conjugations for arbitrary conjugation of a given verb
* Retrieve appropriate article (gender) for searched nouns
* Store running list of failed searches and output that with results. 