import nltk
from nltk.corpus import wordnet

keywords = ['dog','boy','day','apple']
extended_keywords = []

for word in keywords:
	for syn in wordnet.synsets(word):
		for l in syn.lemmas():
			extended_keywords.append(l.name())

extended_keywords = list(set(extended_keywords))
print(extended_keywords)