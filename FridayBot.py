import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import pywhatkit as kit
from datetime import date
from datetime import timedelta

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
username = ""

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.setProperty("rate",145)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour<12:
        speak("Good Morning Boss!")
    elif hour >=12 and hour<18:
        speak("Good Afternoon Boss!")
    else:
        speak("Good Evening Boss!")

    speak("I am Friday. Please tell me how may I help you!")

def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=3, phrase_time_limit=3)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language= 'en-in')
        
    except Exception as e:
        print(e)
        engine.setProperty("rate", 120)
        print("Say that again, please...")
        speak("Say that again, please")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email_address', 'your_password')
    server.sendmail('your_email_address', to, content)
    server.close()

def whatsmyname():
    global username
    if username == "":
        speak("I don't know, but i will remember if u tell me. Would u like to add it now")
        query = takeCommand().lower()
        if query == 'yes':
           speak("Alright. What should i call you")
           query = takeCommand().lower()
           username = query
           speak(f"You'd like to call you {username}. Is that right")
           query = takeCommand().lower()
           if(query == "yes"):
               speak(f"Sure. I'll call you {username} from now on.")
           else:
               speak("Got it. What should i call you")
               query = takeCommand().lower()
               username = query
               speak(f"okay i will remember {username} as your name")
        else:
            speak("ok, lets stop it for now")
            username = ""
    else:
        speak(f"Your name is {username}")

def whatsapp():
    contacts = {"<name1>" : "+91<number>" , "<name2>" : "+91<number>", "<name3>" : "+91<number>"}
    speak("Whom do you want to send message")
    query = takeCommand().lower()
    if query in contacts:
        sendto = contacts.get(query)
        person_name = query
        hrs = int(datetime.datetime.now().strftime("%H"))
        d = datetime.datetime.now() + timedelta(minutes=2)
        mins = int(d.strftime("Z%M").replace('Z0','Z').replace('Z',''))
        speak("whats the message.")
        query = takeCommand().lower()
        message = query
        speak(f" So, that's the message {person_name} saying {message}. Are you ready to send it")
        query = takeCommand().lower()
        if query == 'yes':
            kit.sendwhatmsg(sendto,message,hrs,mins)
            speak("message sent successfully")
        elif query == 'no' or query == 'cancel':
            speak("okay no problem. Message cancelled")
        else:
            speak("since i am having trouble, i won't send that message. You might want to try again later.")
    else:
        speak("No contact found of this name")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

         # Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 3)
            speak("According to Wikipedia")
            speak(results)
            print(results)

        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")

        elif 'open google' in query:
            webbrowser.open('www.google.com')
            
        elif 'open coursera' in query:
            webbrowser.open("www.coursera.org")

        elif 'open stackoverflow' in query:
            webbrowser.open("www.stackoverflow.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'date' in query:
            today = date.today()
            speak(f"Today's date is {today}")

        elif 'open googlecolab' in query:
            webbrowser.open("www.googlecolab.com")

        elif 'spotify' in query:
            os.startfile('C:\\Program Files\\Spotify\\Spotify')

        elif "send whatsapp message" in query:
            whatsapp()

        elif "what's my name" in query:
            whatsmyname()

        elif 'send email' in query:
            try:
                speak('What should I say?')
                content = takeCommand()
                to = "your_email_address"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Boss, I am not able to send this email")

        elif 'exit' in query:
            speak("Thank you for using me, have a nice day")
            exit()
