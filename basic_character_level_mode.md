🤖 "Simple Character-Level Model Code "

This code implements a character-level text generator using a simple RNN.
It learns patterns in sequences of characters from a sample text.
After training, it can generate new text character by character that resembles the training text.

--------------------------------------------------------------------------------------------------------------------------
Torch (PyTorch) is a Python library used to build Artificial Intelligence and Deep Learning models.
It helps you to Create neural networks, Train models on data , do fast mathematical computations and Run models on GPU.

forward method is not automatically part of Python classes—it’s a method you define inside your subclass of nn.Module.
PyTorch expects every nn.Module subclass to have a forward method. It defines how input flows through the network.

--------------------------------------------------------------------------------------------------------------------------

🧠 What is an RNN?
RNN stands for: Recurrent Neural Network
It is a type of neural network made for sequence data like text , sentence, speech.
Why Normal Neural Networks Don’t Work Well for Text
A normal neural network: takes input ,produces output and forgets everything .But text is different. To predict the next word, the model must remember previous words.

Character IDs
      ↓
Embedding (16)
      ↓
RNN (64 memory)
      ↓
Linear layer
      ↓
Predicted next character probabilities

--------------------------------------------------------------------------------------------------------------------------

🪜 Step-by-Step Explanation:

1. First store sample training data.
2. Then create vocabulary
    This part is preparing the text so the computer can understand it.Computers do not understand letters , then only undertsand numbers. So, convert letters -> numbers. 
    
    chars = sorted(list(set(text)))
        set(text) → removes duplicate characters , list(...) → converts it to a list ,sorted(...) → sorts alphabetically
    vocab_size = len(chars)
        This just counts how many unique characters exist.
    stoi = {ch:i for i,ch in enumerate(chars)}
        stoi = "string to index" . This creates a dictionary that maps chars -> numbers like ['e' -> 0, 'h' -> 1 ] etc.,
    itos = "index to string"
        This is the reverse dictionary: numbers -> chars like [0 -> 'e' , 1 -> 'h'] etc
    Even big models from: OpenAI , Google DeepMind do the same concept — but instead of characters, they use tokens (words or subwords).

3. Next step is to encode the text
    data = torch.tensor([stoi[c] for c in text], dtype=torch.long)
        This line converts your text into numerical tensor format so the neural network can learn from it.
        torch.tensor(...) this converts list into a tensor using pytorch. Because neural networks work with tensors, not Python lists.
        dtype=torch.long is data type
        🔥 Why This Step Is Important
        Without this: Neural network cannot understand text ,No training can happen ,No predictions can be made .This is called encoding.

4. Define Hyperparameters
    Hyperparameters are values you choose before training the model.
    embedding_dim = 16 .This is the size of each character vector.
    Earlier we converted characters into numbers:
        h → 5
        e → 2
        l → 8

    But neural networks don’t use the raw number directly. Instead, they convert each number into a vector like this:
        h → [0.21, -0.45, 0.88, ..., 16 values]
    
    hidden_dim = 64 .This controls the size of the RNN’s hidden memory.
    So internally it looks like:
        hidden_state = [0.12, -0.77, 0.33, ..., 64 values]
    Each embedding vector (size 16) is directly fed as input to the RNN at every time step. And RNN creates hidden state of size 64.

5. Create class SimpleGenAI. 
    The embedding layer creates a vector of size 16 for each character in the vocabulary.
    The RNN takes these 16-size vectors along with the previous hidden state and produces a new hidden state of size 64.
    The linear layer converts the 64-size hidden state into scores for each character in the vocabulary (e.g., if the vocabulary has 30 characters, it produces 30 scores. The 30 scores are the output of the linear layer.).

    forward function is how data flows through the model when you give it input.

6.  nn.CrossEntropyLoss is a loss function used for classification tasks.
    It measures the difference between: The predicted probabilities from the model and the true class labels of the data .It outputs a single number (the loss), which tells the optimizer how wrong the model is.

    optimizer = optim.Adam(model.parameters(), lr=0.01)
    optim.Adam is an optimizer, which updates the model’s parameters to reduce the loss. model.parameters() tells the optimizer which parameters to update. lr=0.01 is the learning rate, controlling how big each update step is. “This helps the model learn.” It changes the model’s brain little by little to make better guesses.

7. Train the model
    This loop repeatedly: Feeds data to the model ,Measures how wrong it is , Adjusts the model & Prints progress.

8. Generate text / Predict output
