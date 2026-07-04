# py-utils-starter

A tiny collection of Python string and image utility functions, built as a
learning project for practicing the GitHub pull request workflow.

## Installation

```bash
pip install -e .
```

The `image_to_3d` depth-estimation feature additionally needs `torch` and
`transformers`:

```bash
pip install -e ".[depth]"
```

## Usage

```python
from pyutils.strings import slugify, truncate, is_palindrome

slugify("Hello, World!")      # "hello-world"
truncate("Hello, World!", 5)  # "Hello..."
is_palindrome("racecar")      # True
```

```python
from pyutils.image3d import image_to_3d

# Estimates depth with an AI model (MiDaS) and writes a colored triangle
# mesh where each pixel becomes a vertex positioned by its depth.
image_to_3d("photo.jpg", "photo.obj")
```

## Running tests

```bash
pip install pytest
pytest
```

## License

MIT
