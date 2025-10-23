# Definition Chunker

A Python script that chunks text per definition and stores it in a vector database for easy retrieval and search.

## Features

- Automatically detects and chunks various definition formats
- Stores definitions in a persistent vector database (ChromaDB)
- Supports semantic search across stored definitions
- Command-line interface for easy terminal usage
- Multiple input methods (manual input, file input)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage - Manual Input

Run the script and input definitions directly:
```bash
python definition_chunker.py
```

Then enter your definitions in any of these supported formats:
- `Term: Definition`
- `**Term**: Definition`
- `Term - Definition`
- `1. Term: Definition`

Press `Ctrl+D` (Linux/Mac) or `Ctrl+Z` (Windows) when done.

### File Input

Process definitions from a file:
```bash
python definition_chunker.py --file example_definitions.txt
```

### Section-Based Chunking

For hierarchical content with main headings and sub-items, use section chunking:
```bash
python definition_chunker.py --file example_definitions.txt --sections
```

This will group related items under their main headings instead of treating each item as a separate definition.

### Search Definitions

Search for definitions using semantic search:
```bash
python definition_chunker.py --search "machine learning"
```

### List All Definitions

View all stored definitions:
```bash
python definition_chunker.py --list
```

### Delete Definitions

Delete definitions by term name:
```bash
python definition_chunker.py --delete-term "Machine Learning"
```

Delete a specific definition by ID (get ID from --list):
```bash
python definition_chunker.py --delete-id "uuid-here"
```

Delete all definitions from a specific source:
```bash
python definition_chunker.py --delete-source "file:example_definitions.txt"
```

Delete ALL definitions (with confirmation):
```bash
python definition_chunker.py --clear-all
```

### Custom Database Path

Use a custom database location:
```bash
python definition_chunker.py --db-path /path/to/custom/db --collection my_definitions
```

## Supported Definition Formats

The script automatically detects these formats:

1. **Colon format**: `Term: Definition`
2. **Bold format**: `**Term**: Definition`
3. **Dash format**: `Term - Definition`
4. **Numbered format**: `1. Term: Definition`

## Examples

### Example 1: Manual Input
```bash
python definition_chunker.py
```
Then input:
```
Machine Learning: A subset of AI that enables computers to learn from data.
Deep Learning: A technique using neural networks with multiple layers.
```

### Example 2: File Processing
```bash
python definition_chunker.py --file example_definitions.txt
```

### Example 3: Search
```bash
python definition_chunker.py --search "neural network"
```

## Database

The script uses ChromaDB as the vector database, which:
- Automatically handles text embeddings
- Provides semantic search capabilities
- Persists data locally
- Supports similarity scoring

The database is stored in the `./vector_db` directory by default.

## Command Line Options

- `--db-path`: Path to vector database (default: ./vector_db)
- `--collection`: Collection name (default: definitions)
- `--search`: Search for definitions
- `--list`: List all stored definitions (includes IDs for deletion)
- `--file`: Input file to process
- `--delete-term`: Delete definitions by term name
- `--delete-id`: Delete definition by specific ID
- `--delete-source`: Delete all definitions from a specific source
- `--clear-all`: Delete ALL definitions (requires confirmation)
- `--sections`: Chunk by sections instead of individual definitions
