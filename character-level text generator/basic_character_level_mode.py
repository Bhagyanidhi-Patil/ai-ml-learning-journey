import torch
import torch.nn as nn
import torch.optim as optim

# sample training data
text = "hello world. this is a simple gen ai model.This model reads text, learns character transitions & predicts the next character"

# Create vocabulary
chars = sorted(list(set(text)))
vocab_size = len(chars)

# Create empty dictionaries
stoi = {}
itos = {}

# Loop through characters with index
for i, ch in enumerate(chars):
    stoi[ch] = i
    itos[i] = ch

# Encode text
# For each character c in text ,look up its number using stoi ,create a list of numbers 
# ,convert that list into a tensor and store it in data
data = torch.tensor([stoi[c] for c in text], dtype=torch.long)

# Hyperparameters
embedding_dim = 16
hidden_dim = 64


class SimpleGenAI(nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)  # creates embedding table for each char in (vocal size)
        self.rnn = nn.RNN(embedding_dim, hidden_dim, batch_first=True) # takes 16 size vector + prev memory as input and Produces new memory of size 64
        self.fc = nn.Linear(hidden_dim, vocab_size)    # creates linear layer by taking 64 size hidden layer as input of vocal size (vocal size say 30 then, 30*64 size hidden state)

    def forward(self, x, hidden):
        x = self.embedding(x)
        out, hidden = self.rnn(x, hidden)
        out = self.fc(out)
        return out, hidden

model = SimpleGenAI()
loss_fn = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training loop
for epoch in range(200): 
    hidden = None  #Start with no previous memory
    optimizer.zero_grad()  #Clear old learning signals
    
    inputs = data[:-1].unsqueeze(0)  #everything except the last item
    targets = data[1:].unsqueeze(0)  #everything except the first item
    
    outputs, hidden = model(inputs, hidden)  #In PyTorch, whenever you call model(...), it automatically calls the forward method of your nn.Module
    loss = loss_fn(outputs.squeeze(), targets.squeeze())  #Compare predictions with correct answers to see how wrong the model is.
    
    loss.backward()   #Figure out how to adjust the model to reduce the error.
    optimizer.step()  #Actually update the model weights (this is where learning happens).

    if epoch % 50 == 0:    #Every 50 steps, print the loss so you can see if the model is improving.
        print(f"Epoch {epoch}, Loss: {loss.item()}")

# Generate text
def generate(start="h", length=50):
    model.eval()   #Sets the model to evaluation mode (no learning, just prediction).
    input = torch.tensor([[stoi[start]]])    #Converts the starting character into a number and adds a batch dimension [[...]].
    hidden = None
    result = start
    
    for _ in range(length):
        output, hidden = model(input, hidden)   #Feed the current input into the model along with its memory.
        probs = torch.softmax(output[0, -1], dim=0)  #Convert raw scores into probabilities.
        char_id = torch.multinomial(probs, 1).item()   #Randomly pick a character according to the probabilities.
        result += itos[char_id]
        input = torch.tensor([[char_id]])   #The new character becomes the input for the next step.
    
    return result

print(generate("h"))


