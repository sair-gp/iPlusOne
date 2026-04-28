from wordfreq import *
import json

words = top_n_list("fr", 300, wordlist="best")
data = {}
file_path = "./data/commonWords.json"
# file_pathson = "./data/commonWords.txt";


for w in words:
    freq = word_frequency(w, "fr")
    data[w] = freq


# text_data = "\n".join(f"`{w}` has frequency: {f:.2e}" for w, f in data.items())

try:
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
        print(f"Json file '{file_path}' was created")
except FileExistsError:
    print("That file already exists!")
