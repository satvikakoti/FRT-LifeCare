import os
from datetime import date
from PIL import Image
from twilio.rest import Client
import random
import azure.cognitiveservices.speech as speechsdk
from flask_mail import *  
from flask import Flask, render_template, Response, request, redirect, url_for

from flask import send_from_directory

date = date.today().strftime("%d/%m/%Y")
black = (1,1,1)
white = (255,255,255)
speech_config = speechsdk.SpeechConfig(subscription="SUBSCRIPTION_ID", region="eastus")
global speech_synthesizer,speech_recognizer
def choose_lang(ch):
    global speech_synthesizer,speech_recognizer
    if ch=='English':
        speech_config.speech_synthesis_language = "en-IN" 
        speech_config.speech_synthesis_voice_name ="en-IN-NeerjaNeural"
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        speech_config.speech_recognition_language="en-IN"
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    elif ch=='Telugu':
        speech_config.speech_synthesis_language = "te-IN" 
        speech_config.speech_synthesis_voice_name ="te-IN-ShrutiNeural"
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        speech_config.speech_recognition_language="te-IN"
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    elif ch=='Hindi':
        speech_config.speech_synthesis_language = "hi-IN" 
        speech_config.speech_synthesis_voice_name ="hi-IN-SwaraNeural"
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        speech_config.speech_recognition_language="hi-IN"
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
global Name, Age, Gender, Symptom, Diagnosis, Advice, bill_amt, med, af_bf, amt, t_med, Medicine
Name = ""
Medicine=[]
Age = ""
Gender= ""
Symptom = ""
Diagnosis = ""
Advice = ""
bill_amt="Rs."
med=""
af_bf=""
amt=""
t_med=""
global Serial_No
Serial_No=random.randint(1,99999)

def serial_number():
    global Serial_No
    Serial_No = Serial_No+1
    generate()

def amount(x):
    global amt
    amt=x
    generate()
    
def af_bf(x):
    global af_bf
    af_bf=x
    generate()
    
def time_med(x):
    global t_med
    t_med=x;
    generate()
def name(ch):
    global Name
    print("Name")
    
    if ch=='English':
        voice = speech_synthesizer.speak_text_async("Name").get()
    elif ch=='Telugu':
        voice = speech_synthesizer.speak_text_async("పేరు").get()
    elif ch=='Hindi':   
        voice = speech_synthesizer.speak_text_async("नाम").get()
    print(voice.reason)
    if voice.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('done')
    elif voice.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = voice.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    
    Name = result.text
    print(Name)
    generate(ch)
# name()
def age(ch):
    global Age
    print(speech_synthesizer)
    if ch=='English':
        voice = speech_synthesizer.speak_text_async("Age").get()
    elif ch=='Telugu':
        voice = speech_synthesizer.speak_text_async("వయస్సు").get()
    elif ch=='Hindi':   
        voice = speech_synthesizer.speak_text_async("उम्र").get()
    print(voice.reason)
    if voice.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('done')
    elif voice.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = voice.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get() 
    
    Age = result.text
    print(Age)
    generate(ch)
# age()
def gender(ch):
    global Gender

    if ch=='English':
        voice = speech_synthesizer.speak_text_async("Gender").get()
    elif ch=='Telugu':
        voice = speech_synthesizer.speak_text_async("లింగం").get()
    elif ch=='Hindi':   
        voice = speech_synthesizer.speak_text_async("लिंग").get()
    print(voice.reason)
    if voice.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('done')
    elif voice.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = voice.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    res = result.text.lower()
    print(result.text)
    if ch=='English':
        if res=='mail':
            res='male'
        elif res=='email':
            res='female'

    Gender =  res
    print(Gender)
    generate(ch)
# gender()
def symptoms(ch):
    global Symptom

    if ch=='English':
        voice = speech_synthesizer.speak_text_async("Symptoms").get()
    elif ch=='Telugu':
        voice = speech_synthesizer.speak_text_async("లక్షణాలు").get()
    elif ch=='Hindi':   
        voice = speech_synthesizer.speak_text_async("लक्षण").get()
    print(voice.reason)
    if voice.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('done')
    elif voice.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = voice.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    
    Symptom = result.text
    print(Symptom)
    generate(ch)
# symptoms()
def diagnosis(ch):
    global Diagnosis

    if ch=='English':
        voice = speech_synthesizer.speak_text_async("Diagnosis").get()
    elif ch=='Telugu':
        voice = speech_synthesizer.speak_text_async("నిర్ధారణ").get()
    elif ch=='Hindi':   
        voice = speech_synthesizer.speak_text_async("निदान").get()
    print(voice.reason)
    if voice.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('done')
    elif voice.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = voice.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    Diagnosis = result.text
    print(Diagnosis)
    generate(ch)
# diagnosis()
    
def advice(ch):
    global Advice

    if ch=='English':
        voice = speech_synthesizer.speak_text_async("Advice").get()
    elif ch=='Telugu':
        voice = speech_synthesizer.speak_text_async("సలహా").get()
    elif ch=='Hindi':   
        voice = speech_synthesizer.speak_text_async("सलाह").get()
    print(voice.reason)
    if voice.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print('done')
    elif voice.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = voice.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

    print("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()
    
    Advice = result.text
    print(Advice)
    generate(ch)
# advice()
foreground_image = Image.open('LC_Prescription.png')
def save():
    foreground_image.save("prescription_" + str(Serial_No) + ".png")
def generate(ch):
    write(str(Name),130,210,ch)
    write(str(Age),530,210,ch)
    write(str(Gender),680,210,ch)
    write(str(Symptom),150,270,ch)
    write(str(Diagnosis),40,450,ch)
    write(str(Advice),40,700,ch)
    write(str(date),95,320,ch)
def write(text,x,y,ch):
    if ch=='Telugu':
        font=ImageFont.truetype("Pothana2000.ttf",size=25,layout_engine=ImageFont.LAYOUT_RAQM)
    else:
        font=ImageFont.truetype("ArialUnicodeMS.ttf",size=25,layout_engine=ImageFont.LAYOUT_RAQM)
    draw = ImageDraw.Draw(foreground_image)
    draw.text((x, y), text,font=font, fill="black")


app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'  
app.config['MAIL_PORT']=465  
app.config['MAIL_USERNAME'] = 'SENDER_EMAIL' 
app.config['MAIL_PASSWORD'] = 'SENDER_PASS'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  

mail = Mail(app) 

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')
    
@app.route("/")  
def index():
    return render_template('index.html')

@app.route("/lang")
def background_test():
    return render_template('language.html')

@app.route("/voice_presc", methods=['POST'])
def voice():
    lang=request.form.get("language")
    choose_lang(lang)
    while(True):    

        # Exception handling to handle
        # exceptions at the runtime
        try:
            
            name(lang)

            age(lang)

            gender(lang)

            symptoms(lang)

            diagnosis(lang)

            advice(lang)

            save() 
            email_prescription()
            send_msg(lang)

            break

        except:
            print("Could not request results!")
    return render_template('sendmail.html')

@app.route("/thank_user", methods=['POST'])
def thanks():
    recipient=request.form.get('email')
    email_prescription(recipient)
    return render_template('thanks.html')

def send_msg(ch):
    account_sid ='TWILIO_ACCOUNT_SID'
    auth_token = 'TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)

    #This is a sample message sent to user
    if ch=='English':
        message = client.messages.create(
                                      body='Greetings! The bill amount for your current visit is Rs.1500. Your next visit is ' + Advice ,
                                      from_='SENDER',
                                      to='RECEIVER'
                                  )
    elif ch=='Telugu':
        message = client.messages.create(
                                      body='నమస్కారం! మీ ప్రస్తుత సందర్శన కోసం బిల్లు మొత్తం రూ.1500. మీ తదుపరి సందర్శన '+ Advice,
                                      from_='SENDER',
                                      to='RECEIVER'
                                  )        
    elif ch=='Hindi':
        message = client.messages.create(
                                      body='नमस्ते! आपकी वर्तमान यात्रा के लिए बिल राशि 1500 रुपये है। आपकी अगली यात्रा है ' + Advice,
                                      from_='SENDER',
                                      to='RECEIVER'
                                  )        

    print(message.sid)

def email_prescription(recipient):  
    msg = Message(subject = "Prescription_" + str(Serial_No), body = "Please find your attachment of prescription", sender = "kvsls2001@gmail.com", recipients = recipient.split())  
    with app.open_resource("prescription_" + str(Serial_No) + ".png") as fp:  
        msg.attach("prescription_" + str(Serial_No) + ".png","image/png",fp.read())  
        with app.app_context():
            mail.send(msg)  
    return "sent"  


if __name__ == "__main__":
    app.run()