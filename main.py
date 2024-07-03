import os

from music21 import converter, note, stream, meter
from collections import defaultdict
import random

abc_notation = """
% Generated more or less automatically by swtoabc by Erich Rickheit KSC
X:1
T:Adam In The Garden Pinnin' Leaves
M:2/2
L:1/4
K:F
 F2 A- F| F3/2 F/2 D C| G2 B3/2- G/2| c3/2 c/2 A F| c2 c z| B3/2 B/2 G G|\
 E/2G/2 E/2C/2 D C| F/2 F F3/2| F| _A F _E E/2C/2|D/2-_E/2 D/2 C/2- C F|\
 F/2F/2 F/2F/2 _E C| F/2 F F| A/2^G/2| A F F/2F/2 F|D/2-_E/2 D/2 C/2- C F|\
 F/2F/2 F/2F/2 D C| F/2 F F z||
"""
def extract_durations_by_bars(music_stream):
    durations_by_bars=[]
    for measure in music_stream.parts[0].getElementsByClass(stream.Measure):
        durations = []
        for element in measure.recurse().notesAndRests:
            durations.append(element.quarterLength)
        durations_by_bars.append(durations)
    print(f"durations_by_bars {durations_by_bars}")
    return durations_by_bars

def process_abc_notations(abc_directory, pattern):
    for filename in os.listdir(abc_directory):
        filepath = os.path.join(abc_directory, filename)
        with open(filepath, 'r') as file:
            abc_notation = file.read()
        score = converter.parse(abc_notation, format='abc')
        timesignature = extract_feature_timesignature(score)
        print(f"timesignature {filename} {timesignature}")
        if timesignature == '4/4' or timesignature=='1/4' or timesignature=='2/4' or timesignature=='2/2':
            durations_by_bars = extract_durations_by_bars(score)
            pattern.append(durations_by_bars)


def extract_feature_timesignature(music_stream):
    timesig = None
    # Find the time signature in the score
    time_signatures = music_stream.recurse().getElementsByClass(meter.TimeSignature)
    if time_signatures:
        for ts in time_signatures:
            timesig = ts.ratioString
    else:
        print("No time signature found in the score.")
    return timesig


# Function to generate new sequences using the Markov Chain
def generate_sequence(transitions, target_sum=4.0, max_repeats=2):
    sequence = []
    current_sum = 0
    repeats = defaultdict(int)

    while current_sum < target_sum:
        possible_notes = [note for note in transitions if note + current_sum <= target_sum]
        if not possible_notes:
            break

        current_note = random.choice(possible_notes)
        if repeats[current_note] < max_repeats:
            sequence.append(current_note)
            current_sum += current_note
            repeats[current_note] += 1
        else:
            # Reset current note selection if max_repeats is reached
            possible_notes.remove(current_note)
            if possible_notes:
                current_note = random.choice(possible_notes)
                sequence.append(current_note)
                current_sum += current_note
                repeats[current_note] += 1
            else:
                break

    # Adjust the last note to ensure the sum equals target_sum
    if current_sum < target_sum:
        remaining_sum = target_sum - current_sum
        if remaining_sum > 0:
            sequence.append(remaining_sum)

    return sequence

# Function to generate multiple groups of sequences
def generate_group_sequences(transitions, num_groups=5, sequences_per_group=10, target_sum=4.0, max_repeats=2):
    groups = []
    for _ in range(num_groups):
        group = []
        for _ in range(sequences_per_group):
            new_sequence = generate_sequence(transitions, target_sum, max_repeats)
            group.append(new_sequence)
        groups.append(group)
    return groups

if __name__=="__main__":

    patterns_duration = []

    # pass both array for append inside loop
    process_abc_notations('./dataset', patterns_duration)

    print(f"pattern  {patterns_duration}")

    # Flatten the sequences and create a Markov Chain
    transitions = defaultdict(list)
    for sequence in patterns_duration:
        for note_durations in sequence:
            for i in range(len(note_durations) - 1):
                current_note = note_durations[i]
                next_note = note_durations[i + 1]
                transitions[current_note].append(next_note)

    # Generate new groups of sequences
    num_groups = 5
    sequences_per_group = 10
    target_sum = 4.0
    max_repeats = 2

    new_groups = generate_group_sequences(transitions, num_groups, sequences_per_group, target_sum, max_repeats)

    # Print the new groups of sequences
    for i, group in enumerate(new_groups):
        print(f"Group {i + 1}:")
        for seq in group:
            print(seq)
        print("\n")