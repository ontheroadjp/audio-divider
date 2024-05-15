import re
import sys
import os
import speech_recognition as sr
from pydub import AudioSegment

def split_audio(input_audio):
    # 出力ディレクトリ
    output_dir = os.path.join('dist', os.path.splitext(os.path.basename(input_audio))[0])

    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 無音部分のタイムスタンプを取得
    with open(os.path.join('dist', os.path.basename(input_audio) + '.txt'), 'r') as file:
        silence_data = file.read()

    # タイムスタンプのリストを作成
    timestamps = [0.0]
    matches = re.findall(r'silence_end: (\d+\.\d+)', silence_data)
    timestamps += [float(match) for match in matches]

    # 最後のタイムスタンプを取得
    duration_match = re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)', silence_data)
    if duration_match:
        hours, minutes, seconds = map(float, duration_match.groups())
        total_duration = hours * 3600 + minutes * 60 + seconds
        timestamps.append(total_duration)
    else:
        print("Error: Could not determine the total duration of the audio file.")
        sys.exit(1)

    # 音声認識の初期化
    recognizer = sr.Recognizer()

    # 音声を分割して mp3 形式で保存
    for i in range(len(timestamps) - 1):
        start_time = timestamps[i] * 1000  # pydubはミリ秒単位を使用
        end_time = timestamps[i + 1] * 1000
        duration = end_time - start_time
        output_temp_file = os.path.join(output_dir, f'temp_{i+1}.wav')

        # 分割された音声を一時ファイルとして保存
        audio = AudioSegment.from_file(input_audio)
        segment = audio[start_time:end_time]
        segment.export(output_temp_file, format="wav")

        # 音声認識を使用して英単語を抽出
        with sr.AudioFile(output_temp_file) as source:
            audio_data = recognizer.record(source)
            try:
                word = recognizer.recognize_google(audio_data)
                word = re.sub(r'\W+', '', word)  # ファイル名に使用できない文字を除去
            except sr.UnknownValueError:
                word = f'unknown_{i+1}'

        # 連番をゼロ埋めで付与し、ファイル名を英単語にしてmp3形式で保存
        output_file = os.path.join(output_dir, f'{i+1:03d}_{word}.mp3')
        segment.export(output_file, format="mp3")

        # 一時ファイルを削除
        os.remove(output_temp_file)

        print(f'Created {output_file} from {start_time/1000} to {end_time/1000}')

if __name__ == "__main__":
    # コマンドライン引数から入力ディレクトリまたはファイルを取得
    input_path = sys.argv[1]

    # 入力がディレクトリかどうかをチェック
    if os.path.isdir(input_path):
        # 入力がディレクトリの場合

        # ディレクトリ内の音声ファイルを処理
        for filename in os.listdir(input_path):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                input_audio = os.path.join(input_path, filename)
                split_audio(input_audio)
    else:
        # 入力が単体のファイルの場合
        split_audio(input_path)

