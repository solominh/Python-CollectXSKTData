import inspect
import re
import textwrap

import bs4.element


def replace_code_lines(source, start_token, end_token,
                       replacement, escape_tokens=True):
    """Replace the source code between `start_token` and `end_token`
    in `source` with `replacement`. The `start_token` portion is included
    in the replaced code. If `escape_tokens` is True (default),
    escape the tokens to avoid them being treated as a regular expression."""

    if escape_tokens:
        start_token = re.escape(start_token)
        end_token = re.escape(end_token)

    def replace_with_indent(match):
        indent = match.group(1)
        return textwrap.indent(replacement, indent)

    return re.sub(r"^(\s+)({}[\s\S]+?)(?=^\1{})".format(start_token, end_token),
                  replace_with_indent, source, flags=re.MULTILINE)


# Get the source code of the Tag.select() method
src = textwrap.dedent(inspect.getsource(bs4.element.Tag.select))

# Replace the relevant part of the method
start_token = "if pseudo_type == 'nth-of-type':"
end_token = "else"
replacement = """\
if pseudo_type == 'nth-of-type':
    try:
        if pseudo_value in ("even", "odd"):
            pass
        else:
            pseudo_value = int(pseudo_value)
    except:
        raise NotImplementedError(
            'Only numeric values, "even" and "odd" are currently '
            'supported for the nth-of-type pseudo-class.')
    if isinstance(pseudo_value, int) and pseudo_value < 1:
        raise ValueError(
            'nth-of-type pseudo-class value must be at least 1.')
    class Counter(object):
        def __init__(self, destination):
            self.count = 0
            self.destination = destination

        def nth_child_of_type(self, tag):
            self.count += 1
            if pseudo_value == "even":
                return not bool(self.count % 2)
            elif pseudo_value == "odd":
                return bool(self.count % 2)
            elif self.count == self.destination:
                return True
            elif self.count > self.destination:
                # Stop the generator that's sending us
                # these things.
                raise StopIteration()
            return False
    checker = Counter(pseudo_value).nth_child_of_type
"""
new_src = replace_code_lines(src, start_token, end_token, replacement)

# Compile it and execute it in the target module's namespace
exec(new_src, bs4.element.__dict__)
# Monkey patch the target method
bs4.element.Tag.select = bs4.element.select
