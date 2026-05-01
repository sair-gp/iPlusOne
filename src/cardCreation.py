import wordComp
import utils.genaiClient as gc
import ankiConnect

words = wordComp.openWordList("data/lemmanized/newLemmasFortest-deck.json")
deckWords = wordComp.openWordList("data/decks/test-deck.json")

client = gc.initClient()


wordPhrases = gc.generateCardContextAI(
    client, words, deckWords, "Batman solving a crime"
)

print(wordPhrases)
