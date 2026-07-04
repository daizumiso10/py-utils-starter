# py-utils-starter

A tiny collection of Python string utility functions, built as a learning
project for practicing the GitHub pull request workflow.

## Installation

```bash
pip install -e .
```

## Usage

```python
from pyutils.strings import slugify, truncate, is_palindrome

slugify("Hello, World!")      # "hello-world"
truncate("Hello, World!", 5)  # "Hello..."
is_palindrome("racecar")      # True
```

## Running tests

```bash
pip install pytest
pytest
```

## License

MIT
