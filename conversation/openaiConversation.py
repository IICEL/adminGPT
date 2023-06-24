class Conversation:
    def __init__(self, max_length):
        self.conversation = []
        self.max_length = max_length

    def add_to_conversation(self, role, content):
        # add the message to the conversation list
        self.conversation.append({"role": role, "content": content})

        # check if conversation length is higher than max_length
        if len(self.conversation) > self.max_length:
            # if so, truncate the earliest message
            self.conversation = self.conversation[1:]

    def delete_messages_from(self,role):
        # filter out system messages
        self.conversation = [message for message in self.conversation if message["role"] != role]

    def clear_conversation(self):
        # clear all messages
        self.conversation = []

    def get_conversation(self):
        return self.conversation


    def append_to_system(self, new_content):
        # Reverse iterate over the list to find the latest 'system' role
        for msg in reversed(self.conversation):
            if msg['role'] == 'system':
                # Append to the content of the 'system' role
                msg['content'] += ' ' + new_content
                return
        # If no 'system' role message is found, append a new one
        self.add_to_conversation("system",new_content)
    
    def get_latest_system_msg(self) :
                # Reverse iterate over the list to find the latest 'system' role
        for msg in reversed(self.conversation):
            if msg['role'] == 'system':
                return msg['content']
        
        return ""