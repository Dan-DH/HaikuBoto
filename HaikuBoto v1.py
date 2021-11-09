# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 09:31:24 2021

@author: Daniel Diaz @dan-dh
"""

##HaikuBoto v1##
import praw
import sqlite3
from datetime import datetime
import syllables
import time

#creating a database to save the haikus for posterity
dbCon = sqlite3.connect("RedditBotTest1.db")
cursor = dbCon.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Haikus(
                ID INTEGER PRIMARY KEY,
                Username TEXT,
                Haiku TEXT,
                Date DATE,
                CommentID TEXT,
                SubmissionID TEXT,
                SubmissionTitle TEXT,
                SubName TEXT)"""
                )

#getting the list of commentIDs we have stored in the database to avoid replying twice to same comment
commentIDs = []
request = "SELECT CommentID FROM Haikus;"
cursor.execute(request) 
get_data = cursor.fetchall()
for item in get_data:
    for i_d in item:
        commentIDs.append(i_d)

#connecting to reddit through their API
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
    username="",
    password="",
    )

def haikuboto():
    start = datetime.now()
    #printing the starting time of the script -depending on the number of posts and comments, it can take a long while to run
    print(start)
    #creating an instance of r/all
    subreddit = reddit.subreddit("all")
    
    #haikus have three verses of 5, 7 and 5 syllables
    verses = (5, 7, 5)
    
    #creating a string for each verse
    line1 = ""
    line2 = ""
    line3 = ""
    
    #setting boolean switches to progress through the verses
    first = False
    second = True
    third = True
    
    #we keep found haikus in a list to be printed at the end
    haikuList = []

    #counting how many comments we looked at
    commentCount = 0
    
    #iterating through the top 100 hot posts in r/all
    for post in subreddit.hot(limit=100):
        submission = reddit.submission(id=post.id)
        
        #expanding the 'more comments' links with the actual comment tree
        submission.comments.replace_more(limit=None)
        
        #iterating through the comments in each post
        for comment in submission.comments.list():
            commentCount += 1
            text = comment.body
            
            #links really mess up with the parsing (both the syllable count and
            #they somehow stop haikus from being recognized if they are placed 
            #after a link), so we ignore posts with links alongside posts we 
            #already replied to
            if "http" not in text and comment.id not in commentIDs:
                parseBody = text.split(".")
                parseText = [item.strip() for item in parseBody]
                parseSentence = [item.split(" ") for item in parseText] 
                for sentence in parseSentence:
                    #we only care about sentences that are haiku length
                    if syllables.estimate(" ".join(sentence)) == 17:
                        for word in sentence:
                            #checking if we already completed the first verse, 
                            #and adding a word to the string if not
                            if first == False:
                                line1 += word + " "
                                #checking syllable count after adding the word:
                                #if the verse has more syllables than it should, 
                                #we clear the verse and move onto the next sentence
                                #if it has the correct number of syllables, 
                                #we switch onto the next verse
                                #otherwise we keep adding words
                                if syllables.estimate(line1) > verses[0]:
                                    line1 = ""
                                    break
                                elif syllables.estimate(line1) == verses[0]:
                                    first = True
                                    second = False
                                    continue
                            
                            #same as in the loop above but for the second verse
                            if second == False:
                                line2 += word + " "
                                if syllables.estimate(line2) > verses[1]:
                                    line1 = ""
                                    line2 = ""
                                    break
                                elif syllables.estimate(line2) == verses[1]:
                                    second = True
                                    third = False
                                    continue
                            
                            #same as in the loops above but for the third verse
                            if third == False:
                                line3 += word + " "
                                if syllables.estimate(line3) > verses[2]:
                                    line1 = ""
                                    line2 = ""
                                    line3 = ""
                                    break 
                                elif syllables.estimate(line3) == verses[2]:
                                    third = True 
                      
                            #checking if we have a haiku
                            if first == True and second == True and third == True:
                                #adding the verses to the haiku list to be printed
                                haiku = [line1, line2, line3]
                                haikuList.append("\n".join(haiku))
                                #inserting the data about the comment and the 
                                #user into the database
                                cursor.execute(
                                    """INSERT INTO Haikus(Username,
                                    Haiku,
                                    Date,
                                    CommentID,
                                    SubmissionID,
                                    SubmissionTitle,
                                    SubName)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                                    (                                    
                                    comment.author.name, 
                                    comment.body, 
                                    datetime.strftime(datetime.now(), 
                                                      "%d-%m-%Y %H:%M"),
                                    comment.id, 
                                    submission.id, 
                                    submission.title, 
                                    submission.subreddit.display_name
                                    ))
                                dbCon.commit()
                                #posting the haiku as a reply to the comment
                                comment.reply(f"""A wild haiku appeared!!
                              
   ---  
   >{line1}
    
   >{line2}
    
   >{line3}
      
   ---   
   ^(I'm a boto roboto, beep-bop)""")
                                #being extra careful not to reply twice to the 
                                #same person
                                commentIDs.append(comment.id)
                                #resetting the first verse switch and emptying 
                                #the verses
                                first = False
                                line1 = ""
                                line2 = ""
                                line3 = ""
                                continue
    
    #printing the console the haikus, runtime and number of comments checked
    for haiku in haikuList:
         print(haiku)
    print(datetime.now() - start)
    print("Comments checked for haikus:", commentCount)

while 1:
    haikuboto()
    #time.sleep(60)