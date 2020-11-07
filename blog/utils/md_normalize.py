from math import ceil
import re
from textwrap import dedent
from io import StringIO

def normalize(fp):
    block = "new block"
    lines = list()
    for line in fp:
        ignore = False
        prepend = 0
        append = 0
        if block == "quoted code block":
            if line.strip().startswith("```"):
                block = "new block"
                append = 2
                ignore = True
            else:
                line = "    "+line
        elif block == "indent code block":
            pass
        else:
            block = "normal"
            if line.strip().startswith("#"):
                # title
                pass
            elif line.strip().startswith("```"):
                ignore = True
                if block == "one blank":
                    prepend = 1
                elif block == "new block":
                    prepend = 0
                else:
                    prepend = 2
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
                if block == "one blank":
                    block = "new block"
                elif block == "new block":
                    ignore = True
            else:
                # normal line
                pass
            line = line.rstrip() + "  \n"
        lines.append("  \n"*prepend)
        if not ignore:
            lines.append(line)
        lines.append("  \n"*append)
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
