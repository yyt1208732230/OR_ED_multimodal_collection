# The video synchronization steps include the utilizations of streaming and cv processing packages (librosa, moviepy).

# Something we need to know about the audios:
# 1. Sampling Rate
# 2. Bit Depth
# 3. Bit Rate

import os
import ast
import numpy as np
import copy
import calendar
import time
import argparse
import json
import logging
import matplotlib.pyplot as plt
import moviepy.editor
import cv2
import librosa
from envload import *
import datetime
import subprocess

#Load the Video Clip
# vclip_name = 'DJI_20230224204658_0004_D.mp4'
# vclip_name = 'Cam2_clipboard_close.MP4'
vclip_name = 'DJI_20230323185120_0021_D.MP4'
video_path = RGB_PATH + vclip_name
audio_path = "Audio" + vclip_name +".mp3"

vclip_name_list = ['Baseline//DJI_20230309174408_0008_D.MP4', ]

def getVideoClip(video_path):
    video = moviepy.editor.VideoFileClip(video_path)
    return video

def saveAudioFromVideo(video):
    audio = video.audio.write_audiofile(audio_path)
    return audio

def getVideoFrames(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened(): 
        print("could not open :",video_path)
        return
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length

def showFigureOnset(y, times, o_env):
    D = np.abs(librosa.stft(y))
    fig, ax = plt.subplots(nrows=2, sharex=True)
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                            x_axis='time', y_axis='log', ax=ax[0])
    ax[0].set(title='Power spectrogram')
    ax[0].label_outer()
    ax[1].plot(times, o_env, label='Onset strength')
    # ax[1].vlines(times[onset_frames], 0, o_env.max(), color='r', alpha=0.9,
    #            linestyle='--', label='Onsets')
    ax[1].legend()
    fig.show()
    pass

# Get clapboard timestamp in audio
def getMaxOnsetInAudio(audio_path):
    max_len = 3
    y, sr = librosa.load(audio_path)
    librosa.onset.onset_detect(y=y, sr=sr, units='time')

    o_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(o_env, sr=sr)
    showFigureOnset(y, times, o_env)
    # onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)
    # max_onset_frame = np.argmax(o_env)
    max_onset_frame = np.argsort(o_env)[-max_len:]
    max_onset = o_env[max_onset_frame]
    max_onset_time = times[max_onset_frame]
    len_frame_of_time = len(times)
    return max_onset, max_onset_frame, max_onset_time, len_frame_of_time

def subclipVideoByMaxOnset(video, maxonset):
    clipedVideo = video.subclip(maxonset)
    return clipedVideo

def get_mp4_timestamp(filename, time):
    mp4_timestamp = 0.0
    command = f"ffprobe -v error -select_streams v:0 -show_entries stream=pts_time -of csv=print_section=0 {filename}"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    timestamps = result.stdout.split('\n')[:-1]
    for timestamp in timestamps:
        if float(timestamp) <= time:
            mp4_timestamp = datetime.datetime.utcfromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S.%f')
    return mp4_timestamp

# 最大频谱通量值；最大频谱通量值所在帧；最大频谱通量值所在时间；音频文件总帧数；

_video = getVideoClip(video_path) 
saveAudioFromVideo(_video)
nframes = _video.reader.nframes #28084

max_onset, max_onset_frame, max_onset_time, len_frame_of_time = getMaxOnsetInAudio(audio_path)
print(max_onset, max_onset_frame, max_onset_time, len_frame_of_time)
start_time = max_onset_time[-1]
# Clip Video
# clipedVideo = subclipVideoByMaxOnset(_video, start_time)
# clipedVideo.write_videofile(video_path + "cliped.mp4")
# length = getVideoFrames(_video)
pass



# mp4_timestamp = get_mp4_timestamp(video_path, max_onset_time[-1])
# print(mp4_timestamp)


# clipedVideo = _video.subclip(32, 32+20)
# clipedVideo.write_videofile(video_path + "cliped10.mp4")
