# Online Social Network Data Analysis

This project takes information from Twitter about the tweets regarding the movie "Avengers: End game" which is a marvel MCU movie.

The motto of doing this is it can help to know the liking or disliking the users for the movie and which kind of users are interested in the movie and how they are connected.

**The Best perk of this project is you can use it for analysis of any other topic, you just need to change keywords and twitter query search for it**

The project works in four modules, which are
1. **Collected** raw data from some online social networking site like Twitter
2. Perform **community detection** to cluster users into communities.
3. Perform **supervised classification** to annotate messages and/or users according to some criterion.
4. Analyze the results and **summarize** your conclusions.

To run, the following commands:
```
python collect.py
python cluster.py
python classify.py
python summarize.py
```

Here is what each script does:

- `collect.py`: This collects data used in the analysis. This submits queries to Twitter. The data is raw and comes directly from the original source. Running this script will create a file or files containing the data that you need for the subsequent phases of analysis. This file collects data from Twitter using status/filter and keywords related to the movie are given, that will get all the tweets, now according to tweets, the friend of users are found and that data is saved in classify_friend.json, Tweets are stored in classify_data.json
 
 **This File Will Take 30-45s~ to Run, depending on the system**


- `cluster.py`: This reads the data collected in the previous step and use a community detection algorithm to cluster users into communities. This will cluster that data according to the user name and their friend id from classify_friend.json, and clustering will be done using partition nerwan method and BFS tree. the cluster image is produced and data is stored in cluster_data.txt

- `classify.py`: This classifies data along with the sentiment. This method uses supervised learning, which means you may have a second array containing any labeled data for the problem. This will take tweets from classify_data.json, will load sentiment words from AFFIN data and find the sentiment for the tweets. 

- `summarize.py`: This reads the output of the previous methods to write a text file called `summary.txt` containing the following entries:
  - The number of users collected:
  - The number of messages collected:
  - The number of communities discovered:
  - The average number of users per community:
  - The number of instances per class found:
  - One example from each class:


Other notes:

- Use of any non-standard libraries is included a list of the library names in a file `requirements.txt`. To install that, use the command `pip install -r requirements.txt`.
