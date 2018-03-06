# SpanishDictScraper

Takes an input csv with three labeled columns ["vocab", "definition", "conjugation"],
and converts it into a csv with two unlabeled columns ["english", "spanish"], for input into Anki. 
Each field of the resulting csv is formatted with html.  

Definitions are retrieved by default and not retrieved if the "definition" column is marked with a "n". 
Conjugations are retrieved if the "conjugation" column is marked with a "y".

The definitions and conjugations are scraped from SpanishDict.com

## Run Instructions
1. Install Python on your system ([Anaconda](https://conda.io/docs/installation.html) is an easy way to do it)
2. Create csv with specified columns ["vocab", "definition", "conjugation"]
3. Open the command line (terminal or the equivalent on Windows)
4. Navigate to the SpanishDictScrapter project
5. Execute the command 'python Run.py <path to csv from current folder>'
6. Wait
7. Look for results in the same folder as your original csv

## Desired Changes
* Always fetch the infinitive form of verbs for definitions
* Enable lookup of conjugations for arbitrary conjugation of a given verb
* Retrieve appropriate article (gender) for searched nouns
* Store running list of failed searches and output that with results. 
* For words that have many meanings, create a separate card for each meaning 