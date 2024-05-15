# audio-divider

python script to split audio files by silence.

## Installing

```bash
$ git clone
```



## usage

- Analyze the silent parts.

- The following command will output silence information in a text file in the dist directory
  
  （``input_audio.mp3`` is the original audio file）

- Argument can be a directory containing audio files instead of audio files

```bash
$ sh analyze_silence.sh input_audio.mp3
```

- The following command actually splits the audio using the silence information output above

- The split audio files are stored in the dist directory

- The file names of the split audio files are named after the audio is analyzed.

```bash
$ python split_audio.py input_audio.mp3
```



## require

- python 3 above

- ``speechrecognition`` and ``pydub`` python module

```bash
$ pip install speechrecognition pydub
```


