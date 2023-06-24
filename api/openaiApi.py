import openai

import threading
import queue

class OpenAIAPI:
    timeout=5 # wait for openai api to repsond for 5 seconds otherwise kill the thread
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def _call_api(self, func, q, *args, **kwargs):
        response = func(*args, **kwargs)
        q.put(response)

    def _execute_threaded_api_call(self, api_func, *args, **kwargs):
        q = queue.Queue()
        t = threading.Thread(target=self._call_api, args=(api_func, q) + args, kwargs=kwargs)
        t.start()
        t.join(timeout=self.timeout)
        if t.is_alive():
            return {"choices":[{"message":{"role":"assistant","content":"OpenAI API call is taking too long, Server is too busy, Please try again"}}]}
        else:
            return q.get()

    def complete_prompt(self, prompt, max_tokens=100, temperature=0.5, engine="text-davinci-002"):
        response = self._execute_threaded_api_call(
            openai.Completion.create,
            engine=engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        if isinstance(response, str):
            return response
        else:
            return response.choices[0].text.strip()

    def chat(self, temperature, message, model="gpt-4.0"):
        response = self._execute_threaded_api_call(
            openai.ChatCompletion.create,
            model=model,
            temperature=temperature,
            messages=message
        )
        if isinstance(response, str):
            return response
        else:
            return response['choices'][0]['message']['content']

    def function_chat(self, message, model="gpt-4.0-turbo", functions=[], function_call="auto"):
        response = self._execute_threaded_api_call(
            openai.ChatCompletion.create,
            model=model,
            temperature=0.0,
            messages=message,
            functions=functions,
            function_call=function_call
        )
        if isinstance(response, str):
            return response
        else:
            message = response["choices"][0]["message"]
            return message

    def list_models(self):
        models = openai.Model.list()
        response = ""
        for model in models['data']:
            response += model['id'] + "\n"
        return response
