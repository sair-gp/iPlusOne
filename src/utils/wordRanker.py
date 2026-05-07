def rankNewIntelligence(newLemmas, wordFreqDict=None):
    """
    Ranks only the NEW words based on their importance.
    If wordFreqDict is provided, it uses frequency sums.
    Otherwise, it uses the number of conjugations.
    """
    # 1. Scoring
    scored_lemmas = []
    for lemma, words in newLemmas.items():
        if wordFreqDict:
            # Score = sum of frequencies of all its conjugations
            score = sum(wordFreqDict.get(w, 0) for w in words)
        else:
            # Score = number of conjugations found
            score = len(words)

        scored_lemmas.append((lemma, words, score))

    # 2. The sort: Highest score = Rank 1
    scored_lemmas.sort(key=lambda x: x[2], reverse=True)

    # 3. Format: {Rank: {"lemma": X, "words": [Y], "importance": Z}}
    return {
        i + 1: {"lemma": l, "words": w, "score": s}
        for i, (l, w, s) in enumerate(scored_lemmas)
    }


def getDbExclusions(dbLemmas, newLemmas):
    """
    Returns lemmas that are in the DB but NOT in the current text.
    Use this to see what 'Old Intelligence' is missing from the session.
    """
    missing_keys = set(dbLemmas.keys()) - set(newLemmas.keys())
    return {k: dbLemmas[k] for k in missing_keys}
