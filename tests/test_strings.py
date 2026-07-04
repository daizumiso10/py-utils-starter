from pyutils.strings import slugify, truncate


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_collapses_whitespace():
    assert slugify("  Multiple   spaces  ") == "multiple-spaces"


def test_truncate_shorter_than_length():
    assert truncate("Hello", 10) == "Hello"


def test_truncate_longer_than_length():
    assert truncate("Hello, World!", 5) == "Hello..."
