from pyutils.strings import slugify, truncate, is_palindrome


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_slugify_collapses_whitespace():
    assert slugify("  Multiple   spaces  ") == "multiple-spaces"


def test_truncate_shorter_than_length():
    assert truncate("Hello", 10) == "Hello"


def test_truncate_longer_than_length():
    assert truncate("Hello, World!", 5) == "Hello..."


def test_is_palindrome_true_for_simple_word():
    assert is_palindrome("racecar") is True


def test_is_palindrome_ignores_case_spaces_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") is True


def test_is_palindrome_false_for_non_palindrome():
    assert is_palindrome("hello") is False
