import torch

class semutEvaluation:
    def __init__(self, model, dataloader, criterion, device):
        self.model = model
        self.dataloader = dataloader
        self.criterion = criterion
        self.device = device
    def evaluate(self):
        self.model.eval()  # Set the model to evaluation mode
        total_loss = 0.0
        total_accuracy = 0.0
        total_samples = 0

        with torch.no_grad():  # Disable gradient calculation for evaluation
            for inputs, targets in self.dataloader:
                inputs = inputs.view(inputs.shape[0], inputs.shape[1], 1).to(self.device)
                targets = targets.to(self.device)

                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)

                total_loss += loss.item() * targets.size(0)
                total_accuracy += self.calculate_accuracy(outputs, targets) * targets.size(0)
                total_samples += targets.size(0)

        avg_loss = total_loss / total_samples
        avg_accuracy = total_accuracy / total_samples

        return avg_loss, avg_accuracy

    def calculate_accuracy(self, outputs, targets):
        _, predicted = torch.max(outputs, 1)
        correct = (predicted == targets).sum().item()
        accuracy = correct / targets.size(0)
        return accuracy