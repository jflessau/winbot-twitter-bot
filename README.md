# WinBot
## Required
Make sure you have
[Python](https://www.python.org/downloads/)
and [Twython](https://twython.readthedocs.io/en/latest/usage/install.html) installed on your machine.


### Connection with Twitter
You will need an app on twitter. You can create it right here: [https://apps.twitter.com/](https://apps.twitter.com/)    
Now copy the

- app_key
- app_secret
- oauth_token
- oauth_token_secret

into `winbot.py`.



## Run it
`$ python winbot.py`



## Settings
Have a look at the `tell_settings`-function in `winbot.py` and tweak some settings to make this bot fit your needs. [Use with caution](https://developer.twitter.com/en/docs/basics/rate-limits).


| var | purpose |recommended value |
|-----|---------|----------------------|
|**search_for**|tweets to search for in one cycle|20-120|
|**cycles**|cycles (1 cycle = search for tweets, retweet, like, follow, unfollow)|>1|
|**sleep**|seconds to wai when **interaction_limit** is reached|>120|
|**interaction_limit**| interactions with API in a row (followed by **sleep**)|20-120|
|**max_follow**| max. amount of users followed at a time |<4000|
|**max_mentioned_follow**| max. amount of users mentioned in a tweet to follow |<4|
|**search_query**| query used to search for tweets |*something related to giveaways*|


## Blacklists
### User
You can manually save more names of users (seperated by linebreak) you don't want to interact with. Unfortunately it's not possible to teach a bot to avoid interaction with blocked users. On the other hand the blacklist can be copied and used with multible other bots.
The blacklist is useful, because every unwanted retweet costs time.  

In case you got some more names, don’t hesitate to contribute them!

### Strings
As required by [Darkcast](https://github.com/Darkcast?tab=repositories) you can now save strings (e.g. hashtags) in this file – seperated by linebreak. The bot will ignore tweets with those strings.



## Additional info

### Why is this bot unfollowing users?
Following too many users at a time can get your bot blocked. Because of that, it also unfollows users ([fifo-princliple](https://en.wikipedia.org/wiki/FIFO)).

### It’s kinda time consuming - what can I do about that?
Theres not much you can do about that. Let this bot run on a raspberry or arduino, control it with [cron](https://en.wikipedia.org/wiki/Cron) and wait for some prices :)

## Donate
Did you win cool stuff? Feel free to throw some cash for a beer into my direction:  
[Donate](https://paypal.me/jflessau)
