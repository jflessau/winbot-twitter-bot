# WinBot
## Requirement
Make sure you have
<a href="https://www.python.org/downloads/">Python</a>
and <a href="https://twython.readthedocs.io/en/latest/usage/install.html">Twython</a> installed on your machine.

## Run it
Switch to the directory and type<br><br>
`$ python winbot.py`<br><br>
into the terminal.

## Connection with Twitter
First thing you need is an app on twitter. You can create it right here: https://apps.twitter.com/<br>
After creating the app, you should get the <b>app_key</b> and the <b>app_secret</b>. To interact with your twitter-account you will have to create the <b>oauth_token</b> and the <b>oauth_token_secret</b>.<br><br>
Follow the steps in the Application Manager to get these.
Now open winbot.py in your favorite editor and copy-paste the keys into it.

## Settings
You can leave everything as it is, or tweak some settings to make this bot fit your needs.<br>
The settings are stored in the `tell_settings`-function:<br>
```def tell_settings():
    settings = {'search_for' : 120, 'cycles': 2, 'sleep' : 135, 'interaction_limit' : 4, 'max-follow' : 2000,
                'max_mentioned_follow' : 3,
                'search_query' : 'rt2win OR retweet to win OR Gewinnspiel OR Verlosung -filter:retweets AND -filter:replies'}
    return settings```

### search_for
This value defines for how many tweets the bot will search for in one cycle. Twitters API provides at max. 150 tweets at a time when searching with a certain query. Because we filter for already retweetet tweets, blacklisted users/strings, retweets and replies, we won’t get as many tweets to retweet as we searched for. But that’s okay, because this bot works in cycles and searches for tweets over and over again, as often as you wish. Choose how often the bot will repeat the search-and-retweet-process by changing the amount of <b>cycles</b>.

### cycles
In one cycle, the bot will searches for tweets to retweet, then retweets these tweets, follows their authors and logs some actions. If you want this bot to do that again and again, just increase the number of cycles.

### sleep
Because Twitter does not provide us with endless data, there are some limits for interactions through twitters api. About 150-180 Interactions in 15 minutes (900seconds) are allowed. The value of <b>sleep</b> represents the amount of seconds the bot will wait, every time the <b>interaction_limit</b> is reached.

### interaction_limit
Every interaction wit twitter is counted. Whenever the <i>interaction_limit</i> is reached, the bot will pause in order to prevent getting blocked by twitter because of exceeding limits.<br>
Play with this value, if you're feeling lucky. Reading the <a href="https://support.twitter.com/articles/355430">rules for twitters limits</a> could help, though.

### max-follow
This value represents the max. amount of users this bot will follow at a time. If reached, the bot will unfollow the user you followed for the longest time. The default for this value is 2000. (Twitter will block users, who follow more than about 4.000 users.)
Unfollowing clearly costs time, but it is essential for this bot to run on the long term without being blocked by twitter.

### max_mentioned_follow
Some twitter contests want you to follow not only one user to be part of it. They mention other users you need to follow in order to participate. Because of that, this bot finds metioned users in tweets and follows them. It’s unlikely that you need to follow more than two or three users for a single contest, therefore you can set the limit for following mentioned users (per tweet) with <b>max_mentioned_follow</b>. If set to zero, no mentioned user will be followed.

### search_query
This string is the actual search query. You can manipulate it and explore, what string works best for you. You can find a guide for building these querys right <a href="https://dev.twitter.com/rest/public/search">here</a>.

## Files
### log.txt
All retweets are logged here. Just so that you can keep an eye on the progress. Also the bot compares the results of a search with all tweets from this log-file. Because of that, this bot won't try to retweet a tweet twice, which saves a lot of time.

### follows.txt
This is where every user you followed is saved. It is elementary for the unfollow-process (explained below).

### blacklisted-users.txt
Here you can manually save names of users (seperated by linebreak) you don't want to interact with. Unfortunately it's not possible to teach a bot to avoid interaction with blocked users. On the other hand the blacklist can be copied and used with multible other bots.
The blacklist is useful, because every unwanted retweet costs time.<br>
In the new folder
<a href="https://github.com/jflessau/winbot-twitter-bot/tree/master/filled-blacklist">filled-blacklist</a>
you can find an alternative blacklisted-users.txt with the most annoying BotSpotterBots in it. I'll try to keep it up to date. If you got new names, please let me know.

### blacklisted-strings.txt
As required by <a href="https://github.com/Darkcast?tab=repositories">Darkcast</a> you can now save strings (e.g. hashtags) in this file (seperated by linebreak). The bot will ignore tweets with those strings.<br>
I’ve added a filled version in the <a href="https://github.com/jflessau/winbot-twitter-bot/tree/master/filled-blacklist">filled-blacklist</a>-folder.


## Additional info

### Why is this bot unfollowing users?
Following to many users at a time can get your bot blocked. Because of that, it also unfollows users (<a href="https://en.wikipedia.org/wiki/FIFO">fifo-princliple</a>).

### It’s kinda time consuming - what can I do about that?
Because of twitters limits, theres not much you can do about that. Let this bot run on a raspberry or arduino, controll it with <a href="https://en.wikipedia.org/wiki/Cron">cron</a> and wait for some prices :)
