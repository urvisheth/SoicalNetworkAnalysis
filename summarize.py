"""
Summarize data.
"""
import json
import networkx as nx
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

def read_txt(filename):
    """
    Reading data from file
    """
    array = []
    with open(filename) as f:
        for line in f:
            array.append(line)
    return array
    pass


def main():
	file_collect = read_file("classify_data.json")
	file_friends = read_file("classify_friend.json")
	file_cluster = read_txt("cluster_data.txt")
	file_classify = read_file("sentiment_data.json")
	print("\n Number of users collected:", len(file_friends))
	print("\n Number of messages collected:",len(file_collect))
	print("\nNumber of communities discovered:", len(file_cluster))
	for i in range(0,len(file_cluster)):
		print("Cluster ", i , " number of elements " , len(file_cluster[i]))
	negative_tweets = []
	positive_tweets = []
	balanced_tweets = []
	for u in file_classify:
		for i in u:
			if i['sentiment'] =="negative":
				negative_tweets.append(i)
			elif i["sentiment"] == "positive":
				positive_tweets.append(i)
	print("Number of instances per class", len(file_collect))
	print("Tweets \n The negative tweets are: ",len(negative_tweets), "\n The positive tweets are: ", len(positive_tweets), "\n The balanced tweets are: ",len(balanced_tweets))
 	#print("Number of instances per class found ",len(file_collect))
 	#print(" tweets \n The negative tweets are: ",len(negative_tweets), "\n The positive tweets are: ", len(positive_tweets), "\n The balanced tweets are: ",len(balanced_tweets))
	print("One example from each class:")
	print("negative:", negative_tweets[0])
	print("\n\npositive:", positive_tweets[0])
	pass

if __name__ == "__main__":
    main()