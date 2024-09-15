from music21 import converter
from collections import Counter
import matplotlib.pyplot as plt

# Your ABC notation as a string
abc_notation = """
X:1
T:Adam Catched Eve (round)
M:4/4
L:1/4
K:A
 A A A2| G2 F E| F3 F| E4| D D D2| C2 B, A,| B,3 E| A,4| z c c d| ed/2-c/2 B c|\
 d A A B| cB/2-A/2 G A| B F F G| A2 B- c| d2 c- B| c4| z A, A G/2F/2|\
 E2 z2| z A/2G/2 F E/2D/2| C2 z2| z F/2E/2 D C/2B,/2| A,2 z2| z C/2D/2 E F/2G/2|\
 A4|
"""

# Parse the ABC notation
score = converter.parseData(abc_notation, format='abc')
from music21 import note

# List to store (note_name, duration) tuples
durations = []

# Traverse all elements in the score
for element in score.recurse():
    if isinstance(element, note.Note):
        durations.append((element.nameWithOctave, element.duration.quarterLength))
    elif isinstance(element, note.Rest):
        durations.append(('Rest', element.duration.quarterLength))

# Display the extracted durations
for n, d in durations:
    print(f"Note: {n}, Duration: {d}")


# Extract just the durations
duration_values = [dur for _, dur in durations]

# Count the frequencies
duration_counts = Counter(duration_values)

# Display the counts
print("Duration Frequencies:")
for dur, count in duration_counts.items():
    print(f"Duration: {dur}, Count: {count}")
def find_repeating_patterns(sequence, min_length=2):
    patterns = {}
    n = len(sequence)
    for length in range(min_length, n//2 + 1):
        for i in range(n - length + 1):
            pattern = tuple(sequence[i:i+length])
            # Search for this pattern in the rest of the sequence
            count = 0
            for j in range(i + length, n - length + 1):
                if sequence[j:j+length] == list(pattern):
                    count += 1
            if count > 0:
                patterns[pattern] = count + 1  # Include the initial occurrence
    return patterns

# Find repeating patterns
duration_sequence = [dur for _, dur in durations]
patterns = find_repeating_patterns(duration_sequence)

# Display the patterns
print("\nRepeating Duration Patterns:")
for pattern, count in patterns.items():
    print(f"Pattern: {pattern}, Count: {count}")

# Plot the durations
plt.figure(figsize=(12, 4))
plt.plot(duration_sequence, marker='o')
plt.title('Note Durations')
plt.xlabel('Note Index')
plt.ylabel('Duration (Quarter Lengths)')
plt.grid(True)
plt.savefig('note_durations.png')

