from __future__ import annotations
from typing import Iterable
import gradio as gr
from Script.Record import Record
from Script.TTS import TTS
from Script.Model import FasterWhisperModel
from Script.Detect import Detect
import time
import torch
import threading
import copy
import asyncio
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes

class Seafoam(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.blue,
        secondary_hue: colors.Color | str = colors.blue,
        neutral_hue: colors.Color | str = colors.stone,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_very_large,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        
        super().set(
            # body_background_fill="repeating-linear-gradient(45deg, *primary_200, *primary_200 10px, *primary_50 10px, *primary_50 20px)",
            # body_background_fill_dark="repeating-linear-gradient(45deg, *primary_800, *primary_800 10px, *primary_900 10px, *primary_900 20px)",
            # button_primary_background_fill="linear-gradient(90deg, *primary_300, *secondary_400)",
            # button_primary_background_fill_hover="linear-gradient(90deg, *primary_200, *secondary_300)",
            # button_primary_text_color="white",
            # button_primary_background_fill_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            # slider_color="*secondary_300",
            # slider_color_dark="*secondary_600",
            block_title_text_weight="600",
            block_title_text_color="neutral_900"
            # block_border_width="3px",
            # block_shadow="*shadow_drop_lg",
            # button_shadow="*shadow_drop_lg",
            # button_large_padding="32px",
        )


seafoam = Seafoam()

class HTML():
    def __init__(self, record, detect, tts):

        self.last_audio_name = ''

        self.record = record
        self.detect = detect
        self.tts = tts
        self.model_wait = 0.1
        self.model_size = "medium.en"
        demo = gr.Blocks(theme=seafoam,)
        with demo:
            record_name = list(self.record.get_device_input_names())
            record_name.append("Huawei Eyewear Microphone")
            
            output_name = list(self.record.get_device_output_names())
            output_name.append("Huawei Eyewear Speaker")
            
            
            self.device_input_option = gr.Dropdown(choices= record_name,
                                                   label='device_input')
            self.device_output_option = gr.Dropdown(choices= output_name,
                                                    label='device_output')
            self.model_option = gr.Dropdown(choices=['tiny.en', 'base.en', 'small.en', 'medium.en', 'large.en'],
                                            label='model_size', interactive=True)
            self.speak_rate_slider = gr.Slider(
                0.2, 3.0, value=1.0, step=0.2, label="SpeakRate")

            self.model_wait_slider = gr.Slider(
                0.1, 3.0, value=0.5, step=0.1, label="model_wait")
            
            self.need_detect_word_input = gr.Textbox(
                placeholder="Unwanted_Word")
            self.play_word_input = gr.Textbox(placeholder="Spearcon_Word")

            self.device_input_option.change(
                fn=self.device_input_change, inputs=self.device_input_option, outputs=[])
            self.device_output_option.change(
                fn=self.device_output_change, inputs=self.device_output_option)
            self.model_option.change(
                fn=self.model_size_change, inputs=self.model_option)
            self.speak_rate_slider.change(
                fn=self.RateChange, inputs=self.speak_rate_slider)
            
            self.model_wait_slider.change(
                fn=self.ModelWaitChange, inputs=self.model_wait_slider)

            with gr.Row():
                self.add_button = gr.Button(value="Add", variant="primary")
                

                self.add_button.click(
                    fn=self.add_button_click, inputs=[self.need_detect_word_input, self.play_word_input])
                
            
            with gr.Row():
                self.start_button = gr.Button(value="Start", size='sm')
                self.stop_button = gr.Button(value="Stop", size='sm')
                self.start_button.click(fn=self.start_button_click)
                self.stop_button.click(fn=self.stop_button_click)
            self.detect_result_output = gr.TextArea(value=self.detect_result_change,label='Result',
                                                    interactive=False, every=1.0)

        demo.queue().launch()
        # self.time_delay_change_speaker = st.text_input(
        #     "time_delay_change_speaker", '3')

    def device_input_change(self, device_name):
        self.device_input_name = device_name

    def device_output_change(self, device_name):
        self.device_output_name = device_name

    def model_size_change(self, model_size):
        self.model_size = model_size

    def add_button_click(self, need_detect_word, play_word):
        self.detect.put(need_detect_word,
                        play_word)
        self.tts.Word2File(play_word)
        print("add successfully!")

    def start_button_click(self):
        self.ModelInit()
        self.thread = threading.Thread(target=self.StartRecord)
        self.thread.start()
        print("start!")

    def stop_button_click(self):
        self.record.is_over = True
        print("stop!")

    def detect_result_change(self):
        return str(self.detect)
    
    
    def StartRecord(self):
        print(1)
        self.record.is_over = False
        self.thread2 = threading.Thread(target=self.record.run)
        self.thread2.start()
        print(2)
        time1 = time.time()
        temp = 0
        while self.record.is_over == False:
            time.sleep(self.model_wait)
            text = self.model.TranscribeFile("./temp/111.wav")

            time2 = time.time()

            print((temp, text, time2-time1, self.record.last_name))

            if text.strip() != "":
                time1 = time.time()

            key, audio_name = self.detect.detect(text)

            self.record.playWave(audio_name, self.detect, key)
            # if time2-time1 > float(self.time_delay_change_speaker):
            #     temp += 1

    def ModelInit(self):
        self.record.set_device_input_index(self.device_input_name)
        self.record.set_device_output_index(self.device_output_name)
        self.model = FasterWhisperModel(model_size=self.model_size)

    def RateChange(self, rate):
        self.tts.SetRate(rate)
        for value in self.detect.dict.values():
            self.tts.Word2File(value)
        print("Set rate successfully!")
    def ModelWaitChange(self, seconds):
        self.model_wait = seconds
        print("Set model_wait successfully!")

if __name__ == "__main__":

    record = Record(seconds=10,buffer_ratio= 0.95)
    detect = Detect()
    tts = TTS()
    html = HTML(record, detect, tts)


