# WinBot

## How to run this bot
Reading the Manual before starting this bot is strongly recommended.<br>
Make sure you have
<a href="https://www.python.org/downloads/">Python</a>
installed on your machine. You will also need <a href="https://twython.readthedocs.io/en/latest/usage/install.html">Twython</a>. <br><br>
Now you're ready to run the python script. Switch to the directory and type<br><br>
`$ python winbot.py`<br><br>
into the terminal.

## Manual
### Connection with your account on twitter
First thing you need is an app on twitter. You can create it right here: https://apps.twitter.com/<br>
After creating the app, you should get the app_key and the app_secret. To interact with your twitter-account you will have to create the oauth_token and the oauth_token_secret. Follow the steps in the Application Manager to get these.
Now open winbot.py in your favorite editor and copy-paste the app_key, app_secret, oauth_token and oauth_token_secret into it. These strings are basically your login password to get into the twitter-app.

### Configuration
Under the line that says '''Config''' (in winbot.py) you can configure the way this bot works for you. It's not necessary to change something, but it could be helpful.<br>
You can modify the values for **seconds**, **counter**, **retweet_iter** and **follow_max**.
#### seconds
Is the time in seconds this bot will wait between it's interactions with the twitter api. It's set to 180 by default. We don't want to strain twitter too much, so I don't recommend to lower this value any further.
#### counter
Is the amount of tweets the bot will search for in one cycle. The search-query used to search for tweets about for example giveaways, is located in the function called "get_retweets". The api only allows to search for 150 tweets or less. So keep this value lower than 150.
#### retweet_iter
Is the amount of cycles. In one cycle this bot searches for tweets to retweet to and then executes the retweet and follows the user.<br>
The bot works in cycles, because, as I mentioned earlier, the api delivers max. 150 tweets per search. If you want the bot to work with more than 150 tweets, then the cycles are needed to repeat the search until enough tweets are found.
#### follow_max
Is set to 2000 by default. The bot saves a list of who it followed in follows.txt. If you reach this amount of followed users, the bot will start to unfollow as many users as it followed in the actual run. It will start with the first one followed, so that you can follow users as long as possible in order to still be following when a potential giveaway ends. (If you follow too many users, your twitter app will be blocked.)
### Time-Management
Remember: This bot needs a certain amount of time to run. The estimated time needed to execute all orders is printed to the terminal after you have started the bot. It is calculated like so:<br>
[(**seconds** * **counter** * **retweet_iter**) * 2 / 3600] = Time in hours.<br>
If you want to start the bot automatically every day, keep in mind that the estimated time to execute should be less than 24h.<br>
You will need an external tool to start this bot at a certain time. For example <a href="https://help.ubuntu.com/community/CronHowto">cron</a>.


## Files
#### log.txt
All retweets are logged here. Just so that you can keep an eye on the progress. Also the bot compares the results of a search with all tweets from this log-file. Because of that, this bot won't try to retweet a tweet twice, which saves a lot of time. 
#### follows.txt
This is where every user you followed is saved. This file is elementary for the unfollow-process.
#### blacklist.txt
Is where you can manually save names of users you don't want to interact with. Unfortunately it's not possible to teach a bot to avoid interaction with blocked users. But on the other hand the blacklist can be copied and used with multible other bots. The blacklist is helpful, because every unwanted retweet costs time. If the search function returns some tweets from users on the blacklist, the bot won't interact with them, which saves time. In the new folder
<a href="https://github.com/jflessau/winbot-twitter-bot/tree/master/filled-blacklist">filled-blacklist</a>
you can find a alternative blacklist.txt with the most annoying BotSpotterBots in it. I'll try to keep it up to date. If you got new names, please let me know. 
