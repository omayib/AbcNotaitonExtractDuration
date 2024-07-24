from semut_preprocessing import SemutPreprocessing
from semut_sequence_builder import NoteSequenceBuilder
from semut_dataset import MusicDataset
from torch.utils.data import Dataset, DataLoader
from semut_trainer import Trainer
from semut_lstm_model import SemutLSTMModel
from semut_evaluation import semutEvaluation

import torch
import torch.nn as nn
import random


dir_path = 'dataset'

pre = SemutPreprocessing(dir_path)
notes = pre.get_notes_from_abc()
print(f'pitchnames {notes}')


unique_notes = sorted(set(notes))
print(f'unique_notes {unique_notes}')
pitchnames = sorted(set(item for item in unique_notes))
print(f'pitchnames {pitchnames}')
n_vocab = len(unique_notes)

print(f'notes {notes}')

notes_squence_builder = NoteSequenceBuilder(notes)
network_input, network_output = notes_squence_builder.create_sequences()

print(f'network input {network_input.shape}')
print(f'network output {network_output.shape}')

dataset = MusicDataset(network_input, network_output)
dataloader = DataLoader(dataset, batch_size=64, shuffle=True)

print(f'data loader shape {dataloader}')

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f'device {device}')
model = SemutLSTMModel(input_size=1, hidden_size=256,output_size=n_vocab).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

#train
trainer = Trainer(model, criterion, optimizer, dataloader, device, num_epochs=100)
trainer.train()

semutEval = semutEvaluation(model, dataloader, criterion, device)
avg_loss, avg_accuracy = semutEval.evaluate()

print(f'avg loss {avg_loss}, avg_accuracy {avg_accuracy}')
# Save the trained model
torch.save(model.state_dict(), 'model/lstm_music_model.pth')

int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

def generate_music(model, start_pattern, num_notes):
    model.eval()
    generated = []
    pattern = start_pattern

    with torch.no_grad():
        for _ in range(num_notes):
            input_sequence = torch.tensor(pattern, dtype=torch.float32).view(1, -1, 1).to(device)
            output = model(input_sequence)
            predicted_note = torch.argmax(output).item()
            generated.append(predicted_note)
            pattern.append(predicted_note)
            pattern = pattern[1:]

    return generated


start = random.randint(0, len(network_input) - 1)
start_pattern = network_input[start].tolist()
generated_notes = generate_music(model, start_pattern, 500)

# Convert the generated notes to ABC notation
generated_abc = []
for note_idx in generated_notes:
    generated_abc.append(int_to_note[note_idx])

# Save generated notes to an ABC file
with open('output/generated_music.abc', 'w') as f:
    f.write("X: 1\nT: Generated Music\nM: 4/4\nK: C\n")
    f.write(' '.join(generated_abc))





