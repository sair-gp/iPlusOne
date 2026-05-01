from wordfreq import *
import json

words = top_n_list("fr", 20, wordlist="best")
data = {}
file_path = "./data/commonWords.json"
# file_pathson = "./data/commonWords.txt";


for w in words:
    if len(w) <= 1:
        continue
    freq = word_frequency(w, "fr")
    data[w] = freq


# text_data = "\n".join(f"`{w}` has frequency: {f:.2e}" for w, f in data.items())

try:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Json file '{file_path}' was created. Final lenght: {len(data)}")
except FileExistsError:
    print("That file already exists!")
