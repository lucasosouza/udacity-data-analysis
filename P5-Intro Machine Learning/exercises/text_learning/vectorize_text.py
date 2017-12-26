#!/usr/bin/python

import os
import pickle
import re
import sys

sys.path.append( "../tools/" )
from parse_out_email_text import parseOutText

"""
    Starter code to process the emails from Sara and Chris to extract
    the features and get the documents ready for classification.

    The list of all the emails from Sara are in the from_sara list
    likewise for emails from Chris (from_chris)

    The actual documents are in the Enron email dataset, which
    you downloaded/unpacked in Part 0 of the first mini-project. If you have
    not obtained the Enron email corpus, run startup.py in the tools folder.

    The data is stored in lists and packed away in pickle files at the end.
"""

from_sara  = open("from_sara.txt", "r")
from_chris = open("from_chris.txt", "r")

from_data = []
word_data = []

### temp_counter is a way to speed up the development--there are
### thousands of emails from Sara and Chris, so running over all of them
### can take a long time
### temp_counter helps you only look at the first 200 emails in the list so you
### can iterate your modifications quicker
#temp_counter = 0

for name, from_person in [("sara", from_sara), ("chris", from_chris)]:
    for path in from_person:
        ### only look at first 200 emails when developing
        ### once everything is working, remove this line to run over full dataset
        #temp_counter += 1
        #if temp_counter < 200:
        try: 
            path = os.path.join('..', path[:-1])
            print name, ': ', path
            email = open(path, "r")

            ### use parseOutText to extract the text from the opened email
            words = parseOutText(email)  
            ### use str.replace() to remove any instances of the words
            ### ["sara", "shackleton", "chris", "germani"]
            patt = 'sara|shackleton|chris|germani|sshacklensf|cgermannsf'
            words = re.sub(patt,'',words) 
            #words is a string, not an iterator. wrong usage of plural here has misleaded the programmer.

            ### append the text to word_data
            word_data.append(words)

            ### append a 0 to from_data if email is from Sara, and 1 if email is from Chris
            from_data.append(1) if name == 'chris' else from_data.append(0)

            email.close()

        except:
            pass

print "emails processed"
print word_data[152]
from_sara.close()
from_chris.close()

pickle.dump( word_data, open("your_word_data.pkl", "w") )
pickle.dump( from_data, open("your_email_authors.pkl", "w") )

### in Part 4, do TfIdf vectorization here

"""
#Remove english stopwords
from nltk.corpus import stopwords
sw = stopwords.words('english')

def remove_stopwords(text):
    text = text.split(' ')
    text = [word for word in text if word.lower() not in sw]
    return ' '.join(text)
word_data2 = map(remove_stopwords, word_data)
"""

# Transform the word_data into a tf-idf matrix using the sklearn TfIdf transformation. 
from sklearn.feature_extraction import text
word_matrix = text.TfidfVectorizer(stop_words='english')
word_matrix.fit(word_data)

# You can access the mapping between words and feature numbers using get_feature_names(), which returns a list of all the words in the vocabulary. How many different words are there?
print len(word_matrix.get_feature_names())
#import pdb;pdb.set_trace()
