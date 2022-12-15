from google.cloud import texttospeech
import PyPDF2
import os
import tkinter as tk
from tkinter.filedialog import askopenfilename

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'texttospeech-371713-e72692988d7f.json'
client = texttospeech.TextToSpeechClient()

filename = None


def uploader(event=None):
    file_name = askopenfilename()
    label1['text'] = file_name
    save_name = file_name.split('/')[len(file_name.split('/'))-1][:-4]
    print(save_name)
    pdfFileObj = open(file_name, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    page_num = pdfReader.numPages
    text = ""
    for page in range(page_num):
        text += pdfReader.getPage(page).extractText()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Neural2-H",ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(f"{save_name}.mp3", "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{save_name}.mp3"')
    pdfFileObj.close()


root = tk.Tk()
root.title("PDF to AUDIO APP")
root.geometry("400x100")

label1 = tk.Label(text='Choose your PDF to convert AUDIO')
label1.pack(padx=2, pady=5)

button1 = tk.Button(text='Upload', command=uploader, bg='#2B3467', fg='#FCFFE7')
button1.pack(padx=2, pady=15, ipady=10)

root.mainloop()

