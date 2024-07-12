from music21 import converter, note, chord, stream


# Function to convert ABC notation to sequences of notes and durations
def abc_to_sequence(abc_string):
    # Parse the ABC notation
    abc_score = converter.parse(abc_string, format='abc')

    note_sequence = []
    duration_sequence = []

    # Extract notes and durations
    for element in abc_score.flat.notes:
        if isinstance(element, note.Note):
            note_sequence.append(element.pitch.midi)
            duration_sequence.append(element.quarterLength)
        elif isinstance(element, chord.Chord):
            # If the element is a chord, pick the root note or handle as needed
            note_sequence.append(element.root().pitch.midi)
            duration_sequence.append(element.quarterLength)

    return note_sequence, duration_sequence


# Example ABC notation string
abc_string = """
X: 1
T: Scale
M: 4/4
K: C
C D E F | G A B c |
"""

# Convert ABC notation to sequences
note_sequence, duration_sequence = abc_to_sequence(abc_string)

print(f"Note Sequence: {note_sequence}")
print(f"Duration Sequence: {duration_sequence}")

# Define vocabulary for notes (MIDI pitches 0-127)
note_vocab = {i: i for i in range(128)}

# Define vocabulary for durations (buckets for simplicity, e.g., 0.25, 0.5, 1, etc.)
# This example assumes you are using quarter lengths as duration units
duration_vocab = {0.25: 1, 0.5: 2, 1.0: 3, 2.0: 4}  # Example for simplicity

# Function to tokenize sequences
def tokenize_sequence(note_sequence, duration_sequence):
    tokenized_notes = [note_vocab[note] for note in note_sequence]
    tokenized_durations = [duration_vocab[duration] for duration in duration_sequence if duration in duration_vocab]
    return tokenized_notes, tokenized_durations

# Tokenize the sequences
tokenized_notes, tokenized_durations = tokenize_sequence(note_sequence, duration_sequence)

print(f"Tokenized Note Sequence: {tokenized_notes}")
print(f"Tokenized Duration Sequence: {tokenized_durations}")

import pickle

# Define a path to save tokenized sequences
save_path = 'model/tokenized_sequences.pkl'

# Save tokenized sequences using pickle
with open(save_path, 'wb') as f:
    pickle.dump((tokenized_notes, tokenized_durations), f)


# Load tokenized sequences
with open(save_path, 'rb') as f:
    loaded_tokenized_notes, loaded_tokenized_durations = pickle.load(f)

# Example: Access the loaded tokenized sequences
print(f"Loaded Tokenized Note Sequence: {loaded_tokenized_notes}")
print(f"Loaded Tokenized Duration Sequence: {loaded_tokenized_durations}")


