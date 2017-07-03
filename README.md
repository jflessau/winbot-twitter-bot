# WinBot
## Requirement
Make sure you have
<a href="https://www.python.org/downloads/">Python</a>
installed on your machine. You will also need <a href="https://twython.readthedocs.io/en/latest/usage/install.html">Twython</a>. <br><br>

## How to run it
Switch to the directory and type<br><br>
`$ python winbot.py`<br><br>
into the terminal.

## Manual
### Connection with your account on twitter
First thing you need is an app on twitter. You can create it right here: https://apps.twitter.com/<br>
After creating the app, you should get the app_key and the app_secret. To interact with your twitter-account you will have to create the oauth_token and the oauth_token_secret. Follow the steps in the Application Manager to get these.
Now open winbot.py in your favorite editor and copy-paste the app_key, app_secret, oauth_token and oauth_token_secret into it. These strings are basically your login password to get into the twitter-app.

### Settings
You can leave everything as it is, or tweak some settings to make this bot fit your needs.<br>
The settings are stored in the `tell_settings`-function. Here’s what they do and why it could be smart to change some:<br>

#### search_for
This value defines for how many tweets the bot will search for in one cycle. Twitters API provides 150 tweets at a time when searching with a certain query. Because we filter for already retweetet tweets, blacklisted users/strings and retweets, we won’t get as many tweets to retweet as we searched for. But that’s okay, because this bot works in cycles and searches for tweets over and over again, if you wish.

#### cycles
In one cycle, the bot will searches for tweets to retweet, then retweets these tweets, follows their authors and logs some actions. If you want this bot to do that again and again, just increase the number of cycles.

#### sleep
Because Twitter does not provide us with endless data, there are some limits for interactions through twitters api. About 150-180 Interactions in 15 minutes (900seconds) are allowed.

#### interaction_limit
Play with this value, if you're feeling lucky. Reading the <a href="https://support.twitter.com/articles/355430">rules for twitters limits</a> could help though.

#### max_mentioned_follow
Some twitter contests want you to follow not only one user to be part of it. They mention other users you need to follow in order to participate. Because of that, this bot finds metioned users in tweets and follows them. Because it’s unlikely that you need to follow more than two or three users for a single contest, you can set the limit for following mentioned users (per tweet) with <b>max_mentioned_follow</b>. If set to zero, no mentioned user will be followed.  

## Files
#### log.txt
All retweets are logged here. Just so that you can keep an eye on the progress. Also the bot compares the results of a search with all tweets from this log-file. Because of that, this bot won't try to retweet a tweet twice, which saves a lot of time.

#### follows.txt
This is where every user you followed is saved. It is elementary for the unfollow-process.

#### blacklisted-users.txt
Here you can manually save names of users (seperated by linebreak) you don't want to interact with. Unfortunately it's not possible to teach a bot to avoid interaction with blocked users. But on the other hand the blacklist can be copied and used with multible other bots.<br>
The blacklist is helpful, because every unwanted retweet costs time.<br> In the new folder
<a href="https://github.com/jflessau/winbot-twitter-bot/tree/master/filled-blacklist">filled-blacklist</a>
you can find an alternative blacklist.txt with the most annoying BotSpotterBots in it. I'll try to keep it up to date. If you got new names, please let me know.

#### blacklisted-strings.txt
As required by <a href="https://github.com/Darkcast?tab=repositories">Darkcast</a> you can now save strings (e.g. hashtags) in this file (seperated by linebreak). The bot will ignore tweets with those strings.


## Additional info

### Why is this bot unfollowing users?
Following to many users at a time can get your bot blocked. Because of that, it unfollows users with the <a href="https://en.wikipedia.org/wiki/FIFO">fifo-princliple</a>.

### It’s kinda time consuming - what can I do about that?
Because of twitters limits, theres not much you can do about that. Let this bot run on a raspberry or arduino, controll it with <a href="https://en.wikipedia.org/wiki/Cron">cron</a> and wait for some prices :)
