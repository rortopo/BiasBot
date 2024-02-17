# bot framework by Rory McCann
# LLM training/integration and prompts by Chase Lahner
# MongoDB wizardry by Ivan Puri
from json import loads

import discord
from discord.ext import commands
from transformers import pipeline
import mongoConnect
import botWork

intents = discord.Intents.all()  # cannot be all when we're done
dsClient = discord.Client(intents=intents)  # discord bot privileges
ivancert = 'Certification PathFile'
rorycert = "certification PathFile"

mongo = mongoConnect.Backend("Cluster uri", ivancert)  # mongo methods class instantiation
ot = botWork.botCommands("username","password")  # bot class instantiation
pipe = pipeline("text-classification", model="unitary/toxic-bert", tokenizer="bert-base-uncased", top_k=None)

with open("eduPrompt.json", "r") as file:  # flag word list
    educationalPrompt = loads(file.read())

@dsClient.event  # bot startup command
async def on_ready():
    print(f'We have logged in as {dsClient.user}')


def getBiggestHateScore(classification: list) -> str: # TODO put in another file
    toxic = classification[0][0]['score']
    obscene = classification[0][1]['score']
    insult = classification[0][2]['score']
    identity_hate = classification[0][3]['score']
    severe_toxic = classification[0][4]['score']
    threat = classification[0][5]['score']
    
    if(threat > 0.75):
        return 'threat. Threats are extremely harmful, and even if they are not serious they can cause serious consequences, including potential criminal implications. Threats are never acceptable, no matter if you are joking or not'
    if(identity_hate > 0.75):
        return 'identity_hate. Identity hate is extraordinarily harmful language, and is not tolerated. Identity hate is a form of hate speech, and in some cases can be criminally prosecuted.'
    if(severe_toxic > 0.75):
        return 'severe_toxic. Being severely toxic can be harmful to creating a welcoming community. Please avoid doing so again.'
    if(insult > 0.75):
        return "insult. Insults can seriously hurt someones feelings, even if it wasn't intentional."
    if(obscene > 0.75):
        return 'obscene. Obscene comments are not tolerated, and can be extraordinarily harmful.'
    if(toxic > 0.75):
        return "toxic. Being toxic creates a non-welcoming environment, which isn't tolerated."
    else:
        return 'Implicit/Other'

def getCategory(classification: list) -> str: # TODO put this in another file
    toxic = classification[0][0]['score']
    obscene = classification[0][1]['score']
    insult = classification[0][2]['score']
    identity_hate = classification[0][3]['score']
    severe_toxic = classification[0][4]['score']
    threat = classification[0][5]['score']
    
    if(threat > 0.75):
        return 'threat' 
    if(identity_hate > 0.75):
        return 'identity_hate'
    if(severe_toxic > 0.75):
        return 'severe_toxic'
    if(insult > 0.75):
        return "insult"
    if(obscene > 0.75):
        return 'obscene'
    if(toxic > 0.75):
        return "toxic"
    else:
        return 'Implicit/Other'

@dsClient.event  # message listener (bulk of work)
async def on_message(message):
    if message.author == dsClient.user:  # bot doesn't listen to own messages
        return
    
    messageList = message.content.split() # detect any flag words
    flagList = botWork.botCommands.flagScan(messageList)
    
    # statistical calls
        # Sends Dm to author with average hatescore derived from all of the events from a specific user
    if len(messageList) >= 2:
        if messageList[0] == "!avg":
            user = int(messageList[1])
            score = mongo.userScore(user)
            await message.author.send(score)
        # Sends a Dm to author with the occurence count of a word being said by a specific user
    if len(messageList) >= 3:
        if messageList[0] == "!wordCount":
            count = mongo.wordCount(messageList[1], int(messageList[2]))
            await message.author.send(count)
        # Sends a Dm to author with occurence count of all events by a specific user
    if len(messageList) >= 2:
        if messageList[0] == "!AllEventCount":
            count = mongo.allEventCount(int(messageList[1]))
            await message.author.send(count)
        # Sends a Dm to author with the occurence count of a specific category by a specific user
    if len(messageList) >= 3:
        if messageList[0] == "!CategoryCount":
            count = mongo.categoryCount(messageList[1] ,int(messageList[2]))
            await message.author.send(count)
    

    # Event Occurence
    if len(flagList) > 0:  # message is flagged
        messageClassification = pipe(message.content)  # uses BERT to classify messages
        hateCat = getBiggestHateScore(messageClassification)
        #hateScore = bot.hateScore(message.content)  # calls huggingChat to generate severity score
        # ^^ This sadly broken and fix is unknown. Classification score used as hate index for now. need to switch back
        # the implicitness is currently lost
        newScore = bot.newHateScore(messageClassification)

        
        print(newScore)
        if newScore > 0.5:  # only want to log "bad" messages
            user_data = mongoConnect.Event(message.author.id,
                                           message.content,
                                           message.created_at,
                                           flagList,
                                           newScore,
                                           getCategory(messageClassification))

            mongo.log(user_data) # logging data into mongo
            print('success!')
            await message.author.send(bot.flagReaction(message.content, hateCat, newScore))
            for flag in flagList:
                if mongo.wordCount(flag, message.author.id) > 4:
                    match flag:
                        case "Gypsies":
                            await message.author.send(educationalPrompt[0])
                        case "boy":
                            await message.author.send(educationalPrompt[1])
                        case "people":
                            await message.author.send(educationalPrompt[2])
            return


# run bot
dsClient.run('token')  # bot runner
