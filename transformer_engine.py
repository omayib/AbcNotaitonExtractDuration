import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from sequences_from_abcnotations import duration_vocab

class MusicDataset(Dataset):
    def __init__(self, tokenized_sequences):
        self.tokenized_sequences = tokenized_sequences

    def __len__(self):
        return len(self.tokenized_sequences)

    def __getitem__(self, idx):
        notes, durations = self.tokenized_sequences[idx]
        return torch.tensor(notes, dtype=torch.long), torch.tensor(durations, dtype=torch.long)

class TransformerModel(nn.Module):
    def __init__(self, vocab_size_notes, vocab_size_durations, embed_size, num_heads, num_layers, ff_hidden_size):
        super(TransformerModel, self).__init__()
        self.embedding_notes = nn.Embedding(vocab_size_notes, embed_size)
        self.embedding_durations = nn.Embedding(vocab_size_durations, embed_size)
        self.positional_encoding = nn.Parameter(torch.zeros(1, 512, embed_size))
        self.transformer = nn.Transformer(embed_size, num_heads, num_layers, num_layers, ff_hidden_size)
        self.fc_notes = nn.Linear(embed_size, vocab_size_notes)
        self.fc_durations = nn.Linear(embed_size, vocab_size_durations)

    def forward(self, x_notes, x_durations):
        notes_embedding = self.embedding_notes(x_notes) + self.positional_encoding[:, :x_notes.size(1), :]
        durations_embedding = self.embedding_durations(x_durations) + self.positional_encoding[:, :x_durations.size(1), :]
        x = notes_embedding + durations_embedding
        x = self.transformer(x, x)
        notes_output = self.fc_notes(x)
        durations_output = self.fc_durations(x)
        return notes_output, durations_output

# Example parameters
vocab_size_notes = 128  # MIDI note range
vocab_size_durations = len(duration_vocab)  # Number of unique duration tokens
embed_size = 512
num_heads = 8
num_layers = 6
ff_hidden_size = 2048

# Initialize the model
model = TransformerModel(vocab_size_notes, vocab_size_durations, embed_size, num_heads, num_layers, ff_hidden_size)

# Example tokenized sequences (load from previous steps or data)
tokenized_sequences = [
    ([60, 62, 64, 65, 67], [1, 1, 2, 1, 1]),  # Example sequences
    ([67, 65, 64, 62, 60], [1, 1, 2, 1, 1])
]

# Create the dataset
dataset = MusicDataset(tokenized_sequences)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    epoch_loss = 0
    for batch in dataloader:
        notes, durations = batch
        optimizer.zero_grad()
        notes_output, durations_output = model(notes[:, :-1], durations[:, :-1])
        notes_loss = criterion(notes_output.reshape(-1, vocab_size_notes), notes[:, 1:].reshape(-1))
        durations_loss = criterion(durations_output.reshape(-1, vocab_size_durations), durations[:, 1:].reshape(-1))
        loss = notes_loss + durations_loss
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    print(f'Epoch {epoch+1}, Loss: {epoch_loss/len(dataloader)}')

# Save the trained model
torch.save(model.state_dict(), 'model/transformer_music_model.pth')


def generate_melody(model, start_sequence_notes, start_sequence_durations, max_length=100):
    model.eval()
    generated_notes = start_sequence_notes
    generated_durations = start_sequence_durations
    with torch.no_grad():
        for _ in range(max_length):
            input_notes = torch.tensor(generated_notes[-512:], dtype=torch.long).unsqueeze(0)
            input_durations = torch.tensor(generated_durations[-512:], dtype=torch.long).unsqueeze(0)
            notes_output, durations_output = model(input_notes, input_durations)
            next_note = notes_output.argmax(dim=-1).item()
            next_duration = durations_output.argmax(dim=-1).item()
            generated_notes.append(next_note)
            generated_durations.append(next_duration)
            if next_note == END_TOKEN or next_duration == END_TOKEN:  # Example end condition
                break
    return generated_notes, generated_durations

# Example start sequence
start_sequence_notes = [60, 62, 64]  # Example starting notes
start_sequence_durations = [ 1, 1, 2]  # Example starting durations

# Generate a new melody
new_notes, new_durations = generate_melody(model, start_sequence_notes, start_sequence_durations)
print(f"Generated Notes: {new_notes}")
print(f"Generated Durations: {new_durations}")