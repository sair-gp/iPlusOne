import spacy
import wordComp

nlp = spacy.load("fr_core_news_lg")

diff = wordComp.get_diff()

text = result = " ".join(diff)

doc = nlp(text)

for token in doc:
    print(token.text, token.pos_, token.lemma_)
