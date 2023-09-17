from gtts import gTTS
import os
import openai
import speech_recognition as sr

# Set your OpenAI API key here
api_key = 'YOUR_OPENAI_API_KEY'

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the OpenAI API client
openai.api_key = api_key

def chat_with_gpt3(prompt, model="text-davinci-002", max_tokens=50):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()

# Capture audio from the microphone
with sr.Microphone() as source:
    print("Say something...")
    recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
    audio = recognizer.listen(source)

try:
    # Recognize the speech using Google Web Speech API
    text = recognizer.recognize_google(audio)
    print("You said:", text)

    # Initialize the conversation
    conversation = [f"You: {text}"]

    while True:
        # Get a response from ChatGPT
        ai_reply = chat_with_gpt3("\n".join(conversation))

        print(f"ChatGPT: {ai_reply}")
        conversation.append(f"ChatGPT: {ai_reply}")

        # Convert ChatGPT's response to speech
        tts = gTTS(ai_reply)
        tts.save("output.mp3")

        # Play the TTS output
        os.system("mpg123 output.mp3")

        # Capture user's next speech input
        with sr.Microphone() as source:
            print("You: (Speak or type 'exit' to end)")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # Recognize the user's speech
            text = recognizer.recognize_google(audio)
            print("You said:", text)

            # Add the user's input to the conversation
            conversation.append(f"You: {text}")

            if text.lower() == 'exit':
                break

        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))

except sr.UnknownValueError:
    print("Google Web Speech API could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Web Speech API; {0}".format(e))
