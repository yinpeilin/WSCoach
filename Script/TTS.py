import pyttsx4
import time
# engine = pyttsx4.init('nsss')
# # engine.setProperty('speaker_wav', './docs/i_have_a_dream_10s.wav')

# engine.setProperty('rate', rate)
# voices = engine.getProperty('voices')
# for voice in voices:
#     engine.setProperty('voice', voice.id)
#     engine.say('The quick brown fox jumped over the lazy dog.')
# engine.save_to_file(
#     'i am Hello World, i am a programmer. i think life is short.', 'test1.wav')
# engine.runAndWait()
class TTS():
    def __init__(self):
        self.engine = pyttsx4.init()
        self.initial_rate = self.engine.getProperty('rate')

    def SetRate(self, num):
        self.engine.setProperty('rate', self.initial_rate*num)

    def Word2File(self, text):
        if text != ' ':
            self.engine.save_to_file(
                text, './temp/'+text.replace(' ', '1')+'.wav')
            self.engine.runAndWait()



if __name__ == "__main__":
    tts = TTS()
