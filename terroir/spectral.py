from mmm_python import *
import math
import numpy as np
import array


def midi_to_hz_np(midicents: np.ndarray) -> np.ndarray:
    output = np.array([midicps(note) for note in midicents])
    return output


def midi_to_hz(midicents: list[float]) -> np.ndarray:
    output = np.array([midicps(note) for note in midicents])
    return output

def gen_spectrum_hz(fund: float, dist: float, start: int, amount: int):
    """
    Generates a spectrum, returned as an array.

    Args:
        fund: fundamental in hertz.
        dist: distortion coefficient (1.0 = no distortion, >1.0 = expanded <1.0 = compressed).
        start: the partial number to start from.
        amount: the amount of partials to generate.
    """
    spectrum = []
    for i in range(amount):
        partial = fund * pow(i + 1 + start, dist)
        spectrum = np.append(spectrum, cpsmidi(partial))
    return spectrum

def gen_spectrum_n_hz(fund: float, dist: float, partiels:array.array[int]):
    """
    Generates the given partials from a fundamental in hertz, returned as an array

    :param fund: fundamental in hertz
    :param dist: distortion coefficient (1.0 = no distortion, >1.0 = expanded <1.0 = compressed)
    :param partiels: the partials to generate
    """
    spectrum = []
    for i in partiels:
        partial = fund * pow(i, dist)
        spectrum = np.append(spectrum, cpsmidi(partial))
    return spectrum



def gen_spectrum(fund:float, dist:float, start:int, amount:int):
    """
    Generates a spectrum from a given midi number, returned as an array

    :param fund: fundamental in midicents
    :param dist: distortion coefficient (1.0 = no distortion, >1.0 = expanded <1.0 = compressed)
    :param start: the partial number to start from
    :param amount: the amount of partials to generate
    """
    spectrum = []
    conv_fund = midicps(fund) 
    for i in range(amount):
        partial = conv_fund * pow(i + 1 + start, dist)
        spectrum = np.append(spectrum, cpsmidi(partial))
    return spectrum

def gen_spectrum_n(fund: float, dist: float, partiels: array.array[int]):
    """
    Generates the given partials from a fundamental in midicents, returned as an array

    :param fund: fundamental in hertz
    :param dist: distortion coefficient (1.0 = no distortion, >1.0 = expanded <1.0 = compressed)
    :param partiels: the partials to generate
    """
    
    spectrum = []
    conv_fund = midicps(fund) 
    for i in partiels:
        partial = conv_fund * pow(i, dist)
        spectrum = np.append(spectrum, cpsmidi(partial))
    return spectrum


def ring_mod_hz(pitch1: float = 30, pitch2: float = 440) -> np.ndarray:
    """
    Performs a ring modulation of two given frequencies, returned as an array

    :param pitch1: frequency 1
    :param pitch2: frequency 2
    """
    pitches = [cpsmidi(abs(pitch2 - pitch1)), cpsmidi(pitch2 + pitch1)]
    pitches = np.array(pitches)
    return pitches

def ring_mod(note1: float = 12, note2: float = 60) -> np.ndarray:
    """
    Performs a ring modulation of two given midi notes, returned as an array

    :param note1: midi note 1
    :param note2: midi note 2
    """
    conv1 = midicps(note1)
    conv2 = midicps(note2)
    pitches = np.array([cpsmidi(abs(conv2 - conv1)), cpsmidi(conv2 + conv1)])
    return pitches


def freq_shift_hz(notes: list[float], shift: float) -> np.ndarray:
    """
    Performs a frequency shift on the given frequencies, returned as an array

    :param notes: the frequencies to be shifted
    :param shift: the amount to shift by
    """
    output = []
    for i in notes:
        output.append(i + shift)

    return np.array(output)

def freq_shift(notes: list[float], shift: float) -> np.ndarray:
    """
    Performs a frequency shift on the given midi notes, returned as an array

    :param notes: the midi notes to be shifted
    :param shift: the amount to shift by
    """
    output = []
    for i in notes:
        shifted_note = midicps(i) + shift
        output.append(cpsmidi(shifted_note))

    return np.array(output)

