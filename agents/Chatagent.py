
import configparser

from conversation.openaiConversation import Conversation
from api.openaiApi import OpenAIAPI


class ChatAgent:
    api= None    
    conversation = None
    memory=None
    parent_embedder=None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("main.conf")

        api_key = config["openai"]["api_key"]
        self.api=OpenAIAPI(api_key)

        self.model_engine = "gpt-3.5-turbo-16k"
        self.model_function="gpt-3.5-turbo-0613"
        self.temperature = 0.25
        self.user_input = ""
        self.bot_output = ""
        # Initialize the conversation
        self.conversation = Conversation(20)
        



    def send_user_response(self, user_input):

        self.user_input = user_input
        self.conversation.add_to_conversation('user',user_input)
        return False , " "

    def get_bot_response(self):
        print(self.conversation)
        response = self.api.chat(model=self.model_engine,temperature=self.temperature,message=self.conversation.conversation)
        self.conversation.add_to_conversation("assistant",response)
        self.conversation.delete_messages_from("system")# System messages are deleted after the response has been generated
        self.bot_output=response
        return response


   

    def list_models(self):
       return self.api.list_models()
    


   