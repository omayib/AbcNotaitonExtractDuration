from music21 import converter, note, chord
import os

class SemutPreprocessing:
    def __init__(self,dir):
        self.dir = dir

    def get_notes_from_abc(self):
        notes = []
        for filename in os.listdir(self.dir):
            filepath = os.path.join(self.dir, filename)
            with open(filepath,'r') as file:
                abc_notation = file.read()
            score = converter.parse(abc_notation, format='abc')
            notes_to_parse = score.flat.notes
            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(element.nameWithOctave)  # Use nameWithOctave to get 'A4', 'B4', etc.
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(n.nameWithOctave for n in element.notes))
        return notes



