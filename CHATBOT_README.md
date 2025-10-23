# Vector Database Chatbot

A simple terminal-based chatbot that answers questions using only the data stored in your vector database, powered by Cohere AI.

## Features

- 🤖 Natural language Q&A based on your vector database
- 📚 Only uses information from stored definitions
- 🔍 Shows source definitions and similarity scores
- 💬 Interactive chat mode or single question mode
- 🛡️ Safe responses - won't make up information not in database

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Chat Mode

Start a conversation with the chatbot:
```bash
python chatbot.py
```

Example conversation:
```
You: What is machine learning?
🤔 Searching database and thinking...

🤖 Bot: Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed.

📚 Sources from database:
   1. Machine Learning (similarity: 0.95)
```

### Single Question Mode

Ask one question and get an answer:
```bash
python chatbot.py --question "What is deep learning?"
```

### Custom Database Path

Use a different database location:
```bash
python chatbot.py --db-path /path/to/your/db --collection your_collection
```

### Custom API Key

Use a different Cohere API key:
```bash
python chatbot.py --api-key your_api_key_here
```

## Commands in Chat Mode

- Type your question normally
- Type `quit`, `exit`, `bye`, or `q` to end the chat
- Press `Ctrl+C` to force quit

## How It Works

1. **Question Input**: You ask a question in natural language
2. **Vector Search**: The system searches your vector database for relevant definitions
3. **Context Building**: Top matching definitions are gathered as context
4. **AI Response**: Cohere AI generates an answer using ONLY the database context
5. **Source Display**: Shows which definitions were used and their similarity scores

## Important Notes

- ⚠️ The chatbot will ONLY answer based on data in your vector database
- 📝 If no relevant information is found, it will tell you so
- 🚫 It won't make up or hallucinate information not in your database
- 🔍 Always shows sources so you can verify the information

## Example Questions

Based on the example definitions, you could ask:
- "What is machine learning?"
- "Tell me about neural networks"
- "How does deep learning work?"
- "What's the difference between AI and machine learning?"
- "Explain cloud computing"

## Troubleshooting

### No definitions found
```
⚠️ Warning: No definitions found in the vector database!
Please add some definitions first using definition_chunker.py
```
**Solution**: Add definitions to your database first using `definition_chunker.py`

### API Key Error
```
❌ Error initializing chatbot: Invalid API key
```
**Solution**: Check your Cohere API key is correct

### Database Connection Error
```
❌ Error initializing chatbot: Database not found
```
**Solution**: Make sure the database path exists and contains data

## Command Line Options

- `--api-key`: Cohere API key (default: provided key)
- `--db-path`: Path to vector database (default: ./vector_db)
- `--collection`: Collection name (default: definitions)
- `--question`: Ask a single question and exit
