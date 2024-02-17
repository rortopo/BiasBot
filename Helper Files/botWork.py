from json import loads


from hugchat import hugchat
from hugchat.login import Login
from thefuzz import fuzz
from transformers import pipeline


# some simple bot commands and hugFace calls
class botCommands:
    #  takes in user message and puts it through huggingFace prompt
    #  currently returns hateScore

    def __init__(self, username: str, pw:str,):
        print('initalized')
        sign = Login(username, pw)
        cookies = sign.login()
        cookie_path_dir = "./cookies_snapshot"
        sign.saveCookiesToDir(cookie_path_dir)  # hugging face api calls
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # prompt below
        
    def hateScore(self, message: str, ) -> int: # TODO currently broken. idk why
        biasPrompt = "You are a machine tasked with detecting implicit bias in chat messages. You can only return a single number 0-5. Anything else will break the programming of your machine. Implicit bias, aslo knows as implicit prejudice or implicit attitude, is a negative attitude, of which one is not conciously aware, against a specific social group. Respond with a single integer 0-5 with severity of the bias. ONLY RETURN a single integer. Your response should be 1 number. If there is no bias present, return a 0. Your response needs to be a single integer and nothing else. Do not provide an explanation"
        print(biasPrompt + "\n" + "Message:" + message)
        for resp in self.chatbot.query(biasPrompt + "\n" + "Message:" + message,
                                  stream=True):
            if resp is not None and " " not in resp:
                if resp['token'].isdigit():
                    return int(resp['token'])
                
    def newHateScore(self, classification: list) -> float:
        
        sorted(classification)
        print(classification[0][0]['score'])
        return classification[0][0]['score']

    #  checks message against flag word list using fuzzy search
    def flagScan(message: list) -> list:
        #  file read for flagList
        with open("blacklist.json", "r") as file:  # flag word list
            data = loads(file.read())
        flagList = []
        for flag in data:
            for word in message:
                fuzzScore = fuzz.ratio(flag, word)
                # fuzzy string search seeing if the word is close enough to flag word
                if fuzzScore > 75:  # word is close enough to flag word
                    flagList.append(flag)
        return flagList
    
    def flagReaction(self, message: str, category: str, severity: float) -> str:
       # prompt= 'you are tasked with explaining hateful messages with an educational response. You are given a message, its category, and severity of hate (0-5). Respond in two sentences why the response was hateful, and what they should think about next time'
        #response = self.chatbot.query(prompt + "\n" + "Message:" + message + "\n" + "Category:" + category + "\n" + "Severity:" + str(severity))
        # ^^ we realized LLM for education is a bad look
        response = 'Your message: \n"' + message +  '"\nwas not an acceptable message.' + "\n" + 'It was categorized as ' + category + "\n" + 'Your message was ranked with a severity of: ' + str(round(severity, 3)) + ' out of 1. ' + "\n" + 'Please reconsider using such language again.\n++++++++++++++++++++++++++++++++++++'
        print(response)
        return response





