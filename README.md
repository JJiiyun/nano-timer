# Nano-timer

Nano-timer is a program that utilizes Digilent's Analog Discovery 2 to generate waveforms for specific durations while measuring and analyzing impedance in real-time. The measured data is visualized in real-time and can be saved as .csv files for subsequent analysis.

## Requirements

- **Python**: The program runs stably on Python 3.9.x or lower versions
- **Development Environment**: Developed and tested in Python 3.8.8

## Key Features

### Waveform Generation
- Generates precise waveforms through Analog Discovery 2 for user-defined durations

### Real-time Data Visualization
- Displays sine wave signals measured from Channel 1 and Channel 2 in real-time graphs
- Provides intuitive monitoring of signal changes

### Impedance Calculation and Analysis
- Calculates impedance values in real-time based on channel data
- Visualizes impedance trends through dynamic graphs

### Data Export
- Exports all experimental data including waveforms and impedance measurements
- Saves data in .csv format for easy analysis and storage
