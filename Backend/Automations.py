import subprocess
import webbrowser
import os
import random

import pywhatkit

import re


def clean_command(command):
    # Define a pattern to match whole words and specific phrases only
    patterns = ["open", "search", "wikipedia", "wiki", "on", "can you","in"]

    # Create a regular expression pattern that matches these words
    pattern = r'\b(?:' + '|'.join(map(re.escape, patterns)) + r')\b'

    # Use re.sub to replace matched patterns with an empty string and strip the result
    cleaned_command = re.sub(pattern, '', command, flags=re.IGNORECASE).strip()

    # Clean up multiple spaces
    cleaned_command = re.sub(' +', ' ', cleaned_command)

    return cleaned_command


# Your function that uses the command




#

def play_song(song_name):
    pywhatkit.playonyt(song_name)
    return f"playing {song_name} on youtube"

def open_app(app_name):
    os.system(app_name)
    print(f"Opening {app_name}...")

def close_app(app_name):
    command = f'taskkill /f /im {app_name}'
    # Run the command
    subprocess.run(command, shell=True)
    print(f"Closing {app_name}...")

def open_website(website_name):
    # You can implement a logic here to open the requested website
    print(f"Opening {website_name}...")
    webbrowser.open(website_name)

def search(command):
    webbrowser.open(f"https://en.wikipedia.org/wiki/{command}")

def execute_automation(command):
    sites = [["youtube", "https://www.youtube.com"], ["google", "https://www.google.com"],
             ["wikipedia", "https://www.wikipedia.com"]]
    for site in sites:
        if f"open {site[0]}".lower() in command.lower():
            open_website(site[1])
            return (f"Opening {site[0]} sir.")

    apps = [
        ["visual studio code", r'start "" "C:\Users\bhatt\AppData\Local\Programs\Microsoft VS Code\Code.exe"','Code.exe'],
        ["Excel", r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel 2016.lnk"','EXCEL.EXE'],
        ["Powerpoint", r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint 2016.lnk"', 'POWERPNT.EXE'],
        ["PyCharm", r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\JetBrains\PyCharm Community Edition 2020.3.3.lnk"','pycharm64.exe'],
        ["Python",
         r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\JetBrains\PyCharm Community Edition 2020.3.3.lnk"',
         'pycharm64.exe'],

        ["Task Manager", r'start "" "C:\WINDOWS\system32\Taskmgr.exe"'],
        ["Edge", r'start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"','msedge.exe'],
        ["Ed", r'start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"', 'msedge.exe'],
        ["as", r'start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"', 'msedge.exe'],

        ["Word", r'start "" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word 2016.lnk"','WINWORD.EXE'],
        ["Chrome", r'start "" "C:\Program Files\Google\Chrome\Application\chrome.exe"','chrome.exe']
    ]

    for app in apps:
        if "open" in command.lower() and app[0].lower() in command.lower():
            open_app(app[1])
            return (f"Opening {app[0]} sir.")
        elif ("close".lower() in command.lower() or "cloth" in command.lower()) and app[0].lower() in command.lower():
            close_app(app[2])
            return (f"Closing {app[0]} sir.")

    if "are you there" in command.lower():
        return ("At your service sir.")

    if "play" in command.lower() and "youtube" in command.lower():
        song_name = command.lower().replace("play", "").replace("youtube", "").strip()
        play_song(song_name)
        return True

    elif ("open" in command.lower() or "search" in command.lower()) and (
            "wikipedia" in command.lower() or "wiki" in command.lower()):
        cleaned_command = clean_command(command)
        search(cleaned_command)
        return f"searching {cleaned_command} on wikipedia"


    elif "open" in command.lower() and "website" in command.lower():
        website_name = command.lower().replace("open", "").replace("website", "").strip()
        open_website(website_name)
        return True
    else:
        messages = [
            "Sorry sir, I can't reach you like that.",
            "Apologies, sir, but that's not possible for me.",
            "I'm afraid I can't reach you that way, sir.",
            "Regretfully, sir, I'm unable to reach you like that.",
            "Sorry sir, I can't make that happen.",
            "I'm sorry, sir, but I can't reach you in that manner.",
            "My apologies, sir, that's not within my capabilities.",
            "Unfortunately, sir, I can't reach you that way.",
            "I'm sorry, sir, I can't accommodate that request.",
            "Sorry sir, I can't manage to reach you like that."
        ]
        return random.choice(messages)
