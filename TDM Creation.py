# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:58:00 2023

@author: morid
"""

import json
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import numpy as np

f = open('D:/MSDS/Database Management/Project/corona-out-3_data', 'r')

tweets = {}
texts = {}
users = {}
hashtags = {}

tweet_keys = ['created_at', 'id_str', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count']
user_keys = ['name', 'screen_name', 'verified', 'followers_count', 'friends_count', 'created_at']

rts = []

for line in f:
    if line == '\n':
        continue
    lx = json.loads(line)
    li = dict((k, lx[k]) for k in tweet_keys if k in lx)
    li['user'] = lx['user']['id']
    
    if not 'retweeted_status' in lx or len(lx['retweeted_status']) == 0:
        li['retweet'] = False
        if 'extended_tweet' in lx:    
            thisText = lx['extended_tweet']['full_text']
        else:
            thisText = lx['text']
        li['text'] = thisText
        texts[lx['id']] = thisText
        hashtag_set = set(part[1:] for part in thisText.split() if part.startswith('#'))
        li['hashtags'] = hashtag_set
        for hashtag in hashtag_set:
            if hashtag in hashtags.keys():
                hashtags[hashtag].append(lx['id'])
            else:
                hashtags[hashtag] = [lx['id']]
    else:
        li['retweet'] = True
        li['original_tweet'] = lx['retweeted_status']['id']
    tweets[lx['id']] = li
    if not lx['user']['id'] in users.keys():
        users[lx['user']['id']] = dict((k, lx['user'][k]) for k in user_keys if k in lx['user'])

f.close()

vectorizer = CountVectorizer(token_pattern=r"(?u)\b[a-z][a-z]+\b", stop_words=stopwords.words('english'), min_df = 500)

X = np.transpose(vectorizer.fit_transform(texts.values()))

key_list = [*texts.keys()]
word_list = [*vectorizer.get_feature_names_out()]

X

x1 = X.toarray()

x2 = dict((word_list[w], [key_list[t] for t in np.where(x1[w]>0)[0]]) for w in range(len(x1)))


with open("overall_tdm.json", "w") as outfile:
    json.dump(x2, outfile, indent=2)

with open("hashtag_tdm.json", "w") as outfile:
    json.dump(hashtags, outfile, indent=2)


# upload tweets, x2 to mongodb, users to mysql



# s1 = [sum(i>0) for i in x1]

# s1 = [np.log(i) for i in s1]

# from matplotlib import pyplot as plt

# fig, ax = plt.subplots(figsize =(10, 7))
# ax.hist(s1)

