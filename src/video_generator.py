from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
import music21
import os

class VideoGenerator:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.fps = 30

    def get_interval_name(self, note1, note2):
        """获取两个音符之间的音程名称"""
        n1 = music21.note.Note(note1)
        n2 = music21.note.Note(note2)
        interval = music21.interval.Interval(n1, n2)

        return interval.niceName, interval.semitones

    def create_text_clip(self, text, duration, start_time):
        """创建文字片段"""
        txt_clip = TextClip(text, fontsize=70, color='white', bg_color='black',
                           size=(self.width, self.height), method='caption')
        txt_clip = txt_clip.set_start(start_time).set_duration(duration)
        return txt_clip

    def generate_video(self, audio_file, note_pairs, output_file='output.mp4'):
        """生成完整的训练视频"""
        # 加载音频
        audio = AudioFileClip(audio_file)
        
        # 创建视频片段列表
        clips = []
        current_time = 0
        
        # 为每对音符创建显示片段
        for note1, note2 in note_pairs:
            # 显示音符名称
            note_text = f"{note1} - {note2}"
            interval_name, interval_semitones = self.get_interval_name(note1, note2)
            answer_text = f"{note_text}\n{interval_name}\n{interval_semitones}"
            
            # 创建答案显示片段
            answer_clip = self.create_text_clip(answer_text, 2, current_time + 4)
            clips.append(answer_clip)
            
            current_time += 6  # 每个片段总时长：4秒静音 + 2秒显示答案
        
        # 合并所有片段
        final_clip = CompositeVideoClip(clips, size=(self.width, self.height))
        final_clip = final_clip.set_audio(audio)
        
        # 导出视频
        final_clip.write_videofile(output_file, fps=self.fps, codec='libx264')
        return output_file 