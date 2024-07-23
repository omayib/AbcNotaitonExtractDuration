import torch

class Trainer:
    def __init__(self, model, criterion, optimizer, dataloader, device, num_epochs=200, sequence_length=1):
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.dataloader = dataloader
        self.device = device
        self.num_epochs = num_epochs
        self.sequence_length = sequence_length

    def train(self):
        self.model.to(self.device)
        for epoch in range(self.num_epochs):
            print(f'epoch {epoch}')
            for inputs, targets in self.dataloader:
                inputs = inputs.view(inputs.shape[0], inputs.shape[1], 1).to(self.device)

                targets = targets.to(self.device)

                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch + 1}/{self.num_epochs}], Loss: {loss.item():.4f}')

# Example usage:
# Assuming `model`, `criterion`, `optimizer`, `dataloader`, and `device` are already defined
# trainer = Trainer(model, criterion, optimizer, dataloader, device)
# trainer.train()
