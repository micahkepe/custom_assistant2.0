import speech_recognition as sr
import openai
import PySimpleGUI as sg
from elevenlabslib import *

# Enter keys for OpenAI and ElevenLabs, then put voice model's name and your name
OPENAI_API_KEY = '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'
ELEVENLABS_KEY = '9fe3e2fe88d92bfb0c3af2cde624d296'
openai.api_key = OPENAI_API_KEY
elevenLabsAPIKey = ELEVENLABS_KEY
model = 'Ving Rhames'
YOUR_NAME = 'Micah'
user = ElevenLabsUser(elevenLabsAPIKey)
voice = user.get_voices_by_name(model)[0]

# ----- GUI Definition ----- #
sg.theme("dark grey 9")
layout = [[sg.Text("Your Name:"), sg.Input(key="-USER NAME-")],
          [sg.Text("Model:"), sg.Input(key="-MODEL-")],
          [sg.Text("Query Mode:"), sg.Button("Speak"), sg.Button("Type")],
          [sg.Multiline(key="-OUT-")],
          [sg.Save("Save"), sg.Exit("Exit")]
          ]

# Create the window
window = sg.Window("AI Assistant", layout)

# find microphone to use later to record audio
r = sr.Recognizer()
mic = sr.Microphone()

# initializing the conversation between user and model before queries with context
conversation = [
    {"role": "system", "content": f"Your name is {model} and you're an assistant for {YOUR_NAME}."},
]


def update_from_user_inputs(user_values):
    """
    :param user_values: values associated with user's window
    :return: None
    """
    model = user_values["-MODEL-"]
    user = ElevenLabsUser(elevenLabsAPIKey)
    voice = user.get_voices_by_name(model)[0]


def is_valid_user(user_values):
    """"
    Checks if user's keys are valid
    :param user_values: values associated with user_window
    Checks the given keys for OpenAI and ElevenLabs given by user
    :return: boolean value of valid or not
    """
    try:
        ElevenLabsUser(user_values["-ELEVEN LABS KEY-"])
        openai.api_key = user_values["-OPENAI KEY-"]
        openai.Completion.create(
            engine="text-davinci-003",
            prompt="Test",
            max_tokens=5)
        return True

    except:
        sg.popup_error("OpenAI and/or ElevenLabs Key is not valid")
        return False


def generate_image_response(prompt):
    """
    Generate response from GPT/ DallE for a query involving drawing a picture
    :param prompt: string of the user's query
    :return: string image url of generated drawing
    """
    # find subject user wants
    i = prompt.find("draw")
    i += 5

    # generate GPT response
    gpt_response = openai.Image.create(
        prompt=prompt[i:],
        n=1,
        size="1024x1024"
    )

    # get url from response and return
    url = gpt_response['data'][0]['url']
    return url


def generate_text_response(prompt, ongoing_convo):
    """
    Generate response from GPT for a standard query not involving drawing a picture
        and update chat log
    :param prompt: string of the user's query
    :param ongoing_convo: ongoing conversation between user and model
    :return:
    """
    ongoing_convo.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=ongoing_convo,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response["choices"][0]["message"]["content"]
    ongoing_convo.append({"role": "assistant", "content": answer})
    return answer


while True:
    event, values = window.read()
    print(event, values)
    # user closes window
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break

    # Option 1: User Speaks Question
    if event == "Speak" and is_valid_user(values):
        update_from_user_inputs(values)

        with mic as source:
            r.adjust_for_ambient_noise(source)  # Can set the duration with duration keyword

            window["-OUT-"].update("Speak now...")
            # print("Speak now...")

            try:
                # Gather audio and transcribe to text
                audio = r.listen(source)
                word = r.recognize_google(audio)

                # Show user's query
                window["-OUT-"].add_row(word)
                print(f"You said: {word}")

                # Close window and quit program when user says "That is all"
                if word.lower() == "that is all":
                    print(f"{model}: See you later!")
                    window.close()
                    quit()

                # if user wants to assistant to draw something (has "draw" in prompt)
                if "draw" in word:
                    image_url = generate_image_response(word)
                    print(f"{model}: Here's {word[i:]}")
                    print(image_url)
                    print("=====")

                # if user asks a standard question (no "draw" request)
                else:
                    message = generate_text_response(word, conversation)

                    # Show GPT's response
                    print(f"{model}: {message}")

                    # Uncomment to have model speak response
                    # voice.generate_and_play_audio(message, playInBackground=False)
                    print("=====")

            except Exception as e:
                print("Couldn't interpret audio, try again.".format(e))
                print("=====")

    # Option 2: User writes question
    if event == "Type" and is_valid_user(values):
        update_from_user_inputs(values)


window.close()

# if __name__ == "__main__":

