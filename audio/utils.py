#设置麦克风
import speech_recognition as sr
import pyttsx3


def Speak(words):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 'zh')
    engine.say(words)
    # engine.say('The quick brown fox jumped over the lazy dog.')
    engine.runAndWait()
    pass



def Listen():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=11)
    #进行录音
    print('录音中...')
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    #进行识别
    print('录音结束，识别中...')
    command = r.recognize_google(audio, language='zh-CN')#这样设置language可以支持中文
    return command




