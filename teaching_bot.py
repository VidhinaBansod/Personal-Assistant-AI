import pyttsx3
import speech_recognition as sp
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from colorama import Fore, Style
from mtranslate import translate
import asyncio

# Initialize the TTS engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[18].id)
engine.setProperty('rate', 170)

# Initialize Ollama model
model = OllamaLLM(model="llama3.2")

# Function to convert text to speech (with faster processing)
async def speak_text(text):
    engine.say(text)
    # print(Fore.CYAN + "Sarthi:" + text, flush=True)
    engine.runAndWait()

# Function to translate Hindi to English (if needed)
def translate_hin_to_eng(text):
    return translate(text, "en-in")

# Optimized function to capture voice input
async def speech_recognizer():
    recognizer = sp.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 1500
    recognizer.pause_threshold = 1.2
    recognizer.non_speaking_duration = 0.5

    with sp.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print(Fore.GREEN + '\nListening.....', flush=True)
        try:
            audio = recognizer.listen(source, timeout=4)
            print("\r" + Fore.LIGHTBLACK_EX + "Recognising....", flush=True)
            recognizer_text = recognizer.recognize_google(audio).lower()
            trans_text = translate_hin_to_eng(recognizer_text)
            print("\r" + Fore.BLUE + "User: " + trans_text)
            return trans_text
        except sp.UnknownValueError:
            await speak_text("Please repeat.")
            return " "
        except sp.WaitTimeoutError:
            await speak_text("Listening timed out.")
            return " "
        finally:
            print("\r", end="", flush=True)

# Store conversation history in memory for faster access
conversation_history = ""

async def read_conversation_history():
    global conversation_history  # Declare global to modify it
    try:
        with open("C:\\Studies\\Python\\PA\\assets\\learning_path.txt", 'r', encoding='utf-8') as file:
            conversation_history = file.read()
    except FileNotFoundError:
        conversation_history = ""

# Write conversation history only at necessary times to avoid frequent file I/O
async def write_conversation_history():
    global conversation_history  # Declare global to access it
    with open("C:\\Studies\\Python\\PA\\assets\\learning_path.txt", 'w', encoding='utf-8') as file:
        file.write(conversation_history)

# Main function for the AI teacher
async def personal_teacher():
    global conversation_history  # Declare global to modify it
    await speak_text("Hello, I am your personal teacher. Let's start learning! How can I help you today?")
    await read_conversation_history()

    while True:
        user_input = await speech_recognizer()

        if "exit" in user_input:
            await speak_text("Goodbye, and happy learning!")
            break

        # Define the prompt template for the teacher model
        template = """
        You are a personal teacher which teaches things in simple and fun way with increasing complexity to get 
        expert in topic. And when user want to switch topic remember topic where it is left and help in learning 
        new topic.

        Previous interactions: {history}
        User message: {question}

        Your response (explain the words concisely):
        """

        prompt = ChatPromptTemplate.from_template(template)
        input_text = prompt.format(history=conversation_history, question=user_input)

        # Get the response from the Ollama model
        response = model.invoke(input_text)
        print(Fore.LIGHTCYAN_EX + "Teacher: " + response, flush=True)
        await speak_text(response)

        # Update conversation history in memory
        conversation_history += f"\nUser: {user_input}\nTeacher: {response}"

        # Write history periodically to avoid frequent disk writes
        if len(conversation_history.split('\n')) % 10 == 0:
            await write_conversation_history()

# Start the personal teacher mode asynchronously for faster response
# asyncio.run(personal_teacher())
