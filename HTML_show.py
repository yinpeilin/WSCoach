import streamlit as st
from Script.Record import Record
from Script.TTS import TTS
from Script.Model import FasterWhisperModel
from Script.Detect import Detect
import time
import torch
import threading
import copy
import asyncio
'''
 streamlit run ./HTML_show.py 
'''


class HTML():
    def __init__(self, record, detect, tts):

        self.last_audio_name = ''

        self.record = record
        self.detect = detect
        self.tts = tts
        self.device_input_option = st.selectbox(
            'device_input', (self.record.get_device_input_names())
        )
        self.device_output_option = st.selectbox(
            'device_output', (self.record.get_device_output_names())
        )
        self.model_option = st.selectbox(
            'model_size',
            ('tiny.en', 'base.en', 'small.en', 'medium.en', 'large.en'))

        if torch.cuda.is_available():
            self.device_option = st.selectbox(
                'model_to',
                ('cpu', 'cuda:0'))
        else:
            self.device_option = st.selectbox(
                'model_to',
                ('cpu'))

        self.time_delay_change_speaker = st.text_input(
            "time_delay_change_speaker", '3')
        self.rate = st.slider('SpeakRate', 0.2, 3.0, 1.0,
                              0.2, on_change=self.RateChange)

        self.need_detect_word = st.text_input(
            'need_detect_word', '',)
        self.play_word = st.text_input('play_word', '')

        if st.button('add'):
            self.detect.put(copy.deepcopy(self.need_detect_word),
                            copy.deepcopy(self.play_word))
            self.tts.Word2File(self.play_word)
            st.text("add successfully")

        if st.button('StartDetect'):
            self.ModelInit()
            self.thread = threading.Thread(target=self.StartRecordloop)
            self.thread.start()
            self.StartRecordloop()

        if st.button('Stop'):
            self.EndRecordloop()

        st.text(str(self.detect))

    def StartRecordloop(self):
        self.record.start()

        time1 = time.time()
        temp = 0
        while True:
            if self.record.is_playing == False:
                self.record.GetWave()
                text = self.model.TranscribeFile("./temp/111.wav")

                time2 = time.time()

                print((temp, text, time2-time1, self.record.last_name))

                if text.strip() != "":
                    time1 = time.time()

                audio_name = self.detect.detect(text)
                self.record.playWave(audio_name)

                if time2-time1 > float(self.time_delay_change_speaker):
                    temp += 1

    def EndRecordloop(self):
        self.record.endRecord()
        self.thread.terminate()

    def ModelInit(self):
        self.record.set_device_input_index(self.device_input_option)
        self.record.set_device_output_index(self.device_output_option)
        # self.model = WhisperModel(model_size=self.model_option)
        self.model = FasterWhisperModel(model_size=self.model_option)

    def RateChange(self):
        self.tts.SetRate(self.rate)
        for value in self.detect.dict.values():
            self.tts.Word2File(value)
        print("Set rate successfully!")


if __name__ == "__main__":

    record = Record(seconds=5)
    detect = Detect()
    tts = TTS()
    html = HTML(record, detect, tts)

    # while True:
    #     record.GetWave()
    #     time1 = time.time()

    #     print(whisper_model.TranscribeFile('123.wav'))
    #     time2 = time.time()
    #     print(time2 - time1)
