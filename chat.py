from fnmatch import translate
import json
import string

def chatbot(user_input):
    file = open('chat_bot.json') # Open Script json
    script = json.load(file) # Load script into variable

    for i in script: # For each group in script
        for x in script[i]["Input"]: # For each accepted input in the group 
            if x == (user_input.lower()).translate(str.maketrans("", "", string.punctuation)): # If input is same as lowercase input without punct
                return i, script[i]["Output"] # Return the output