import pandas as pd
pd.set_option('display.max_colwidth', None)
sentences = pd.read_csv('files/sente.csv', header=None)
nouns = pd.read_csv('files/nouns.csv', header=None)
adjectives = pd.read_csv('files/adjectives.csv', header=None)