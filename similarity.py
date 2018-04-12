# # import math
# # from collections import Counter
# # def get_cosine(vec1, vec2):
# #     common = set(vec1.keys()) & set(vec2.keys())
# #     numerator = sum([vec1[x] * vec2[x] for x in common])

# #     sum1 = sum([vec1[x]**2 for x in vec1.keys()]) 
# #     sum2 = sum([vec2[x]**2 for x in vec2.keys()]) 
# #     denominator = math.sqrt(sum1) * math.sqrt(sum2)
   
# #     if not denominator:
# #         return 0.0 
# #     else:
# #         return float(numerator) / denominator

# # def text_to_vector(text): 
# #     words = text.split() 
# #     return Counter(words)

# # # text1 = 'This is an article on analytics vidhya' 
# # # text2 = 'article on analytics vidhya is about natural language processing'

# # text1 = 'moonday'
# # text2 = 'noon'

# # vector1 = text_to_vector(text1) 
# # vector2 = text_to_vector(text2) 
# # percentage_similar = get_cosine(vector1, vector2)

# # print(percentage_similar)
# from nltk.corpus import wordnet as wn

# forms = [] #We'll store the derivational forms in a set to eliminate duplicates
# for happy_lemma in wn.lemmas("mine"): #for each "happy" lemma in WordNet
#     forms.append(happy_lemma.name()) #add the lemma itself
#     for related_lemma in happy_lemma.derivationally_related_forms(): #for each related lemma
#         forms.append(related_lemma.name()) #add the related lemma
#         
# print (lemma('gave'))
# from pattern.en import conjugate, lemma, lexeme,PRESENT,SG
# x=lexeme('characterization')
# print (conjugate(verb='give',tense=PRESENT,number=SG)) # he / she / it
import io
from google.cloud import vision
import re
import nltk
from nltk import sent_tokenize,word_tokenize
from nltk.corpus import wordnet as wn
from pattern.en import conjugate, lemma, lexeme,PRESENT,SG
import math 

answer=['i','am','eat','eating','in','a','mine','mined']
keywords=['eat','mine','shine']
extended_keywords=[]
keywords_matched=0
for word in keywords:
    temp_list=[]
    temp_list.extend(lexeme(word))
    for happy_lemma in wn.lemmas(word): #for each "happy" lemma in WordNet
        temp_list.append(happy_lemma.name()) #add the lemma itself
        for related_lemma in happy_lemma.derivationally_related_forms(): #for each related lemma
            temp_list.append(related_lemma.name()) #add the related lemma
    temp_list=list(set(temp_list))
    extended_keywords.append((word,temp_list))

keywords_dictionary={key:value for (key,value) in extended_keywords}
# print(keywords_dictionary)

for (keyword,keyword_list) in keywords_dictionary.items():
        for word in keyword_list:
            if word in answer:
                keywords_matched=keywords_matched+1
                break

print(keywords_matched)

