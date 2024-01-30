import pyaudio
import wave
from threading import Thread
import numpy as np
from collections import deque
import time
# from deepgram import Deepgram
# import asyncio
# import aiohttp


class Record(Thread):

    def __init__(self, seconds=5, device_input_index=2, device_output_index=4,buffer_ratio = 0.7):
        super().__init__()
        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
        with wave.open('./temp/'+'understand'+'.wav', "rb") as f:
            CHUNK = 1024
            FORMAT = self.p.get_format_from_width(f.getsampwidth())
            print(FORMAT)
            CHANNELS = 1
            print(CHANNELS)
            RATE = f.getframerate()
            print(RATE)
            self.chunk = 1024  # Record in chunks of 1024 samples

            self.sample_format = FORMAT  # 16 bits per sample
            self.channels = CHANNELS
            self.fs = f.getframerate()  # Record at 44100 samples per second
            
            self.buffer_ratio = buffer_ratio
        self.seconds = seconds
        self.device_input_index = device_input_index
        self.device_output_index = device_output_index

        self.buffer = deque()

        self.is_over = False

        self.stream = None

        self.last_name = ''

        self.is_playing = False

    def get_device_input_names(self):
        self.in_device_names_dict = {}
        for i in range(self.p.get_device_count()):

            device_info = self.p.get_device_info_by_index(i)

            if device_info['maxInputChannels'] > 0:
                if self.in_device_names_dict.get(device_info['name']) == None:
                    self.in_device_names_dict[device_info['name']] = i

        return self.in_device_names_dict.keys()

    def set_device_input_index(self, device_name):
        self.in_device_input_index = self.in_device_names_dict.get(device_name)

    def get_device_output_names(self):
        self.out_device_names_dict = {}
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            # print(device_info)
            if device_info['maxOutputChannels'] > 0:
                if self.out_device_names_dict.get(device_info['name']) == None:
                    self.out_device_names_dict[device_info['name']] = i

        return self.out_device_names_dict.keys()

    def set_device_output_index(self, device_output_name):
        self.device_output_index = self.out_device_names_dict[device_output_name]

    def run(self,):
        self.stream = self.p.open(format=self.sample_format,
                                  channels=self.channels,
                                  rate=self.fs,
                                  frames_per_buffer=self.chunk,
                                  input=True, input_device_index=self.device_input_index, output=True, output_device_index=self.device_output_index)
        
        
        length = 0
        max_length = int(self.fs / self.chunk * self.seconds)
        while self.is_over == False:
            data = self.stream.read(self.chunk)
            self.buffer.append(data)
            length += 1
            if length >= max_length:
                self.GetWave()
                while length > int(max_length*self.buffer_ratio):
                    self.buffer.popleft()
                    length -= 1

        self.stream.stop_stream()
        self.stream.close()

    def endRecord(self):
        self.need_end = True
        pass

    def GetBuffer(self):

        return np.array(self.buffer, dtype=np.float32)

    def GetWave(self):
        wf = wave.open('temp/111.wav', 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.buffer))
        wf.close()

    def playWave(self, name, detect=None, first_name=None):
        time.sleep(0.1)
        if name == " " or name == "":
            return
        elif name == self.last_name:
            return
        else:
            with wave.open('./temp/'+name.replace(' ', '1')+'.wav', "rb") as f:
                self.is_playing = True
                detect.num_dict[first_name] += 1

                data = f.readframes(self.chunk)

                while len(data) > 0:

                    self.stream.write(data)
                    data = f.readframes(self.chunk)

                self.is_playing = False
            self.last_name = name
            Thread(target=self.last_name_thread).start()

    def last_name_thread(self):
        temp = self.last_name
        time.sleep(self.seconds)
        if self.last_name == temp:
            self.last_name = ""


if __name__ == "__main__":
    record = Record()
    record.start()
    # record.GetWave()
    # record.endRecord()
