# HaikuBoto

## A poetic Reddit bot

<img src="https://github.com/Dan-DH/HaikuBoto/blob/main/screenshot.PNG?raw=true" alt="Haiku" width="800"/>

### What is HaikuBoto?

HaikuBoto is a Reddit bot written in Python. It combs through the comments of the hottest posts in r/all, looking for phrases that are 17 syllables long.

If the comment can be divided into three verses of 5-7-5 syllables without splitting words in half, HaikuBoto will reply to the comment with the formatted haiku. It will also log the comment and user ID of the author in a SQLite database for posterity.

### Why is HaikuBoto?

    There would be lots

    of pitter pattering as

    they walked across
    
      /u/PumpkinSpice2Nice

Because sometimes people write poetry without realizing it, and you get to put a smile on their faces by pointing it out. Also, I needed to practice Python.

### I want to use HaikuBoto

Fork it and run it! You will need a Reddit account and a [Reddit Api key](https://www.reddit.com/wiki/api). You will have to add the account and key credentials to the script so HaikuBoto can connect to Reddit. You can do so on lines 38 to 45 of the script.

The subreddit and the number of posts to check can be modified in lines 52 and 74 respectively. By default it checks the comments of the first 100 posts o r/all, filtered by hot.

You will need to comment out the SQLite parts, unless you are setting up your own database.

### Hey, this haiku has 16 syllables!

Good eye! Turns out it is actually tricky to accurately count syllables in English. HaikuBoto uses [syllables](https://pypi.org/project/syllables/) by David L Day for the syllable count. It works well most of the time, but it has a tendency to count one syllable words like 'there' as two syllables.

<image src="https://media1.giphy.com/media/k5lj4s1qxaSyI/giphy.gif?cid=ecf05e475t1ri8pnyxmnuz7kjez36n51rwek45rezlbcteae&rid=giphy.gif&ct=g" width="400" height="200"/>
