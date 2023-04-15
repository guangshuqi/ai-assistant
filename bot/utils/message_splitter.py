import textwrap
MAX_MESSAGE_LENGTH = 2000
def split(message):
    wrapped_response = textwrap.wrap(message, width=MAX_MESSAGE_LENGTH, break_long_words=True, replace_whitespace=False)
    return wrapped_response