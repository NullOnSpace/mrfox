from math import ceil
import re
from textwrap import dedent
from io import StringIO

def normalize(fp):
    block = "new block"
    parent_block = ""
    indent_level = 0
    last_indent_level = 0
    lines = list()
    for line in fp:
        ignore = False
        prepend = 0
        append = 0
        if line.strip():
            if block == "new block":
                last_indent_level = 0
            else:
                last_indent_level = indent_level
            indent_level = ceil((len(line)-len(line.lstrip())) / 4)
        if block == "quoted code block":
            if line.strip().startswith("```"):
                # close quoted code block
                if parent_block:
                    block = parent_block
                    append = 1
                else:
                    block = "new block"
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
                # start new quoted code block
                ignore = True
                if block == "one blank":
                    pass
                elif block == "new block":
                    prepend = 0
                elif block.endswith("list"):
                    prepend = 1
                    if indent_level > last_indent_level:
                        parent_block = block
                    else:
                        parent_block = ""
                else:
                    prepend = 2
                block = "quoted code block"
            elif line.strip().startswith("> "):
                # reference
                block = "reference"
            elif re.search(r"^\s*\d+\.", line):
                # ol
                if block != "new block" and not block.endswith("list"):
                    # last one line is not a list block
                    prepend = 1
                elif block.endswith("list"):
                    if indent_level > last_indent_level:
                        parent_block = block
                block = "ordered list"
            elif re.search(r"^\s*- ", line):
                # ul
                if block != "new block" and not block.endswith("list"):
                    prepend = 1
                elif block.endswith("list"):
                    if indent_level > last_indent_level:
                        parent_block = block
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
                if parent_block and indent_level > last_indent_level:
                    block = parent_block
                elif parent_block and indent_level == 0:
                    if block == "one blank":
                        prepend = 1
                    elif block != "new block":
                        prepend = 2
                    block = "normal"
                else:
                    block = "normal"
            line = line.rstrip()+"  \n"
        # debug only
        # line = line.rstrip()  + f"  # b:{block} pb:{parent_block} id:{indent_level}" + "  \n"

        lines.append("  \n"*prepend)
        if not ignore:
            lines.append(line)
        lines.append("  \n"*append)
    return "".join(lines)

def main():
    res = normalize(StringIO(lines))
    with open('test.md', 'w', encoding='utf8') as fp:
        fp.write(res)
    print(res)

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
mutex_instances.LOCKED_BY_THREAD_ID。步骤如下:
1.  假设线程1等待互斥锁。
2.  可以确认该线程在等待那个线程:
    ```
    SELECT * FROM events_waits_current WHERE THREAD_ID = <thread_1>;
    ```
    假设查询结果发现线程在等待锁A。
3.  可以确定哪个线程持有锁A:
    ```
    SELECT * FROM mutex_instances WHERE OBJECT_INSTANCE_BEGIN = <mutex_A>;
    ```
    假设发现了是线程2,这是在`mutex_instances.LOCKED_BY_THREAD_ID`中找到的。
"""


if __name__ == "__main__":
    main()
