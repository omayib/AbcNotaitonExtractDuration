import mido
from mido import MidiFile, MidiTrack, Message
import random

# Define note values in terms of beats
note_values = [4, 2, 1, 0.5, 0.25]

# Define the C blues scale (C, E♭, F, F♯, G, B♭)
blues_scale = [60, 63, 65, 66, 67, 70]  # MIDI note numbers for C, E♭, F, F♯, G, B♭
arabian_scale = [60, 61, 64, 65, 67, 68, 70, 72]

# Function to generate combinations of note durations
def generate_combinations(time_signature_top, time_signature_bottom):
    measure_duration = (4 / time_signature_bottom) * time_signature_top
    combinations = []

    def find_combinations(current_combination, current_duration):
        if current_duration == measure_duration:
            combinations.append(current_combination)
            return
        elif current_duration > measure_duration:
            return

        for value in note_values:
            find_combinations(current_combination + [value], current_duration + value)

    find_combinations([], 0)
    return combinations

# Function to generate multiple bars
def generate_multiple_bars(num_bars, time_signature_top, time_signature_bottom):
    all_bars = []
    for _ in range(num_bars):
        combinations = generate_combinations(time_signature_top, time_signature_bottom)
        if combinations:
            random_combination = random.choice(combinations)
            all_bars.append(random_combination)
    return all_bars

# Map note durations to MIDI ticks (assuming 480 ticks per beat)
def duration_to_ticks(duration, ticks_per_beat=480):
    return int(duration * ticks_per_beat)

# Example usage
time_signature_top = 4
time_signature_bottom = 4
num_bars = 4

bars = generate_multiple_bars(num_bars, time_signature_top, time_signature_bottom)

# Create a new MIDI file
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Set the tempo (optional, default is 500000 microseconds per beat)
tempo = mido.bpm2tempo(60)
track.append(mido.MetaMessage('set_tempo', tempo=tempo))

# Add note events to the track using the blues scale
velocity = 64

for bar in bars:
    for duration in bar:
        ticks = duration_to_ticks(duration)
        pitch = random.choice(arabian_scale)
        track.append(Message('note_on', note=pitch, velocity=velocity, time=0))
        track.append(Message('note_off', note=pitch, velocity=velocity, time=ticks))

# Save the MIDI file
mid.save('arabian_scale_output.mid')

# Print the generated bars
for i, bar in enumerate(bars):
    print(f"Bar {i + 1}: {bar}")
