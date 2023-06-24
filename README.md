# adminGPT
 This is a bot that allows you to manage your OS by typing in normal natural language

Example 1
![alt text](example1.png)

Example2
![alt text](example2.png)


### Setup

git clone
```bash
pip3 install -r requirements.txt
```
or for windows
```bash
pip install -user -r requirements.txt
```
edit the main.conf file to add you openai key


Running the code :
python3 main.py

Visit the URL : localhost:8085 in your browser

### Switching the code to other OS
1. Edit Lines in os_agent.py
prompt on line : 27
prompt on line : 37
prompt on line : 43

2. Optional output on line 73

3. Line 82 change powershell for any other shell.