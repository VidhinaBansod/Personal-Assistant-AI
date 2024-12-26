import pyttsx3
from colorama import Fore, Style
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from mtranslate import translate
from textblob import TextBlob
import speech_recognition as sp
import asyncio

# Initialize the TTS engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[18].id)
engine.setProperty('rate', 170  )
# Cache for repeated translations
translation_cache = {}


def translate_hin_to_eng(text):
    if text in translation_cache:
        return translation_cache[text]
    english_text = translate(text, "en-in")
    translation_cache[text] = english_text
    return english_text


recognizer = sp.Recognizer()
recognizer.dynamic_energy_threshold = False
recognizer.energy_threshold = 3000


# Speech recognition function (synchronous)
def recognize_speech_sync(source):
    while True:
        print(Fore.GREEN + '\n Listening.....', end="", flush=True)
        print(Style.RESET_ALL, end="", flush=True)

        try:
            audio = recognizer.listen(source, timeout=None)
            print(Fore.LIGHTBLACK_EX + "Recognising....", end="", flush=True)
            recognizer_text = recognizer.recognize_google(audio).lower()
            trans_text = translate_hin_to_eng(recognizer_text)
            print(Fore.BLUE + "User: " + trans_text)
            return trans_text
        except sp.UnknownValueError:
            engine.say("Please say that again.")
            engine.runAndWait()
            continue  # Keep listening until valid input


# Async function to invoke the model and generate response
async def invoke_model_async(sentiment, conversation_history, chat):
    model = OllamaLLM(model="llama3.2")

    # Define the prompt template
    template = """
    You are a supportive friend who provides emotional support.Answer in couple of lines not too long.
    Analyze the user's emotions and respond empathetically, without mentioning sentiment scores.
    Use previous interactions to inform your response.

    User's emotions: {sentiment}
    User's previous interactions: {history}
    User's message: {question}

    Your response:
    """
    prompt = ChatPromptTemplate.from_template(template)
    input_text = prompt.format(sentiment=sentiment, history=conversation_history, question=chat)

    result = model.invoke(input_text)
    print(Fore.LIGHTYELLOW_EX + "Sarthi: " + result, end="", flush=True)
    return result


# Cache conversation history in memory and write to file periodically
history_file_path = 'C:\\Studies\\Python\\PA\\assets\\emotionchat_history.txt'
conversation_history = ""


def read_conversation_history(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""


def write_conversation_history(file_path, history):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(history)


# Optimized emotional mode with parallel tasks
async def emotion_mode():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[18].id)
    engine.say("Emotional mode is activated" )
    print(Fore.LIGHTYELLOW_EX+ "Sarthi: "+"Emotional mode is activated",end="",flush=True)
    engine.say("Hello, how are you, my friend?")
    print(Fore.LIGHTYELLOW_EX+ "Sarthi: "+"Hello, how are you, my friend?" ,end="",flush=True)
    engine.runAndWait()

    global conversation_history
    conversation_history = read_conversation_history(history_file_path)

    with sp.Microphone() as source:  # Synchronous microphone usage
        recognizer.adjust_for_ambient_noise(source)

        while True:
            chat = recognize_speech_sync(source)

            if "exit" in chat:
                engine.say("Exiting emotional mode")
                engine.runAndWait()
                break
            else:
                blob = TextBlob(chat)
                sentiment = blob.sentiment
                result = await invoke_model_async(sentiment, conversation_history, chat)
                engine.say(result)
                engine.runAndWait()

                # Update conversation history
                conversation_history += f"\nUser: {chat}\nBot: {result}"

            # Save conversation history periodically
            write_conversation_history(history_file_path, conversation_history)


# Entry point to start emotional mode
if __name__ == "__main__":
    asyncio.run(emotion_mode())

