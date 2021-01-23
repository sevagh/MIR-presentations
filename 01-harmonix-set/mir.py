#!/usr/bin/env python3

import argparse
import matplotlib
import matplotlib.pyplot as plt
import sys
import json
import multiprocessing
import numpy
import librosa
from madmom.io.audio import load_audio_file, write_wave_file
import itertools
import madmom


def load_wav(wav_in):
    x, fs = load_audio_file(wav_in, sample_rate=44100)

    # stereo to mono if necessary
    if len(x.shape) > 1 and x.shape[1] == 2:
        x = x.sum(axis=1) / 2

    # cast to float
    x = x.astype(numpy.single)

    # normalize between -1.0 and 1.0
    x /= numpy.max(numpy.abs(x))

    print(x.shape)

    return x


def main():
    parser = argparse.ArgumentParser(
        prog="mir.py",
        description="Apply beat, downbeat, and structural segmentation analyses for harmonixset presentation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("wav_in", help="input wav file")
    parser.add_argument("beat_wav_out", help="output beat wav file")
    parser.add_argument("downbeat_wav_out", help="output downbeat wav file")
    parser.add_argument("onset_wav_out", help="output onset wav file")

    args = parser.parse_args()

    print("Loading file {0} with 44100 sampling rate".format(args.wav_in))
    x = load_wav(args.wav_in)

    proc_beat = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    act_beat = madmom.features.beats.RNNBeatProcessor()(x)

    # 4 beats per bar
    proc_downbeat = madmom.features.downbeats.DBNDownBeatTrackingProcessor(beats_per_bar=4, fps=100)
    act_downbeat = madmom.features.downbeats.RNNDownBeatProcessor()(x)

    beat_times = proc_beat(act_beat)

    true_downbeat_times = []
    downbeat_times = proc_downbeat(act_downbeat)
    for downbeat_location, downbeat_position in downbeat_times:
        if downbeat_position == 1:
            true_downbeat_times.append(downbeat_location)

    #onset_times = librosa.onset.onset_detect(y=x, sr=44100, units='time')

    # the way harmonixset does it
    hop = 512
    onset_frames = librosa.onset.onset_detect(y=x, sr=44100, hop_length=hop)
    onset_times = librosa.frames_to_time(onset_frames, sr=44100, hop_length=hop)

    print('beat times: {0}'.format(beat_times))
    print('downbeat times: {0}'.format(true_downbeat_times))
    print('onset times: {0}'.format(onset_times))

    print("Overlaying clicks at beat, downbeat, onset locations")

    beat_clicks = librosa.clicks(beat_times, sr=44100, length=len(x))
    downbeat_clicks = librosa.clicks(true_downbeat_times, sr=44100, length=len(x))
    onset_clicks = librosa.clicks(onset_times, sr=44100, length=len(x))

    beat_waveform = (x + beat_clicks).astype(numpy.single)
    downbeat_waveform = (x + downbeat_clicks).astype(numpy.single)
    onset_waveform = (x + onset_clicks).astype(numpy.single)

    print("Writing outputs with clicks to {0}, {1}, {2}".format(args.beat_wav_out, args.downbeat_wav_out, args.onset_wav_out))
    write_wave_file(beat_waveform, args.beat_wav_out, sample_rate=44100)
    write_wave_file(downbeat_waveform, args.downbeat_wav_out, sample_rate=44100)
    write_wave_file(onset_waveform, args.onset_wav_out, sample_rate=44100)

    #generate_all_plots(x, beat_times, downbeat_times, onset_times)


def generate_all_plots(
    x, beats, downbeats, onsets
):
    timestamps = [i / 44100.0 for i in range(len(x))]

    plt.figure(1)
    plt.title("Waveform with beats, downbeats, onsets")
    plt.plot(timestamps, x)
    plt.xlabel("time (seconds)")
    plt.ylabel("amplitude")
    plt.plot(
        beats,
        numpy.zeros(len(beats)),
        marker="o",
        linestyle="None",
        markersize=10,
        color="red",
    )
    plt.plot(
        downbeats,
        numpy.zeros(len(downbeats)),
        marker=".",
        linestyle="None",
        markersize=10,
        color="red",
    )
    plt.plot(
        onsets,
        numpy.zeros(len(onsets)),
        marker="x",
        linestyle="None",
        markersize=10,
        color="yellow",
    )
    plt.show()


if __name__ == "__main__":
    main()
