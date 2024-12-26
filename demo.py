import os
import pyautogui
import concurrent.futures
import asyncio
import pyttsx3
import pywhatkit as pwk
import speech_recognition as sp
import datetime
import wikipedia
import pywhatkit
import webbrowser
from mtranslate import translate
from selenium import webdriver
import cv2
from imaginairy.api import imagine
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time

# Contacts
contacts = {
    "devesh": '+919322421076',
    "nishchay": "+917999511189",
}

# Initialization
ASSISTANT_NAME = "Sarthi"
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[10].id)

history_file_path = '/assets/conversation_history.txt'

# Thread Pool Executor
executor = concurrent.futures.ThreadPoolExecutor()


# Helper functions
def speak(audio):
    print(f"Sarthi: {audio}")
    engine.say(audio)
    engine.runAndWait()


async def async_speak(audio):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, speak, audio)


def translate_hin_to_eng(text):
    english_text = translate(text, "en-in")
    return english_text


def read_conversation_history(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""


def write_conversation_history(file_path, history):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(history)


def ollama_chat_async(query):
    global conversation_history
    model = OllamaLLM(model="llama3.2")
    template = """"You are an AI assistant named Sarthi. Answer humorously and politely like a assistant. Try to answer in less time. Ask before answering in large.
                   Here is the conversation history: {context}
                   Question:{question}
                   Answer:
                """
    prompt = ChatPromptTemplate.from_template(template)
    context = read_conversation_history(history_file_path)
    input_text = prompt.format(context=context, question=query)
    result = model.invoke(input_text)
    updated_history = context + f"User: {query}\nSarthi: {result}\n"
    write_conversation_history(history_file_path, updated_history)
    return result


def searchGoogle(query):
    query = query.replace("sarthi", "").replace("google search", "").replace("google", "").replace("search on google",
                                                                                                   "").replace(
        "open google", "")
    speak("This is what I found on google")
    try:
        pywhatkit.search(query)
        result = wikipedia.summary(query, sentences=1)
        speak(result)
    except:
        speak("No speakable output available")


def searchYoutube(query):
    query = query.replace("youtube search", "").replace("youtube", "").replace("play song", "").replace("open youtube",
                                                                                                        "").replace(
        "search on youtube", "")
    speak("This is what I found for your search!")
    web = "https://www.youtube.com/results?search_query=" + query
    webbrowser.open(web)
    pywhatkit.playonyt(query)
    speak("Done, Sir")


def search_amazon(query):
    query = query.replace("amazon search", "").replace("amazon", "").replace("search on amazon", "").replace(
        "open amazon", "")
    base_url = "https://www.amazon.in/s?k="
    search_url = base_url + query.replace(" ", "+")
    webbrowser.open(search_url)
    speak(f"Searching Amazon.in for: {query}")


def open_app(query):
    app_name = query.lower()
    query = query.replace("open", "")
    speak(f"Opening {query}, sir")
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
            speak(f"App {query} is not supported.")
    except Exception as e:
        speak(f"An error occurred: {e}")


def generate_image(prompt):
    try:
        image = imagine(prompt)
        image_path = f"{prompt.replace(' ', '_')}.png"
        image.save(image_path)
        speak(f"Image generated and saved as {image_path}")
    except Exception as e:
        speak(f"An error occurred while generating the image: {e}")


async def send_whatsapp_message(phone_number, message):
    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(minutes=1)
    await asyncio.to_thread(pwk.sendwhatmsg, phone_number, message, send_time.hour, send_time.minute, 10, True, 15)


async def make_whatsapp_call(contact_name):
    pyautogui.hotkey('win', 's')
    pyautogui.write('WhatsApp')
    pyautogui.press('enter')
    await asyncio.sleep(5)
    search_box = pyautogui.locateOnScreen("C:\\Studies\\Python\\PA\\search_box.png", confidence=0.8)
    if search_box:
        pyautogui.click(search_box)
        pyautogui.write(contact_name)
        pyautogui.press("down")
        pyautogui.press('enter')
        await asyncio.sleep(3)
        call_button = pyautogui.locateOnScreen('C:\\Studies\\Python\\PA\\call_button.png')
        if call_button:
            pyautogui.click(call_button)
            await asyncio.sleep(10)
        else:
            await async_speak("Call button not found.")
    else:
        await async_speak("Search box not found.")


# Asynchronous handlers
async def speech_recognizer():
    recognizer = sp.Recognizer()
    with sp.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        while True:
            try:
                audio = recognizer.listen(source, timeout=None)
                recognizer_text = recognizer.recognize_google(audio).lower()
                if recognizer_text:
                    trans_text = translate_hin_to_eng(recognizer_text)
                    print(f"User: {trans_text}")
                    return trans_text
                else:
                    return " "
            except sp.UnknownValueError:
                await async_speak("Sorry, I didn't catch that. Can you please repeat?")
                continue


async def process_query(query):
    if "google" in query:
        searchGoogle(query)
    elif "youtube" in query:
        searchYoutube(query)
    elif "amazon" in query:
        search_amazon(query)
    elif any(app in query for app in ["camera", "calculator", "linkedin", "this pc", "whatsapp", "notepad"]):
        open_app(query)
    elif "generate image" in query:
        prompt = query.replace("generate image", "").strip()
        generate_image(prompt)
    elif "message" in query:
        contact_name = query.lower().split("saying")[0].replace("message", "").strip()
        if contact_name in contacts:
            phone_number = contacts[contact_name]
            message = query.split("saying")[-1].strip()
            await send_whatsapp_message(phone_number, message)
        else:
            await async_speak(f"Contact {contact_name} not found.")
    elif "call" in query:
        contact_name = query.lower().replace("call", "").strip()
        if contact_name in contacts:
            await make_whatsapp_call(contact_name)
        else:
            await async_speak(f"Contact {contact_name} not found.")
    else:
        response = ollama_chat_async(query)
        await async_speak(response)


async def main_loop():
    while True:
        print("\nListening for your command...\n")
        query = await speech_recognizer()
        if "exit" in query or "stop" in query:
            await async_speak("Goodbye, Sir. Have a great day!")
            break
        else:
            await process_query(query)


# Start the assistant
asyncio.run(main_loop())
