import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = "In 2018, twenty-three days after Thanos erased half of all life in the universe,[a] Carol Danvers rescues Tony Stark and Nebula from deep space and they reunite with the remaining Avengers—Bruce Banner, Steve Rogers, Thor, Natasha Romanoff, and James Rhodes—and Rocket on Earth. Locating Thanos on an uninhabited planet, they plan to use the Infinity Stones to reverse his actions, but discover Thanos has already destroyed them to prevent further use. Enraged, Thor decapitates Thanos.Five years later, Scott Lang escapes from the Quantum Realm.[b] Reaching the Avengers Compound, he explains that he experienced only five hours while trapped. Theorizing that the Quantum Realm allows time travel, they ask a reluctant Stark to help them retrieve the Stones from the past to reverse the actions of Thanos in the present. Stark, Rocket, and Banner, who has since merged his intelligence with the Hulk's strength, build a time machine. Banner notes that altering the past does not affect their present; any changes create alternate realities. Banner and Rocket travel to Norway, where they visit the Asgardian refugees' settlement New Asgard and recruit an overweight and despondent Thor. In Tokyo, Romanoff recruits Clint Barton, who became a vigilante after the death of his family.Banner, Lang, Rogers, and Stark time-travel to New York City during Loki's attack in 2012."
def summarizer(text):
    docu = text
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    # print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word] = 1
            else:
                word_freq[word] = word_freq[word]+1

    max_freq = max(word_freq.values())
    # print(max_freq)
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    sent_token = [sents for sents in doc.sents]
    # print(sent_token)
    sent_scores = {}
    for sentence in sent_token:
        for word in sentence:
            if word in word_freq.keys():
                if sentence not in sent_scores.keys():
                    sent_scores[sentence] = word_freq[word]
                else:
                    sent_scores[sentence] += word_freq[word]
    # print(sent_scores)

    select_len = int(sent_token.__len__()*0.3)
    # print(select_len)
    summary = nlargest(select_len,sent_scores,key = sent_scores.get)
    # We need to choose the summary in such a way that the chosen lines are the nmax but at the same time they are ordered
  
    summary = [word.text for word in summary]
    # print(summary)
    summary1 = []
    for line in sent_token:
        if line.text in summary:
            summary1.append(line)
    summary = [word.text for word in summary1]
    final_summary = " ".join(summary)
    # print(final_summary)
    return final_summary,docu,len(docu.split(' ')),len(final_summary.split(' '))
summarizer(text)