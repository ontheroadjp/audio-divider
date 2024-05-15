#!/bin/bash

# 入力ファイルまたはディレクトリのパスを取得
input_path=$1

# 出力ディレクトリ
output_dir='dist'

# 出力ディレクトリが存在しない場合は作成
if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
fi

# 入力がディレクトリかどうかをチェック
if [ -d "$input_path" ]; then
    # 入力がディレクトリの場合

    # ディレクトリ内の音声ファイルを処理
    for filename in "$input_path"/*.mp3 "$input_path"/*.wav; do
        if [ -f "$filename" ]; then
            echo "Analyzing $filename"
            # 無音部分を検出し、結果をファイルに保存
            ffmpeg -i "$filename" -af silencedetect=noise=-30dB:d=0.5 -f null - 2> "$output_dir/$(basename "$filename").txt"
        fi
    done
else
    # 入力が単体のファイルの場合

    echo "Analyzing $input_path"
    # 無音部分を検出し、結果をファイルに保存
    ffmpeg -i "$input_path" -af silencedetect=noise=-30dB:d=0.5 -f null - 2> "$output_dir/$(basename "$input_path").txt"
fi

