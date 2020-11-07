from math import ceil
import re
from textwrap import dedent
from io import StringIO

def normalize(fp):
    block = "normal"
    lines = list()
    for line in fp:
        ignore = False
        if block == "quoted code block":
            if line.strip().startswith("```"):
                block = "normal"
                ignore = True
            else:
                line = "    "+line
        elif block == "indent code block":
            pass
        else:
            if line.strip().startswith("#"):
                # title
                pass
            elif line.strip().startswith("```"):
                ignore = True
                block = "quoted code block"
            elif line.strip().startswith("> "):
                # reference
                pass
            elif re.search(r"^\s+\d+\.", line):
                # ol
                pass
            elif re.search(r"^\s+- ", line):
                # ul
                pass
            elif not line.strip():
                # empty line
                pass
            else:
                # normal line
                pass
            line = line.rstrip() + "  \n"
        if not ignore:
            lines.append(line)
    return "".join(lines)

def main():
    lines = """\
    # h1
    ```
    def function(args):
        code line1
        code line2
    ```
    1. ol
    2. ol
    """
    dedent(lines)
    print(normalize(StringIO(lines)))


if __name__ == "__main__":
    main()
