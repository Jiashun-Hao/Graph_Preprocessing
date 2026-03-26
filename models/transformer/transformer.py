import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from transformers import BertModel, BertConfig, AdamW
import jsonlines
import matplotlib.pyplot as plt

class VectorDataset(Dataset):
    def __init__(self, jsonl_file):
        self.data = []
        with jsonlines.open(jsonl_file) as reader:
            for obj in reader:
                self.data.append((obj['func'], obj['target']))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        vec, label = self.data[idx]
        return torch.tensor(vec, dtype=torch.float), torch.tensor(label, dtype=torch.long)

dataset = VectorDataset('TEST_Emberding_code.jsonl')
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

config = BertConfig(
    vocab_size=2,
    hidden_size=100,
    num_hidden_layers=1,
    num_attention_heads=1,
    intermediate_size=128,
)

class CustomBertModel(nn.Module):
    def __init__(self, config):
        super(CustomBertModel, self).__init__()
        self.bert = BertModel(config)
        self.classifier = nn.Linear(config.hidden_size, 2)

    def forward(self, input_vec):
        outputs = self.bert(inputs_embeds=input_vec.unsqueeze(1))
        pooled_output = outputs.pooler_output
        return self.classifier(pooled_output)

model = CustomBertModel(config)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = AdamW(model.parameters(), lr=1e-5)
loss_fn = nn.CrossEntropyLoss()

# 用于记录损失的列表
loss_values = []

for epoch in range(100):  # 假设训练3个epoch
    model.train()
    total_loss = 0
    for batch in dataloader:
        inputs, labels = batch
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        loss = loss_fn(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader)
    loss_values.append(avg_loss)
    print(f"Epoch {epoch+1}, Loss: {avg_loss}")

# 绘制损失图
plt.plot(loss_values, label='Training Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Loss Over Time')
plt.legend()
plt.show()


#