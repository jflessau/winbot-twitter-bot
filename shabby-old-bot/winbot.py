import time
import random
import sys



#TWITTER API CONNECTION
from twython import Twython, TwythonError
app_key = "YOUR___app_key"
app_secret = "YOUR___app_secret"
oauth_token = "YOUR___oauth_token"
oauth_token_secret = "YOUR___oauth_token_secret"
twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)






'''FUNCTIONS'''

#printe messages w/ some style
def announce_step(message):
    print("########################")
    print(message)
    print("########################")



#wait so we're good with the api
def wait_for_it():
    time.sleep(seconds())



#adds line to .txt-file
def add_line(zeile, datei):
    file = open(datei, "r+")
    list= []
    for line in file:
        list.append(line)
    file.write(zeile + "\n")
    file.close()



#start to retweet in cycles
def retweet_action(counter, iter, secs):
    if iter > 0:
        iter -= 1
        retweets = get_retweets()
        tweets = get_tweets(counter)
        retweets_to_do = []
        for t in tweets:
            in_list = 0
            for r in retweets:
                if (t == r.rstrip('\n')):
                    in_list = 1
                    break
                else:
                    in_list = 0
            if (in_list == 0):
                retweets_to_do.append(t)
        amount_retweets = len(retweets_to_do)
        print("----------")
        print("Will retweet " + str(amount_retweets) + " Tweet(s)")
        print("Estimated time to finish this cycle: " + str(((amount_retweets * secs))/60) + " Minutes...")
        print(str(iter + 1) + " Cycles left.")
        print("----------")
        do_retweets_to(retweets_to_do, counter, iter)



#get old retweets from Log
def get_retweets():
    try:
        file = open("log.txt", "r")
        log_list = open("log.txt").readlines()
        retweet_ids = []
        for i in log_list:
            parts_list =str.split(i, ' | ')
            retweet_ids.append(parts_list[3])
    except:
        print("ERROR while reading log file.")
        print("Empty retweet-list used instead.")
        retweet_ids = []
    return retweet_ids



#search for tweets to retweet to
def get_tweets(counter):
    blacklist = get_blacklist()
    keywords = "rt2win OR retweet to win OR Gewinnspiel OR Verlosung -filter:retweets AND -filter:replies"
    search_results = twitter.search(q=keywords, result_type= "recent", count=counter)
    tweet_ids = []
    try:
        for tweet in search_results["statuses"]:
            add_tweet = True
            for name in blacklist:
                tweeter = tweet["user"]["screen_name"]
                if (name.rstrip('\n') == tweeter):
                    add_tweet = False
            if (add_tweet == True):
                tweet_ids.append(str(tweet["id_str"]))
    except TwythonError as e:
        print e
    return tweet_ids



#retweet tweets from task-list, follow users and log actions
def do_retweets_to(retweet_list, counter, iter):
    for tweet_ids in retweet_list:
        try:
            tweet = twitter.show_status(id = tweet_ids)
            user_id = tweet["user"]["id_str"]
            screenname = tweet["user"]["screen_name"]
            twitter.retweet(id = tweet_ids)
            try:
                twitter.create_friendship(user_id = user_id)
                add_line(screenname, "follows.txt")
            except TwythonError as e:
                print("Follow-Error: ")
                print e
            datum_zeit = (time.strftime("%d-%m-%Y") + " | " + time.strftime("%H:%M:%S"))
            log_entry = str(datum_zeit) + " | RT | " + tweet_ids + " | " + screenname
            add_line(log_entry, "log.txt")
            wait_for_it()
        except TwythonError as e:
            print ("Retweet-Error: " + tweet["user"]["screen_name"])
            print e
            wait_for_it()
    retweet_action(counter, iter, seconds())



#get list of users we don't like (mainly botspotters)
def get_blacklist():
    file = open("blacklist.txt", "r")
    blacklist = file.readlines()
    file.close()
    if (len(blacklist) > 0):
        return blacklist
    else:
        empty_list = []
        return empty_list



#start to unfollow users
def unfollow_action(unfollow_counter, max):
    user_names = get_followed_users(unfollow_counter, max)
    if (len(user_names) > 0):
        print ("Unfollow " + str(len(user_names)) + " user(s)")
        print("----------")
    else:
        print("Not going to unfollow. Max. amount of followed users not reached.")
        print("----------")
    for entry in user_names:
        try:
            twitter.destroy_friendship(screen_name= entry)
        except TwythonError as e:
            print e
        wait_for_it();



#read log to get followed users
def get_followed_users(unfollow_counter, max):
    file = open("follows.txt", "r")
    followed_user_list = file.readlines()
    to_unfollow_list = []
    file.close()
    if (len(followed_user_list) > max):
        for x in range(0, unfollow_counter):
            to_unfollow_list.append(followed_user_list[0])
            followed_user_list.pop(0)
            file = open("follows.txt", "w")
            for z in followed_user_list:
                file.write(z)
            file.close()
        return to_unfollow_list
    else:
        empty_list = []
        return empty_list






'''CONFIG'''

#time to wait between actions (at leat 100 seconds are recommended)
def seconds():
    return 180
#amount of tweets to search for in one cycle
counter= 45

#search cycle iterations (counter * retweet_iter = amount of retweets)
retweet_iter = 5

#amount of max. followed accounts (if you follow more, unfollow_action will be executed)
follow_max = 2000

#amount of users to unfollow if follow_max is reached
unfollow_counter = counter * retweet_iter






'''MAIN'''

#tell that Bot is running
announce_step("Bot is running...")

#calculate amount of time required to finish programm (worst case)
print("----------")
print("Max. Time for Bot to process given tasks: " + str((counter*retweet_iter+unfollow_counter)*seconds()/60/60) + "h")

#bot starts to search for tweets to retweet to, then retweets, then repeat toll no cycles are left
retweet_action(counter, retweet_iter, seconds())

#bot starts to unfollow users if you follow more than follow_max
unfollow_action(unfollow_counter, follow_max)

#tell that bot stopped
announce_step("Bot has stopped.")
