import os
from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np

class AudioGenerator:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.note_frequencies = {
            'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13,
            'E4': 329.63, 'F4': 349.23, 'F#4': 369.99, 'G4': 392.00,
            'G#4': 415.30, 'A4': 440.00, 'A#4': 466.16, 'B4': 493.88,
            'C5': 523.25, 'C#5': 554.37, 'D5': 587.33, 'D#5': 622.25,
            'E5': 659.25, 'F5': 698.46, 'F#5': 739.99, 'G5': 783.99,
            'G#5': 830.61, 'A5': 880.00, 'A#5': 932.33, 'B5': 987.77
        }

    def generate_note(self, note_name, duration_ms=1000):
        """生成指定音符的音频"""
        if note_name not in self.note_frequencies:
            raise ValueError(f"Invalid note name: {note_name}")
        
        frequency = self.note_frequencies[note_name]
        # 使用正弦波生成音符
        sine_wave = Sine(frequency, sample_rate=self.sample_rate)
        audio = sine_wave.to_audio_segment(duration=duration_ms)
        
        # 添加淡入淡出效果
        audio = audio.fade_in(50).fade_out(50)
        return audio

    def generate_silence(self, duration_ms):
        """生成指定时长的静音"""
        return AudioSegment.silent(duration=duration_ms)

    def get_random_notes(self, num_pairs=10, min_octave=4, max_octave=5):
        """生成随机音符对"""
        notes = []
        for _ in range(num_pairs):
            # 随机选择第一个音符
            first_note = np.random.choice(list(self.note_frequencies.keys()))
            # 随机选择第二个音符（确保在指定八度范围内）
            second_note = np.random.choice(list(self.note_frequencies.keys()))
            notes.append((first_note, second_note))
        return notes 