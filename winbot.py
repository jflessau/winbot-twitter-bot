import time
import random
import sys



# twitter api connection
from twython import Twython, TwythonError
app_key = "<app_key>>"
app_secret = "<app_secret>"
oauth_token = "<oauth_token>"
oauth_token_secret = "<oauth_token_secret>"
twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)






'''FUNCTIONS'''

def win_things():
    print_settings()
    for i in range(0, tell_settings()['cycles']):
        print '\n\n\nstart cycle: ' +str(i + 1)
        fresh_tweets = search_for_tweets()
        filtered_tweets = filter_tweets(fresh_tweets)
        print 'found ' + str(len(fresh_tweets)) + ' tweets in this cycle'
        print str(len(filtered_tweets)) + ' tweets left after filtering'
        print_line(3)
        get_intimate_with(filtered_tweets)
    print_end()

def get_list(filename):
    result = [];
    file = open(filename, 'r')
    for line in file:
        result.append(line.rstrip('\n'))
    return result

def get_past_retweets():
    result = [];
    file = open('log.txt', 'r')
    for line in file:
        line = line.split(' | ')
        line = line[3]
        result.append(line.replace('\n', ''))
    return result

def search_for_tweets():
    query = tell_settings()['search_query']
    tweets = twitter.search(q=query, result_type='mixed', count=tell_settings()['search_for'])
    fresh_tweets = []
    for tweet in tweets['statuses']:
        fresh_tweets.append(tweet)
    return fresh_tweets

def filter_tweets(tweets):
    tweets = blacklisted_users_filter(tweets)
    tweets = blacklisted_strings_filter(tweets)
    tweets = past_retweets_filter(tweets)
    return tweets

def blacklisted_users_filter(tweet_list):
    result = []
    blacklisted_users = get_list('blacklisted-users.txt')
    for tweet in tweet_list:
        add = True
        for screen_name in blacklisted_users:
            if tweet['user']['screen_name'] == screen_name:
                add = False
        if add == True:
            result.append(tweet)
    return result

def blacklisted_strings_filter(tweet_list):
    blacklisted_strings = get_list('blacklisted-strings.txt')
    result = []
    for tweet in tweet_list:
        add = True
        for string in blacklisted_strings:
            if (tweet_has_string(tweet, string)):
                add = False
        if add == True:
            result.append(tweet)
    return result

def past_retweets_filter(tweet_list):
    past_retweets = get_past_retweets()
    result = []
    for tweet in tweet_list:
        add = True
        for past_retweet_id in past_retweets:
            if str(past_retweet_id) == str(tweet['id']):
                add = False
        if add == True:
            result.append(tweet)
    return result

def tweet_has_string(tweet, str):
    main_str = tweet['text']
    if main_str.lower().find(str.lower()) != -1:
        return True
    else:
        return False

def get_intimate_with(tweet_list):
    limit_counter = len(tweet_list)
    for tweet in tweet_list:
        print '{'
        retweet(tweet)
        follow_author(tweet)
        limit_counter = limit_counter + 3
        followed_num = follow_mentioned(tweet)
        limit_counter += (2 * followed_num)
        if should_we_like_it(tweet):
            limit_counter = limit_counter + 1
            like_this(tweet)
        limit_counter = wait(limit_counter)
        print '}\n\n'

def find_screen_names_in_text(text, max_users):
    result = []
    splitted_status = text.split('@')
    if len(splitted_status) > 1:
        splitted_status.pop(0)
        for part in splitted_status:
            screen_name = part.split(' ');
            screen_name = screen_name[0]
            result.append(screen_name)
        if max_users == 0:
            return result
        else:
            shortened_result = []
            range_end = max_users
            if len(result) < max_users:
                range_end = len(result)
            for i in range(0, range_end):
                shortened_result.append(result[i])
            return shortened_result
    else:
        return []

def retweet(tweet):
    try:
        twitter.retweet(id=tweet['id'])
        print 'retweeted: [tweet_id:' + str(tweet['id']) + ']'
        date_time = (time.strftime("%d-%m-%Y") + " | " + time.strftime("%H:%M:%S"))
        log_entry = str(date_time) + " | RT | " + str(tweet['id']) + " | " + tweet['user']['screen_name']
        add_line(log_entry, 'log.txt')
    except TwythonError as e:
        print 'FAILED to retweet: [tweet_id:' + str(tweet['id']) + ']'

def follow_user(screen_name):
    follows = get_list('follows.txt')
    add = True
    for stored_screen_name in follows:
        if screen_name == stored_screen_name:
            add == False
    if add == True:
        unfollow_add = unfollow_fifo()
        try:
            twitter.create_friendship(screen_name=screen_name)
            add_line(screen_name, 'follows.txt')
            print 'followed ' + screen_name.encode('ascii', 'ignore')
        except TwythonError as e:
            print 'FAILED to follow ' + screen_name.encode('ascii', 'ignore')
        return (unfollow_add + 1)
    else:
        return unfollow_add

def follow_author(tweet):
    followed_num = follow_user(tweet['user']['screen_name'])
    return followed_num

def add_line(str, filename):
    file = open(filename, "r+")
    list= []
    for line in file:
        list.append(line)
    file.write(str + "\n")
    file.close()

def follow_mentioned(tweet):
    screen_names = find_screen_names_in_text(tweet['text'], tell_settings()['max_mentioned_follow'])
    followed_num = 0
    if len(screen_names) > 0:
        for screen_name in screen_names:
            follow_user(screen_name)
    return len(screen_names)

def wait(counter):
    if counter > tell_settings()['interaction_limit']:
        print '---sleep for ' + str(tell_settings()['sleep'])
        time.sleep(tell_settings()['sleep'])
        return 0
    else:
        return counter

def unfollow_fifo():
    followed = get_list('follows.txt')
    if (len(followed) > tell_settings()['max-follow']):
        last_one = followed[(0)]
        followed.pop(0)
        empty_file('follows.txt')
        for line in followed:
            add_line(line, 'follows.txt')
        try:
            twitter.destroy_friendship(screen_name=last_one)
            print 'unfollowed: ' + last_one.encode('ascii', 'ignore')
        except:
            print 'FAILED to unfollow ' + last_one.encode('ascii', 'ignore')
        return 1
    else:
        return 0

def empty_file(filename):
    open(filename, 'w').close()

def print_settings():
    print_line(0)
    print '--------------------------WinBot----------------------------'
    print '************************************************************'
    print 'SETTINGS:\nSearch for ' + str(tell_settings()['search_for']) + ' tweets in each cycle'
    print 'amount of cycles: ' + str(tell_settings()['cycles'])
    print 'sleeps for ' + str(tell_settings()['sleep']) + ' seconds'
    print 'whenever bot interacted ' + str(tell_settings()['interaction_limit']) + ' times with twitter-api'
    print 'follows max. ' + str(tell_settings()['max_mentioned_follow'])  + ' users, who were mentioned in a tweet'
    print '------------------------------------------------------------'

def print_end():
    print '\n\n\n'
    print '------------------------------------------------------------\nDONE'

def should_we_like_it(tweet):
    if (tweet_has_string(tweet, 'like') or tweet_has_string(tweet, 'liking')):
        return True
    else:
        return False;

def like_this(tweet):
    try:
        twitter.create_favorite(id=tweet['id'])
        print 'liked tweet: [tweet_id:' + str(tweet['id']) + ']'
    except TwythonError as e:
        print 'FAILED to like tweet: [tweet_id:' + str(tweet['id']) + ']'

def print_line(breaks):
    print '------------------------------------------------------------'
    for i in range(0, breaks):
        print '\n'





'''SETTINGS'''

def tell_settings():
    settings = {'search_for' : 120, 'cycles': 2, 'sleep' : 135, 'interaction_limit' : 4, 'max-follow' : 2000,
                'max_mentioned_follow' : 3,
                'search_query' : 'rt2win OR retweet to win OR Gewinnspiel OR Verlosung -filter:retweets AND -filter:replies'}
    return settings






'''MAIN'''

# start winning
win_things()
