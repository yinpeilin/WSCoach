# import whisper
import time
# from deepgram import Deepgram
import asyncio
import json
import sys
from faster_whisper import WhisperModel as fasterWhisper


# class WhisperModel():
#     def __init__(self, model_size="tiny.en", download_root='MODEL', device='cpu', in_memory=True):
#         self.model = whisper.load_model(
#             model_size, download_root=download_root, device=device, in_memory=True)

#     def TranscribeFile(self, fileName):
#         result = self.model.transcribe(fileName)
#         return result["text"]

#     def TranscribeArray(self, buffer):
#         result = self.model.transcribe(buffer)
#         return result["text"]

# class DeepgramModel():
#     def __init__(self):
#         self.DEEPGRAM_API_KEY = 'xxxx'
#         self.deepgram = Deepgram(self.DEEPGRAM_API_KEY)
#         self.text = ''

#     async def TranscribeFile(self, fileName):
#         audio = open(fileName, 'rb')
#         source = {
#             'buffer': audio,
#             'mimetype': 'wav'
#         }
#         response = await asyncio.create_task(
#             self.deepgram.transcription.prerecorded(
#                 source,
#                 {
#                     'smart_format': True,
#                     'model': 'nova',
#                 }
#             )
#         )
#         self.text = response['results']

#         return self.text


class FasterWhisperModel():
    def __init__(self, model_size="medium.en", download_root='MODEL/FASTER', in_memory=True):
        self.model = fasterWhisper(
            model_size, download_root=download_root, num_workers=4, cpu_threads=8)

    def TranscribeFile(self, fileName):
        try:
            segments, info = self.model.transcribe(fileName)
            text = ''
            for segment in segments:
                print(segment)
                if segment.no_speech_prob < 0.65:
                    text += segment.text
            return text
        except:
            return ''

    def TranscribeArray(self, buffer):
        result = self.model.transcribe(buffer)
        return result["text"]


if __name__ == "__main__":
    # model = DeepgramModel()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(model.TranscribeFile("./temp/1.wav"))
    # print(model.text)
    model = FasterWhisperModel()
    text = model.TranscribeFile("./temp/understand.wav")
    print(text)
