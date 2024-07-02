import os

from music21 import converter, note, stream, meter

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

def process_abc_notations(abc_directory, pattern3, pattern4):
    for filename in os.listdir(abc_directory):
        filepath = os.path.join(abc_directory, filename)
        with open(filepath, 'r') as file:
            abc_notation = file.read()
        score = converter.parse(abc_notation, format='abc')
        timesignature = extract_feature_timesignature(score)
        print(f"timesignature {filename} {timesignature}")
        if timesignature == '4/4' or timesignature == '2/4' or timesignature == '2/2':
            durations_by_bars = extract_durations_by_bars(score)
            pattern4.append(durations_by_bars)
        elif timesignature == '3/4' or timesignature == '6/8':
            durations_by_bars = extract_durations_by_bars(score)
            pattern3.append(durations_by_bars)


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

if __name__=="__main__":

    # initiate array for time signature 4/4
    patterns_duration_4 = []
    # initiate array for time signature 3/4
    patterns_duration_3 = []

    # pass both array for append inside loop
    process_abc_notations('./dataset', patterns_duration_3, patterns_duration_4)

    print(f"pattern 3/4 {patterns_duration_3}")
    print(f"pattern 4/4 {patterns_duration_4}")
