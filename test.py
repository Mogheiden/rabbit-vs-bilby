import torch
import torch.utils.data.dataloader as dl
import torchvision.transforms.v2 as transforms
import torchvision

TESTING_DATA_DIR = './dataset/testing'

model = torch.jit.load('./model.pt')
preprocess = transforms.Compose([
    transforms.Resize([256, 256]),
    transforms.ToImage(),
    transforms.ToDtype(torch.float32, scale=True),
    transforms.Grayscale(3),
    transforms.RandomRotation(1),
    transforms.RandomHorizontalFlip(.35),
])

testing_dataset = torchvision.datasets.ImageFolder(TESTING_DATA_DIR, transform=preprocess)
testing_loader = dl.DataLoader(testing_dataset, shuffle=True, num_workers=0, batch_size=1, pin_memory=True)

if __name__ == '__main__':
  with torch.no_grad():
    device = torch.device("cuda" if torch.cuda.is_available else "cpu")
    model.train(False)
    correct = 0
    total = 0
    for (inputs, labels) in testing_loader:
      inputs, labels = inputs.to(device), labels.to(device)
      outputs = model(inputs)
      _, predicted = torch.max(outputs.data, 1)
      correct += (predicted == labels).sum().item()
      total += labels.size(0)
    acc = correct / total
    print("Accuracy: {}".format(acc))