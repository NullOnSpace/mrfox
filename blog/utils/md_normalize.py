from math import ceil
import re
from textwrap import dedent
from io import StringIO

def normalize(fp):
    block = "new block"
    parent_block = ""
    indent_level = 0
    lines = list()
    for line in fp:
        ignore = False
        prepend = 0
        append = 0
        last_indent_level = indent_level
        indent_level = ceil(len(line)-len(line.lstrip()) / 4)
        if block == "quoted code block":
            if line.strip().startswith("```"):
                block = "new block"
                if parent_block:
                    append = 1
                else:
                    append = 2
                ignore = True
            else:
                line = "    "+line
        elif block == "indent code block":
            pass
        else:
            if line.strip().startswith("#"):
                block = "new block"
                parent_block = ""
                append = 1
            elif line.strip().startswith("```"):
                ignore = True
                if block == "one blank":
                    prepend = 1
                elif block == "new block":
                    prepend = 0
                elif block.endswith("list"):
                    prepend = 1
                    parent_block = block
                else:
                    prepend = 2
                block = "quoted code block"
            elif line.strip().startswith("> "):
                # reference
                block = "reference"
            elif re.search(r"^\s+\d+\.", line):
                # ol
                if block != "new block" and not block.endswith("list"):
                    prepend = 1
                block = "ordered list"
            elif re.search(r"^\s+- ", line):
                # ul
                if block != "new block" and not block.endswith("list"):
                    prepend = 1
                block = "unordered list"
            elif not line.strip():
                if block == "one blank":
                    parent_block = ""
                    block = "new block"
                elif block == "new block":
                    parent_block = ""
                    ignore = True
                else:
                    parent_block = block
                    block = "one blank"
            else:
                # normal line
                block = "normal"
            line = line.rstrip() + "  \n"
        lines.append("  \n"*prepend)
        if not ignore:
            lines.append(line)
        lines.append("  \n"*append)
    return "".join(lines)

def main():
    lines = """\
    # h1
    -   this is a unordered
    -   this is another unordered
    ```
    def function(args):
        code line1
        code line2
    ```
    1.  ol
    2.  ol
    -   this is a level 1 ul
        -   this is level 2 ul for test bock
            ```
            def function():
                pass
            ```
    """
    dedent(lines)
    print(normalize(StringIO(lines)))


if __name__ == "__main__":
    main()
