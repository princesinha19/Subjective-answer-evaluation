# # try____________________________________________________


# # Generate some data to send to PHP
# #result = {'status': 'Yes!'}

# # Send it to stdout (to PHP)
# #print json.dumps(1)
# # try___________________________________________________

import io
from google.cloud import vision
import re
import nltk
from nltk import sent_tokenize,word_tokenize
from nltk.corpus import wordnet as wn
from pattern.en import conjugate, lemma, lexeme,PRESENT,SG
import math
import os

import sys, json
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/ayush/Downloads/key.json"





project_dir = "/opt/lampp/htdocs/project_be/project/"
image_file = project_dir+'a1.png'

client = vision.ImageAnnotatorClient()

def get_marks(data,image_file):

    keywords_matched=0
    #maximum_marks = 5
    maximum_marks = data[0]
    
    keywords=[]
    keywords=data[3].split(',')
    # keywords=['data','mine','database','characterization','knowledge','background','task','classify','associate','visualize','predict','cluster']
    expected_keywords = len(keywords)
    
    #expected_no_of_words = 200
    expected_no_of_words = data[1]
    
    #expected_no_of_sentences = 15
    expected_no_of_sentences = data[2]
    
    # extended_keywords = []
    # for word in keywords:
    #     for syn in wn.synsets(word):
    #         for l in syn.lemmas():
    #             extended_keywords.append(l.name())
    
    forms = [] #We'll store the derivational forms in a set to eliminate duplicates
    for word in keywords:
        for happy_lemma in wn.lemmas(word): #for each "happy" lemma in WordNet
            forms.append(happy_lemma.name()) #add the lemma itself
            for related_lemma in happy_lemma.derivationally_related_forms(): #for each related lemma
                forms.append(related_lemma.name()) #add the related lemma
    
    verb=[]
    for word in keywords:
        verb.extend(lexeme(word))
    
    # keywords.extend(extended_keywords)
    keywords.extend(forms)
    keywords.extend(verb)
    
    keywords =  [x.lower() for x in keywords]
    keywords = list(set(keywords))
    # print(keywords)
    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    
    response = client.text_detection(image=image)
    texts = response.text_annotations
    string = texts[0].description.replace('\n',' ').lower() #for converting to lower case
    string = re.sub('[^A-Za-z0-9.]+', ' ', string) #for eliminating special character
    
    print string
    
    word_list = word_tokenize(string) #for word spliting
    no_of_words = len(word_list)
    if no_of_words>expected_no_of_words:
        no_of_words=expected_no_of_words
    
    no_of_sentences = len(sent_tokenize(string))
    if no_of_sentences>expected_no_of_sentences:
        no_of_sentences=expected_no_of_sentences
    print 'no_of_words',no_of_words
    print 'no_of_sentences',no_of_sentences
    
    for keyword in keywords:
        if(keyword in word_list):
            keywords_matched=keywords_matched+1        
    if keywords_matched>expected_keywords:
        keywords_matched = expected_keywords
    print 'keywords matched',keywords_matched
    
    keywords_percentage = 0.55*(keywords_matched/expected_keywords)    
    word_percentage = 0.35*(no_of_words/expected_no_of_words)
    sentence_percentage = 0.10*(no_of_sentences/expected_no_of_sentences)
    
    print 'keywords_percentage',keywords_percentage
    print 'word_percentage',word_percentage
    print 'sentence_percentage',sentence_percentage
    
    total_marks = maximum_marks*(keywords_percentage+word_percentage+sentence_percentage)
    total_marks=round(total_marks,1)
    digit=total_marks*10
    if(digit%10<5):
        total_marks=math.floor(total_marks)
    if(digit%10>5):
        total_marks=math.ceil(total_marks)  
    print 'total_marks',total_marks
    return total_marks


from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
app = Flask(__name__)
img_directory = app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def get_result():

    files = request.files['image']
    filename = secure_filename(files.filename)
    files.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    files = app.config['UPLOAD_FOLDER']+filename
    print files

    if files:
        print(request.form['keywords'])
        data = [int(request.form['max_marks']), int(request.form['min_words']), int(request.form['min_sentence']), request.form['keywords']]
        
        marks = get_marks(data,files)
        return render_template('result.html', marks=marks)
app.run(host='0.0.0.0')