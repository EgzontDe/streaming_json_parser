# Streaming JSON Parser

A Python implementation of a streaming JSON parser that processes JSON data incrementally.

## Features

- Processes JSON data incrementally in chunks
- Returns the current state of the parsed JSON object at any point
- Handles partial string values while maintaining the JSON structure
- Efficient parsing with O(n) time complexity where n is the length of the input
- Supports a subset of JSON with string values and objects

## Setup

### Using Docker

```bash
# Build and run tests with Docker
docker build -t streaming-json-parser .
docker run streaming-json-parser

# Or use docker-compose
docker-compose up
```

### Using Conda

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate streaming_json_parser
```

### Using pip

```bash
# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```python
from streaming_json_parser import StreamingJsonParser

# Initialize the parser
parser = StreamingJsonParser()

# Consume chunks of JSON data
parser.consume('{"foo": "bar", ')
parser.consume('"baz": "qux"}')

# Get the current state of the parsed JSON
result = parser.get()
print(result)  # {'foo': 'bar', 'baz': 'qux'}

# Works with partial data too
parser = StreamingJsonParser()
parser.consume('{"user": "John", "country": "Switzerl')
print(parser.get())  # {'user': 'John', 'country': 'Switzerl'}
```

## API

### `StreamingJsonParser`

A class that implements the streaming JSON parser.

#### Methods

- `__init__()`: Initializes the parser with an empty state.
- `consume(buffer: str)`: Consumes a chunk of JSON data.
- `get()`: Returns the current state of the parsed JSON object as a Python dictionary.

## Limitations

- Supports only string values and objects (no arrays, numbers, booleans, or null)
- Does not handle escape sequences in strings
- Does not validate for duplicate keys in objects

## Testing

Run the included tests with:

```bash
# Using pytest
pytest -v

# Or simply
python test_streaming_json_parser.py

# Using Docker
docker-compose up
```