import pyaudio as pa
import copy
import time as t

from AmplifyClass import Amplify
from VibratoClass import Vibrato
from DelayClass import Delay
from PitchShiftClass import PitchShift


class SoundProcessor:

    def __init__(self):
        self.tick = 0
        self.p = pa.PyAudio()
        self.stream = self.p.open(
            format=pa.paInt16,
            channels=1,
            rate=44100,
            input_device_index=1,
            input=True,
            frames_per_buffer=1024
        )

        self.output = self.p.open(
            format=pa.paInt16,
            channels=1,
            rate=44100,
            output=True,
            frames_per_buffer=1024
        )
        self.output.start_stream()

        self.effects = {
            "amp": Amplify(),
            "vibrato": Vibrato(),
            "delay": Delay(),
            "pitchShift": PitchShift(),
        }

        self.inputFrame = []
        self.currentFrame = []

    @staticmethod
    def getGraphByFrame(frame, rect):
        lines = []
        if len(frame) > 0:
            x_diff = rect[2] / min(len(frame), 500)
            centre_y = (rect[1] + (rect[3] / 2))
            for n, amp in enumerate(frame[:min(len(frame), 500)]):
                lines.append((rect[0] + (x_diff * n), centre_y + (amp / 30)))
        else:
            lines = [(rect[0], rect[1]), (rect[0], rect[1])]

        return lines

    def update(self, fps: int, time: float):
        self.tick += 1

        data = self.stream.read(min(self.stream.get_read_available(), 2048))
        if len(data) > 0:
            self.inputFrame = []
            for i in range(0, len(data), 2):
                self.inputFrame.append(int.from_bytes(data[i:i + 2], byteorder="little", signed=True))

            self.currentFrame = copy.copy(self.inputFrame)
            for effect in self.effects.values():
                self.currentFrame = effect.process(self.currentFrame, self.tick, fps)

        output_frame = b''
        for i in self.currentFrame:
            if i > 32767:
                i = 32767
            elif i < -32768:
                i = -32768
            output_frame += int(i).to_bytes(2, "little", signed=True)

        self.output.write(output_frame)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
