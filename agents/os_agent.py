from agents.Chatagent import ChatAgent

import json
import subprocess

class OsAgent(ChatAgent):
    def __init__(self):
        super().__init__()
  

    # function is not needed but it is here to make code easy to read.
    def send_user_response(self,user_input) :

        return super().send_user_response(user_input)


    def get_bot_response(self):
        function_response=self.make_decision1()
        
        return function_response+"\n"+super().get_bot_response()

        
     
    def make_decision1(self) :
        message=self.conversation.get_conversation()[-5:] #Only copy the last 5 messages to generate the command
        message.append({"role":"system","content":""" 
        You are a sysadmin for Windows. You are logged in as Admin and can run any command in powershell terminal.
        please reply to any prompt only with bash commands. No explenations are needed. You can only run commands in non interactive mode.
        """})  #  Modify this if you want the system to use Ubuntu/Mac commands

        model=self.model_function
        function_call="auto"

        functions=[
            {
                "name": "execute_commands",
                "description": "function to execute List of Windows commands. No sudo needed. Interactive commands can not be executed.", #  Modify this if you want the system to use Ubuntu/Mac commands
                "parameters": {
                    "type": "object",
                    "properties": {
                        "commands": {
                            "type": "object",
                            "description": "List of Windows commands with switches that need to be executed", #  Modify this if you want the system to use Ubuntu/Mac commands
                        },
                        
                    },
                    "required": ["commands"],
                },
            },
            
        ]
        
        decision=self.api.function_chat(message=message,model=model,functions=functions,function_call=function_call)

        print(decision)
        
        function_name=""
        function_response=""

        if decision.get("function_call"):

            function_name = decision["function_call"]["name"]
            
            if  function_name== "execute_commands" :
                parsed_json = json.loads(decision['function_call']['arguments'])
                if 'commands' in parsed_json:
                    linux_commands=parsed_json['commands']
                
                    print(linux_commands)
                    for command in linux_commands :
                        output=self.execute_command(command)
                        self.conversation.append_to_system(f"PS C:\\Users\\>{command} \n Output :  {output}")
                        function_response=f"PS C:\\Users\\>{command} \n Output :  {output}"
        return function_response
        


    #this executes shell commands on both linux and windows.
    def execute_command(self, s):
        try:
            # Create the command
            command = ["powershell", "-Command", s]  ## Modify "powershell" to "bash" or "sh" to use it in linux

            # Execute the command
            result = subprocess.run(command, shell=True, check=True, timeout=30, capture_output=True)

            if result.returncode != 0:
                print(f"Error: {result.stderr.decode().strip()}")
            return result.stdout.decode()

        except subprocess.CalledProcessError as e:
            # Catch the exception and print the error message
            return f"Error Exception: {e.stderr.decode().strip()}"

        except subprocess.TimeoutExpired:
            # Catch the timeout exception and kill the process
            return "Command timed out and was killed."
