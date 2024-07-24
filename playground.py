from music21 import converter, note, stream

# ABC notation as a string
abc_notation = """
X:1
T:ABDUL ABULBUL AMEER
M:3/4
L:1/4
K:D
 z2 F| F E ^D| E F G| B A ^G| A2A/2-A/2| d c d| e d B| A3| z2 A/2A/2|\
 A E E| E F G| B A F| d2F/2-F/2| A A A| G F E| D3-| D z2|
"""

# Parse the ABC notation
abc_stream = converter.parse(abc_notation, format='abc')

# Extract notes from the stream
notes = abc_stream.flat.notes

# Print extracted notes and their MIDI numbers
for n in notes:
    if isinstance(n, note.Note):
        print(f"Note: {n.nameWithOctave}, MIDI Number: {n.pitch.midi}, Duration: {n.quarterLength}")
    elif isinstance(n, note.Rest):
        print(f"Rest: Duration: {n.quarterLength}")

# Convert the stream to a MIDI file
mf = abc_stream.write('midi', fp='output/output.mid')

print("MIDI file created successfully!")
