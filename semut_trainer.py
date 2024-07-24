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
            self.total_loss = 0.0
            self.total_accuracy = 0.0
            self.total_sample = 0

            self.model.train()
            for inputs, targets in self.dataloader:
                inputs = inputs.view(inputs.shape[0], inputs.shape[1], 1).to(self.device)
                targets = targets.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)
                loss.backward()
                self.optimizer.step()

                self.total_loss += loss.item() * targets.size(0)
                self.total_accuracy += self.calculate_accuracy(outputs, targets) * targets.size(0)
                self.total_sample += targets.size(0)

            avg_loss = self.total_loss / self.total_sample
            avg_accuracy = self.total_accuracy / self.total_sample

            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch + 1}/{self.num_epochs}], Loss: {avg_loss:.4f}, accuracy {avg_accuracy:.4f}')

    def calculate_accuracy(self, outputs, targets):
        _,predicted = torch.max(outputs,1)
        correct = (predicted==targets).sum().item()
        accuracy = correct / targets.size(0)
        return accuracy
# Example usage:
# Assuming `model`, `criterion`, `optimizer`, `dataloader`, and `device` are already defined
# trainer = Trainer(model, criterion, optimizer, dataloader, device)
# trainer.train()
