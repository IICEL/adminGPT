import gradio as gr
from agents.os_agent import OsAgent
from agents.Chatagent import ChatAgent


# Create an instance of the ChatAgent class
chat_agent = OsAgent()

def add_text(history, text):
    history = history + [(text, None)]
    return history, ""


def bot(history):
    user_input = history[-1][0]  # Get the last user input from the history
    command , output=chat_agent.send_user_response(user_input)

    if(command):
        response=output  
    else:
        response = get_bot_response()
    history[-1][1] = response
    return history

def get_bot_response() :
    return chat_agent.get_bot_response()
        

with gr.Blocks() as demo:
    chatbot = gr.Chatbot([], elem_id="chatbot").style(height=400)

    with gr.Row():
        with gr.Column(scale=0.65):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",
            ).style(container=False)


    txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
        bot, chatbot, chatbot
    )


demo.launch(server_port=8085, server_name="localhost", )

