from __future__ import print_function
from .utils import get_files_from_dir
import random
import math

from pydub.effects import compress_dynamic_range


def randF(min, max, divisor = 1000):
    r = random.randint(int(min * divisor), int(max * divisor))
    return r / divisor

# TRANSFORMS
def changeGain(sound, max_amount_of_gain=50, makeup = 0):
    #print('play with gain')
    gain = random.randint(0, max_amount_of_gain)
    return sound.apply_gain(-sound.max_dBFS - gain + makeup)

def addCompression(sound):
    #print('play with compression')

    threshold = randF(-40, 0)
    ratio = randF(0, 10)
    attack = randF(0, 10)
    release = randF(0, 500)
    return compress_dynamic_range(sound, threshold=threshold, ratio=ratio, attack=attack, release=release)

def changePitch(sound, min = -0.5, max = 0.5):
    #print('play with pitch')

    octaves = randF(min, max)
    # shift the pitch up by half an octave (speed will increase proportionally)
    new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))

    return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(44100)

def mixWith(sound, overlay):
    if len(overlay) < len(sound):
        orig_overlay = overlay
        times = len(sound)/len(overlay)
        for i in range(1, math.ceil(times)):
            overlay = overlay + orig_overlay

    length = len(sound)
    rand_start = random.randint(0, len(overlay) - length)
    mixed_sound = sound.overlay(overlay[rand_start:rand_start + length])
    assert len(mixed_sound) == len(sound), "Lengths don't match post mixing, original: %i, transformed: %i" % (len(sound), len(mixed_sound))

    return mixed_sound
