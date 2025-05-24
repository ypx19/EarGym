import os
from audio_generator import AudioGenerator
from video_generator import VideoGenerator
import argparse
from pydub import AudioSegment

def main():
    parser = argparse.ArgumentParser(description='生成相对音感训练视频')
    parser.add_argument('--num_pairs', type=int, default=10, help='要生成的音符对数量')
    parser.add_argument('--output', type=str, default='output.mp4', help='输出视频文件名')
    args = parser.parse_args()

    # 创建临时目录
    os.makedirs('temp', exist_ok=True)

    # 初始化生成器
    audio_gen = AudioGenerator()
    video_gen = VideoGenerator()

    # 生成随机音符对
    note_pairs = audio_gen.get_random_notes(num_pairs=args.num_pairs)
    
    # 生成音频
    combined_audio = AudioSegment.empty()
    for note1, note2 in note_pairs:
        # 生成第一个音符
        audio1 = audio_gen.generate_note(note1, duration_ms=1000)
        # 生成第二个音符
        audio2 = audio_gen.generate_note(note2, duration_ms=1000)
        # 生成静音
        silence = audio_gen.generate_silence(duration_ms=4000)
        
        # 组合音频
        combined_audio += audio1 + audio2 + silence

    # 保存临时音频文件
    temp_audio_file = 'temp/temp_audio.wav'
    combined_audio.export(temp_audio_file, format='wav')

    # 生成视频
    video_gen.generate_video(temp_audio_file, note_pairs, args.output)

    # 清理临时文件
    os.remove(temp_audio_file)
    os.rmdir('temp')

    print(f"视频已生成: {args.output}")

if __name__ == '__main__':
    main() 