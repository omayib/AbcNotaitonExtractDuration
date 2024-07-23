import numpy as np
class NoteSequenceBuilder:
    def __init__(self, all_notes, sequence_length=100):
        self.all_notes = all_notes
        self.sequence_length = sequence_length
        self.flat_notes = [note for sublist in all_notes for note in sublist]
        self.unique_notes = sorted(set(self.flat_notes))
        self.note_to_int = {note: number for number, note in enumerate(self.unique_notes)}
        self.network_input = []
        self.network_output = []
        self.n_vocab = len(self.unique_notes)

    def create_sequences(self):
        for i in range(len(self.flat_notes) - self.sequence_length):
            sequence_in = self.flat_notes[i:i + self.sequence_length]
            sequence_out = self.flat_notes[i + self.sequence_length]
            self.network_input.append([self.note_to_int[char] for char in sequence_in])
            self.network_output.append(self.note_to_int[sequence_out])

        self.network_input = np.array(self.network_input)
        self.network_output = np.array(self.network_output)

        return self.network_input, self.network_output

    def get_note_to_int(self):
        return self.note_to_int

