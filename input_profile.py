import numpy as np


def sweep_60s_40Hz(x, t=60):
    f_start = 0  # Start frequency (Hz)
    f_end = 40  # End frequency (Hz)
    duration = 60
    amplitude = 0.02  # Amplitude of the sine wave

    # Sweep parameters
    k = (f_end - f_start) / duration  # Frequency rate for linear sweep

    # Calculate instantaneous frequency
    instantaneous_frequency = f_start + k * x  # Linear sweep

    # Calculate phase
    phase = 2 * np.pi * (f_start * x + 0.5 * k * x ** 2)

    # Generate sine wave
    y = amplitude * np.sin(phase)

    return y


def road_bump(x, center=1.5, width=0.025, height=0.02):
    return height * np.exp(-((x - center) ** 2) / (2 * (width ** 2)))
