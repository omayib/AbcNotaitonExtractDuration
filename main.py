import os

from music21 import converter, note, stream

abc_notation = """
X:1
T:ABDUL ABULBUL AMEER
M:3/4
L:1/4
K:D
 z2 F| F E ^D| E F G| B A ^G| A2A/2-A/2| d c d| e d B| A3| z2 A/2A/2|\
 A E E| E F G| B A F| d2F/2-F/2| A A A| G F E| D3-| D z2|
"""
def extract_durations_by_bars(music_stream):
    durations_by_bars=[]
    for measure in music_stream.parts[0].getElementsByClass(stream.Measure):
        durations = []
        for element in measure.recurse().notesAndRests:
            durations.append(element.quarterLength)
        durations_by_bars.append(durations)
    return durations_by_bars

def load_abc_notations(abc_directory):
    for filename in os.listdir(abc_directory):
        filepath = os.path.join(abc_directory, filename)
        with open(filepath, 'r') as file:
            abc_notation = file.read()
        print(abc_notation)

if __name__=="__main__":
    load_abc_notations('./dataset')
    score = converter.parse(abc_notation, format='abc')
    durations_by_bars = extract_durations_by_bars(score)
    print(durations_by_bars)