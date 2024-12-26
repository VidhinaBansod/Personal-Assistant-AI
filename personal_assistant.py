import asyncio
import datetime
import time
import webbrowser
import numpy as np
import face_recognition
import pygetwindow as gw
import cv2
import pyautogui
import pyperclip
import pyttsx3
import pywhatkit
import pywhatkit as pwk
import speech_recognition as sp
import wikipedia
from colorama import Fore, init, Style
from imaginairy import *
from imaginairy.api import imagine
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from mtranslate import translate
import random
from emotion_mode_chat import emotion_mode
from teaching_bot import personal_teacher

contacts = {
    # enter your contact here
}
ASSISTANT_NAME = "Sarthi"
engine = pyttsx3.init("sapi5")
init(autoreset=True)
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[18].id)
engine.setProperty('rate', 180)


def speak(audio):
    engine.say(audio)
    print(Fore.MAGENTA + "Sarthi: " + audio, end="", flush=True)
    engine.runAndWait()


def print_loop():
    while True:
        print(Fore.GREEN + 'Listening.....', end="", flush=True)
        print(Style.RESET_ALL, end="", flush=True)


def translate_hin_to_eng(text):
    english_text = translate(text, "en-in")
    return english_text


async def speech_recognizer():
    recognizer = sp.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 2000
    recognizer.dynamic_energy_adjustment_damping = 0.030
    recognizer.dynamic_energy_ratio = 1.0
    recognizer.pause_threshold = 1.2
    recognizer.non_speaking_duration = 0.5

    with sp.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        while True:
            print(Fore.GREEN + '\nListening.....', end="", flush=True)
            print(Style.RESET_ALL, end="", flush=True)
            try:
                audio = recognizer.listen(source, timeout=None)
                print("\r" + Fore.LIGHTBLACK_EX + "Recognising....", end="", flush=True)
                recognizer_text = recognizer.recognize_google(audio).lower()
                if recognizer_text:
                    trans_text = translate_hin_to_eng(recognizer_text)
                    print("\r" + Fore.BLUE + "User :" + trans_text)
                    return trans_text
                else:
                    return " "
            except sp.UnknownValueError:
                speak("Say that again please")
                recognizer_text = " "
            finally:
                print("\r", end="", flush=True)


def wish():
    hour = int(datetime.datetime.now().hour)
    if 4 <= hour <= 12:
        speak("Good Morning Sir, Let's Start the day")
    elif 12 < hour < 16:
        speak("Good afternoon Sir, let's not be lazy because of lunch today")
    elif 16 <= hour <= 18:
        speak("Good evening Sir")
    elif 18 < hour < 11:
        speak("Good evening sir or should I say night, either way let's wrap up things for you Sir")
    else:
        speak("Staying up late sir , Let's wrap up work fast so you can get your good night's sleep ")


async def searchGoogle(query):
    speak("what you want to google?")
    google_query = await speech_recognizer()
    speak(f"searchGoogle called with {google_query}\n")
    google_query = google_query.replace("sarthi", "").replace("google search", "").replace("google", "")
    speak("This is what I found on google")


async def searchYoutube(query):
    speak("What you want to search on youtube?")
    youtube_query = await speech_recognizer()
    speak(f"searchYoutube called with  {youtube_query} \n")
    youtube_query = youtube_query.replace("youtube search", "").replace("youtube", "").replace("play song", "")
    speak("This is what I found for your search!\n")
    web = "https://www.youtube.com/results?search_query=" + youtube_query
    webbrowser.open(web)
    pywhatkit.playonyt(youtube_query)
    speak("Done, Sir")


async def search_amazon(query):
    speak("what you want to search on amazon sir ?")
    search_query = await speech_recognizer()
    search_query = search_query.replace("amazon search", "").replace("amazon", "").replace("search on amazon", "")
    base_url = "https://www.amazon.in/s?k="
    search_url = base_url + search_query.replace(" ", "+")
    webbrowser.open(search_url)
    speak(f"Searching Amazon.in for: {search_query}")


history_file_path = 'C:\\Studies\\Python\\PA\\assets\\conversation_history.txt'


# Function to read conversation history from a text file
async def read_conversation_history(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""


# Function to write conversation history to a text file
async def write_conversation_history(file_path, history):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(history)


# ai model
async def ollama_chat(query):
    global conversation_history
    model = OllamaLLM(model="llama3.2")
    template = """"
       You are an AI assistant named Sarthi.Try to avoid *(asterisk). Your task is to assist me with various tasks in a humorous and engaging manner with respect too.
           **Give answer in less than 30 words and if content is large ASK USER IF HE WANTS TO CONTINUE THEN SPEAK REST OF IT**
       You can perform app opening, call automation, Amazon search, YouTube search, and help me learn languages easily.
       Additionally, you will assist me in my daily job tasks.


     

    Here is the conversation history: {context}

    Question:{question}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)
    context = await read_conversation_history(history_file_path)
    chain = prompt | model
    input_text = prompt.format(context=context, question=query)
    result = model.invoke(input_text)
    updated_history = context + f"User: {query}\nSarthi: {result}\n"
    await write_conversation_history(history_file_path, updated_history)
    return result


async def open_app(query):
    app_name = query.lower()
    query = query.replace("open", "")
    speak(f"Opening {query} , sir")
    try:
        if app_name == "notepad" or app_name == "open notepad":
            os.system("notepad.exe")
        elif app_name == "calculator" or app_name == "open calculator":
            os.system("calc.exe")
        elif app_name == "linkedin" or app_name == "open linkedin":
            os.system("start linkedin://")
        elif app_name == "whatsapp" or app_name == "open whatsapp":
            os.system("start whatsapp://")
        elif app_name == "this pc" or app_name == "open this pc":
            os.system("explorer.exe shell:MyComputerFolder")
        elif app_name == "camera" or app_name == "open camera":
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        else:
            speak("App {query} is not supported.")
    except Exception as e:
        print(f"An error occurred: {e}")


async def send_whatsapp_message(phone_number, message):
    now = datetime.datetime.now()
    # Schedule the message to be sent in 1 minute from now
    send_time = now + datetime.timedelta(minutes=1)
    pwk.sendwhatmsg(phone_number, message, send_time.hour, send_time.minute, 10, True,
                    15)
    time.sleep(15)


async def generate_message(query):
    # Extract the message part from the command
    if "saying" in query:
        message = query.split("saying")[-1].strip()
    else:
        message = "Hello, this is a message from Sarthi AI!"
    return message


async def switch_window(query):
    speak("switching window sir")
    pyautogui.hotkey("alt", "tab")


async def taking_note():
    os.system("notepad.exe")
    time.sleep(1)
    # Get the window with "Untitled - Notepad" in its title
    notepad = gw.getWindowsWithTitle("Untitled - Notepad")

    if notepad:
        notepad[0].activate()  # Bring Notepad to the front
        time.sleep(0.2)
        speak("What do you want to write in your note, sir?")
        note = speech_recognizer()  # Capture speech input
        # Copy the note to the clipboard
        pyperclip.copy(note)
        time.sleep(1)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(1)  # Ensure the text is pasted
        pyautogui.hotkey("ctrl", "s")
        speak("saving Note")
        time.sleep(2)
        random_num = random.randint(1, 9)
        pyautogui.write(f"MyNote{random_num}")
        pyautogui.press("enter")
        pyautogui.hotkey("ctrl", "w")
        speak("Notepad closed, sir.")
    else:
        speak("Unable to open Notepad, sir.")


async def make_whatsapp_call(contact_name):
    pyautogui.hotkey('win', 's')
    pyautogui.write('WhatsApp')
    pyautogui.press('enter')
    time.sleep(5)

    search_box = pyautogui.locateOnScreen("C:\\Studies\\Python\\PA\\assets\\search_box2.png", confidence=0.8)
    if search_box:
        pyautogui.click(search_box)
        pyautogui.write(contact_name)
        time.sleep(0.5)
        pyautogui.press("down")
        pyautogui.press('enter')

        time.sleep(3)  # Wait for the chat to open

        # Click on the call button
        call_button = pyautogui.locateOnScreen('C:\\Studies\\Python\\PA\\assets\\call_button.png')

        if call_button:
            pyautogui.click(call_button)
            time.sleep(10)
        else:
            speak("Call button not found.")
    else:
        speak("Search box not found.")


known_image1 = face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\person1.jpg")
known_image2 = face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\person2.jpg")
known_image3 = face_recognition.load_image_file("C:\\Studies\\Python\\PA\\assets\\person3.jpg")

known_encoding1 = face_recognition.face_encodings(known_image1)[0]
known_encoding2 = face_recognition.face_encodings(known_image2)[0]
known_encoding3 = face_recognition.face_encodings(known_image3)[0]
known_face_encodings = [known_encoding1, known_encoding2, known_encoding3]
known_face_names = ["Nishchay", "Devesh", "Rudra"]


async def recognize_face():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open video device.")
        return "Unknown"

    start_time = time.time()

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            best_match_distance = face_distances[best_match_index]

            name = "Unknown"
            if best_match_distance < 0.4:  # Lowered threshold to 0.4
                name = known_face_names[best_match_index]

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # If a known face is recognized, return the name
            if name != "Unknown":
                video_capture.release()
                cv2.destroyAllWindows()
                return name

        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Check if 4 seconds have passed
        if time.time() - start_time > 4:
            video_capture.release()
            cv2.destroyAllWindows()
            return "Unknown"

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return "Unknown"


async def main_loop():
    name = await recognize_face()  # Run face recognition
    if name == "Unknown":
        speak("Face not recognized, exiting.")
        return

    speak(f"Welcome, {name}! How can I assist you today?")
    # wish()
    print("")
    while True:
        query = await speech_recognizer()
        print(f"Recognized query: {query}")

        if "google" in query:
            await searchGoogle(query)
        elif "youtube" in query:
            await searchYoutube(query)
        elif "amazon" in query:
            await search_amazon(query)
        elif any(app in query for app in ["camera", "calculator", "linkedin", "this pc", "whatsapp", "notepad"]):
            await open_app(query)
        elif "message" in query:
            contact_name = query.lower().split("saying")[0].replace("message", "").strip()
            if contact_name in contacts:
                phone_number = contacts[contact_name]
                message = await generate_message(query)
                await send_whatsapp_message(phone_number, message)
            else:
                speak(f"Contact {contact_name} not found.")
        elif "call" in query:
            contact_name = query.lower().replace("call", "").strip()
            if contact_name in contacts:
                await make_whatsapp_call(contact_name)
            else:
                speak(f"Contact {contact_name} not found.")
        elif "switch window" in query:
            await switch_window(query)
        elif "take note" in query:
            await taking_note()
        elif "turn on emotional mode" in query:
            await emotion_mode()
        elif "teach me" in query:
            speak("Turning on personal teacher mode.")
            await asyncio.create_task(personal_teacher())
        elif "exit" in query or "stop" in query:
            speak("Goodbye, Sir. Have a great day!")
            break
        else:
            response = await ollama_chat(query)  # ollama_chat will handle the query
            speak(response)


if __name__ == "__main__":
    asyncio.run(main_loop())
