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
retweets = {}
replies ={}
texts = {}
users = {}
hashtags = {}

# The specific keys to extract for tweets and users
tweet_keys = ['created_at', 'id_str', 'reply_count', 'retweet_count']
user_keys = ['name', 'screen_name', 'verified', 'followers_count', 'friends_count', 'created_at']

# Iterating over the input file
for line in f:
    if line == '\n':
        continue
    lx = json.loads(line)
    
    # Main extraction only for non-retweets
    if not 'retweeted_status' in lx or len(lx['retweeted_status']) == 0:
        li = dict((k, lx[k]) for k in tweet_keys if k in lx)
        # Store user ID and user screen name
        li['user'] = lx['user']['id']
        li['user_name'] = lx['user']['screen_name']
        
        # In some cases, text is truncated - here, extended_tweet full_text will contain the full version
        # If available, we use that, else the main text field is not truncated so we can use it
        if 'extended_tweet' in lx:    
            thisText = lx['extended_tweet']['full_text']
        else:
            thisText = lx['text']
        
        # Store the text (from whichever source) in both the tweet and the data source for keyword extraction
        li['text'] = thisText
        texts[lx['id']] = thisText
        
        # Identify hashtags using regex
        # The hashtags under entities are built from the main text field, which may have been truncated
        # So that subfield may be inaccurate
        hashtag_set = list(set(part[1:] for part in thisText.split() if part.startswith('#')))
        li['hashtags'] = hashtag_set
        li['hashtag_count'] = len(hashtag_set)
        
        # Track tweet IDs by hashtag, for later mapping
        for hashtag in hashtag_set:
            if hashtag in hashtags.keys():
                hashtags[hashtag].append(lx['id'])
            else:
                hashtags[hashtag] = [lx['id']]
        
        # Store this set of tweet details under this tweet ID
        tweets[lx['id']] = li
        
        # Track replies against their original tweets
        if 'in_reply_to_status_id' in lx:
            if not lx['in_reply_to_status_id'] in replies.keys():
                replies[lx['in_reply_to_status_id']] = 1
            else:
                replies[lx['in_reply_to_status_id']] = replies[lx['in_reply_to_status_id']] + 1
    else:
        # If a retweet, track against the original tweet
        orig_id = lx['retweeted_status']['id']
        
        if not orig_id in retweets.keys():
            retweets[orig_id] = 1
        else:
            retweets[orig_id] = retweets[orig_id] + 1
    
    # If this user has not been seen before, add their details into the user list
    if not lx['user']['id'] in users.keys():
        users[lx['user']['id']] = dict((k, lx['user'][k]) for k in user_keys if k in lx['user'])

f.close()

# Map retweets and replies to their original tweets, with counts
for rt in retweets.keys():
    if rt in tweets.keys():
        tweets[rt]['retweet_count'] = retweets[rt]

for rt in replies.keys():
    if rt in tweets.keys():
        tweets[rt]['reply_count'] = replies[rt]


# Extract unigrams, removing stopwords, for all keywords that appear at least 50 times
vectorizer = CountVectorizer(token_pattern=r"(?u)\b[a-z][a-z]+\b", stop_words=stopwords.words('english'), min_df = 50)

X = vectorizer.fit_transform(texts.values())

# The list of IDs and keywords used in the vectorizer
key_list = [*texts.keys()]
word_list = [*vectorizer.get_feature_names_out()]

# Track the number of keywords mapped to each ID, and store the count with the tweet details
x1 = X.toarray()

x2 = dict((key_list[w], len([word_list[t] for t in np.where(x1[w]>0)[0]])) for w in range(len(x1)))

for key_id in x2.keys():
    if key_id in tweets.keys():
        tweets[key_id]['keyword_count'] = x2[key_id]

# Track the IDs associated with each keyword, and store the mapping
X = np.transpose(X)

x1 = X.toarray()

x2 = dict((word_list[w], [key_list[t] for t in np.where(x1[w]>0)[0]]) for w in range(len(x1)))


# Upload tweets dict to MongoDB
# Upload users dict to MySQL

# Upload TDMs (x2, hashtags) to MongoDB
with open("overall_tdm.json", "w") as outfile:
    json.dump(x2, outfile, indent=2)

with open("hashtag_tdm.json", "w") as outfile:
    json.dump(hashtags, outfile, indent=2)


# Temp plots to explore
# s1 = [sum(i>0) for i in x1]

# s1 = [np.log(i) for i in s1]

# from matplotlib import pyplot as plt

# fig, ax = plt.subplots(figsize =(10, 7))
# ax.hist(s1)
