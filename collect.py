"""
collect.py
"""

from collections import Counter, defaultdict
from TwitterAPI import TwitterAPI
import time
import pickle
import signal
from threading import Thread, Condition
from multiprocessing import Queue
import sys
import json
import threading
import numpy as np

queueSize = 500
queue = Queue(queueSize)
twitter_rate_limit = Condition()
#Filename
CLASSIFY_FILE_NAME= "classify_data.json"
CLASSIFY_FRIEND_NAME= "classify_friend.json"

# Service Tokens
consumer_key = 'ftwgjnC4SR8U4lEPNHqNKiNCV'
consumer_secret = 'DiIXS7Z0NkrYgtes9zbD666AwhJiC9AM4lBTuv8aMrKOAb7jBC'
access_token = '596398510-mYstiQ7CekWvoqXsDKdi7CxxaRgiGlTsgsnigT5z'
access_token_secret = 'i5a2c5379p1UCCYbJfLnkEdIycDRuR9YvjLvzHCxSA410'


class CreateData(Thread):
    def __init__(self, run_event, service, keywords,file):
        self.run_event = run_event
        self.service = service
        self.comments = self.robust_request(self.service,'statuses/filter', {'language': 'en', 'track': keywords})
        self.file = file
        Thread.__init__(self)
        
    def run(self):
        global queue
        for comment in self.comments:
            if not self.run_event.is_set():
                break
            try:
                print(comment['text'])
            except:
                continue
            queue.put(comment)
            data = {}
            data["tweet"] = comment["text"]
            data["created_at"] = comment["created_at"]
            data["user_name"] = comment['user']["screen_name"]
            data["user_id"] = str(comment['user']["id"])
            data["location"] = comment['user']["location"]
            json.dump(data, self.file)
            self.file.write("\n")
            
    def robust_request(self, twitter, resource, params, max_tries=5):
        for i in range(max_tries):
            request = twitter.request(resource, params)
            if request.status_code == 200:
                return request
            else:
                print('Got error %s \nsleeping for 15 minutes.' % request.text)
                sys.stderr.flush()
                twitter_rate_limit.acquire()
                twitter_rate_limit.wait(61 * 15)
                twitter_rate_limit.release()
                if not self.run_event.is_set():
                    break

class CollectFriendData(Thread):
    def __init__(self, run_event, service, keywords, file):
        self.run_event = run_event
        self.service = service
        self.users_file = file
        Thread.__init__(self)
        
    def run(self):
        global queue
        while self.run_event.is_set():
            comment = queue.get()
            user_id = comment['user']['id']
            request = self.robust_request(self.service, "friends/ids", {'user_id': user_id})
            if request is None:
                continue
            data = {}
            data["user_id"] = str(comment['user']["id"])
            data["user_name"] = comment['user']["screen_name"]
            data["friends"] = list(request)
            json.dump(data, self.users_file)
            self.users_file.write("\n")      
            
            
    def robust_request(self, twitter, resource, params, max_tries=5):
        for i in range(max_tries):
            request = twitter.request(resource, params)
            if request.status_code == 200:
                return request
            else:
                print('Got error %s \nsleeping for 15 minutes.' % request.text)
                sys.stderr.flush()
                twitter_rate_limit.acquire()
                twitter_rate_limit.wait(61 * 15)
                twitter_rate_limit.release()
                if not self.run_event.is_set():
                    break

def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        x = input("Please keywords you want to have use for analysis in one line using commas\n (Recommanded related keywords for better search) \n").split(',')
        keywords = np.asarray(x)
        return keywords
    if reply[0] == 'n':
        return True 
    else:
        return yes_or_no("Uhhhh... please enter y or n ")
pass

def main():
    run_event = threading.Event()
    run_event.set()
    service = TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)
    file1 = open(CLASSIFY_FILE_NAME, "w")
    file2 = open(CLASSIFY_FRIEND_NAME,"w")
    keywords = ["Avengers End Game", "Avengers", "End Game", "MCU" , "Marvel", "Marvel Cinematic Universe", "Iron Man","Thanos", "Hulk"]
    answer = yes_or_no("This Analysis shows results for 'Avengers:EndGame' movie, Do you want to try something else?")
    if(isinstance(answer,np.ndarray)):
        keywords = answer
    collect_comments = CreateData(run_event, service, keywords,file1)
    collect_friends = CollectFriendData(run_event, service, keywords, file2)
    try:
        collect_comments.start()
        collect_friends.start()
    except:
        run_event.clear()
        twitter_rate_limit.acquire()
        twitter_rate_limit.notify()
        twitter_rate_limit.release()
        collect_comments.join()
        collect_friends.join()
        file1.close()
        file2.close()
        sys.exit()
        quit()
    try:    
        while queue.qsize() < queueSize:
            time.sleep(.1)
        raise Exception("Exit")
    except Exception:
        print("Data Collected! Exiting")
        run_event.clear()
        twitter_rate_limit.acquire()
        twitter_rate_limit.notify()
        twitter_rate_limit.release()
        collect_comments.join()
        collect_friends.join()
        file1.close()
        file2.close()
        sys.exit()
        quit()
       
    
if __name__ == '__main__':
    main()
