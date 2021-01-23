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
        prog="segment_clicks.py",
        description="Apply beat, downbeat, and structural segmentation analyses for harmonixset presentation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("wav_in", help="input wav file")
    parser.add_argument("segment_wav_out", help="output segment wav file")

    args = parser.parse_args()

    print("Loading file {0} with 44100 sampling rate".format(args.wav_in))
    x = load_wav(args.wav_in)

    # copy-pasted in from librosa_plot_segmentation.py
    segment_times = [0.58049887, 8.08054422, 11.74929705, 14.09451247]

    silence = numpy.zeros(int(0.5*44100))

    index = [int(s*44100) for s in segment_times]
    print(index)
    for i in index:
        x = numpy.concatenate((x[:i], silence, x[i:]))

    print("Writing outputs with pauses to {0}".format(args.segment_wav_out))
    write_wave_file(x, args.segment_wav_out, sample_rate=44100)

if __name__ == '__main__':
    main()
