import numpy as np
from math import *


def input_profile(x):
    f_start = 0  # Start frequency (Hz)
    f_end = 40  # End frequency (Hz)
    duration = 10  # Total duration of the sweep (seconds)
    amplitude = 0.01  # Amplitude of the sine wave

    # Sweep parameters
    k = (f_end - f_start) / duration  # Frequency rate for linear sweep

    # Calculate instantaneous frequency
    instantaneous_frequency = f_start + k * x  # Linear sweep

    # Calculate phase
    phase = 2 * np.pi * (f_start * x + 0.5 * k * x ** 2)

    # Generate sine wave
    y = amplitude * np.sin(phase)

    return y