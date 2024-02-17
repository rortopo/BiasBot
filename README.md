# BiasBot
Discord bot created for [Hacking 4 Humanity 2024](https://www.hacking4humanity.online/)\
First Place winner of Tech Track\
Created by: \
Rory McCann(rcm71@pitt.edu),\
Ivan Puri(isp25@pitt.edu),\
Chase Lahner(cal256@pitt.edu),\
Holden Gent(hfg8@pitt.edu)

## The Problem

Discord is one of the top messaging platforms, with 19 million servers and 175 million monthly users worldwide [(Curry)](www.buisnessofapps.com/data/discord-statistics/).
It is typically used in gaming communities, with integration on consoles as well as PCs. Although there is moderation available, 
much of hate falls through the cracks. Approximately 1 in 10 young gamers are exposed to some sort of white supremacy, which is
far too high [(Center for Technology and Society)](www.adl.org/resources/report/hate-no-game-hate-and-harrasment-online-games-2022).

## Theory of Change

Online hate plagues communities that are made to bring people together. The common approach to online hate is to just 
outright ban users, but this is just a quick fix to a much larger issue. Hate stems from ignorance and misinformation 
so we chose to fight hate through education. There are two types of people who engage in harmful rhetoric, the 
willfully ignorant, and the plain ignorant. Our bot aims to target those who are just plain ignorant, and hopefully change their 
language habits. By using education as opposed to a firm hand, we hope to stop the cycle of hate.

## How it Works

1. The bot must be initialized on a local machine
2. Once initialized, the bot listens to all messages in public channels for all servers it is a part of
3. When a message is sent, a fuzzy search is used to check of flag words within the message
    - A fuzzy search uses a Levenshtein ratio to determine how similar words are, even when misspelled
4. If any flagged words exist, a call is made to Hugging Face using a BERT model fine-tuned to categorize the hate and give it a score
    - We had a hate score ranking that was much better at implicit bias. It worked by making a call to the standard Hugging Face LLM using hugchat, but this fell apart due to unknown reasons. The current number one priority is getting this functionality back, as it gave us a much better implicit reading. See ```botWork.botCommands.hateScore()```.
5. If the hate score is above a set threshold, the event is logged into MongoDB and the user is sent a warning
6. If the same word has been used a certain number of times, an educational blurb is sent to the user to explain why their language can be harmful, with further reading.
    - If anyone would like to update the JSONs, please feel free to add more!
  
***There is a demo video in the files***

## Community Inclusion

Our bot is aimed towards Discord servers for classes or gaming communities that are too large for the amount of human moderators in their server.
One of our team members is a part of a server with 4 moderators for approximately 400 people. On larger servers, the 1:100 ratio
does not scale well, posing an issue. Our objective is to provide a tool for the owners and moderators to better manage
their large communities. We would like to stay in close communication with the owners and moderators of communities
where our bot is active to make our product as effective as possible. We currently have statistical commands that can give
insight into user habits.

## Ethical Considerations and Drawbacks

Our bot utilizes Hugging Face, an open source LLM(Large Language Model) platform alternative to Open AI. We chose this due to Hugging Face's
customization and transparency in models and training data. Despite this, using AI will always lead to ethical concerns.
We initially used it to generate educational prompts, but realized that we cannot guarantee that more misinformation is being not being spread.
We also would like to put some work into detecting implicit bias. A day before the competition deadline, we had a working prototype and were excited to polish and send in the morning.
It utilized hugchat, sending it a prompt asking to rate the message on a 1 - 5 scale of implicit bias. It worked pretty well, and could detect things
like "You people suck at driving" as biased speech. Now, the server side of that call is failing us, but it is priority number one. We may want
to consider other methods, such as creating our own dataset to base a model off of, for more accuracy in it's rating. We switched over to
use the categorical value for the time being.

We would also like to take measures to maintain the anonymity of data within MongoDB. Currently, we use a two table approach to store the ID, and then link that
to their events. It's *a* level of security, but it's not enough.

## Next Steps

Currently, our bot is not ready to work on a large scale. We have a few "number one priorities". 
Firstly, we would like to get the implicit bias detection functionality back. Also, we would like to
expand our JSON files, filling them with more flag words and educational prompts. We were fairly limited
in this capacity while prototyping, but for a real deployment, this would need to be bolstered. As mentioned
earlier, we also plan on adding additional security measures to make sure that the users data is anonymous to onlookers.
The final step would be to host the bot on a virtual machine, so that we don't have to run it on a personal
computer. 

## Works Cited

- Curry, David. "Discord Revenue and Usage (2024)." *BuisnessofApps*, 10 Jan. 2024, www.buisnessofapps.com/data/discord-statistics/.
- Anti-Defamation League. "Hate Is No Game: Hate and harrasment in Online Games." *Anti-Defamation League*, 2022, www.adl.org/resources/report/hate-no-game-hate-and-harrasment-online-games-2022.

