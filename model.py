import torch
import torch.nn as nn

class ThreeLayerLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, dropout):
        super(ThreeLayerLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.relu = nn.ReLU(inplace=True)
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden_size, hidden_size)
        self.fc1_1 = nn.Linear(hidden_size, hidden_size//2)
        self.fc1_2 = nn.Linear(hidden_size//2, 1)
        self.fc2_1 = nn.Linear(hidden_size, hidden_size//2)
        self.fc2_2 = nn.Linear(hidden_size//2, 1)
        self.fc3_1 = nn.Linear(hidden_size, hidden_size//2)
        self.fc3_2 = nn.Linear(hidden_size//2, 2)
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        out, _ = self.lstm(x, (h0, c0))
        out = self.dropout(out)
        out = self.fc1(out[:, -1, :])
        out = self.relu(out)
        out1 = self.fc1_1(out)
        out1 = self.relu(out1)
        out1 = self.fc1_2(out1)
        out1 = self.relu(out1)
        out2 = self.fc2_1(out)
        out2 = self.relu(out2)
        out2 = self.fc2_2(out2)
        out2 = self.relu(out2)
        out3 = self.fc3_1(out)
        out3 = self.relu(out3)
        out3 = self.fc3_2(out3)
  
        return out1, out2, out3
    
