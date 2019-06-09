"""
Classify data.
"""
import json
import re
from collections import Counter
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

CLASSIFY_FILE_NAME= "classify_data.json"

def read_file(filename):
    """
    Reading data from file
    """
    array = []
    with open(filename) as f:
        for line in f:
            array.append(json.loads(line))
    return array
    pass

def get_tokens(tweets):
    
    tokens = []
    for tweet in tweets:
        tweet["token"] = []
        text = tweet['tweet'].lower()
        text = re.sub('@\S+', ' ', text)  # Remove mentions.
        text = re.sub('http\S+', ' ', text)  # Remove urls.
        token = re.findall('[A-Za-z]+', text)
        tokens.append(token) # Retain words.
        #print(token)
        tweet["token"] = token
    return tokens
    pass

def purne_token(tweets, wordCount):
    word_counts = Counter()
    for tweet in tweets:
        word_counts.update(tweet["token"])
    # Retain in vocabulary words occurring more than wordCount.
    vocab = set([w for w, c in word_counts.items() if c > wordCount])
    newtoks = []
    for i, tweet in enumerate(tweets):
        newtok = [token for token in tweet["token"] if token in vocab]
        if len(newtok) > 0:
            newtoks.append(newtok)
           
    return newtoks
    pass

def download_afinn():
    url = urlopen('http://www2.compute.dtu.dk/~faan/data/AFINN.zip')
    zipfile = ZipFile(BytesIO(url.read()))
    afinn_file = zipfile.open('AFINN/AFINN-111.txt')
    afinn = dict()

    for line in afinn_file:
        parts = line.strip().split()
        if len(parts) == 2:
            afinn[parts[0].decode("utf-8")] = int(parts[1])
    print("read %d AFINN terms." %(len(afinn)))
    return afinn

def afinn_posneg(terms, afinn, verbose=False):
    pos = 0
    neg = 0
    for t in terms:
        if t in afinn:
            if verbose:
                print('\t%s=%d' % (t, afinn[t]))
            if afinn[t] > 0:
                pos += afinn[t]
            else:
                neg += -1 * afinn[t]
    return pos, neg

def afinn_sentiment(tweets, afinn):
    for u in tweets:
            u['pos'], u['neg'] = afinn_posneg(u['token'], afinn) 
            sentiment = "balanced"
            if u['pos'] < u['neg']:
                sentiment = "negative"
            else:
                sentiment = "positive"
            u['sentiment'] = sentiment
    pass

def main():
    tweets = read_file(CLASSIFY_FILE_NAME)
    print("Tweets has been read!")
    tokens = get_tokens(tweets)
    purned_tokens = purne_token(tweets,2)
    afinn = download_afinn()
    afinn_sentiment(tweets, afinn)
    negative_tweets = [u for u in tweets if u['sentiment'] == "negative"]
    positive_tweets = [u for u in tweets if u['sentiment'] == "positive"]
    print("In total ",len(tweets)," tweets \n The negative tweets are: ",len(negative_tweets), "\n The positive tweets are: ",len(positive_tweets))
    file = open("sentiment_data.json","w")  
    json.dump(tweets,file)
    file.close()
    pass

if __name__ == "__main__":
    main()