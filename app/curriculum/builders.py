"""Builders track - typically ages 13-15, assumes the Foundations basics."""
from __future__ import annotations

from .schema import Lesson, Track

LESSONS = [
    Lesson(
        slug="functions-that-work",
        title="Functions With Options",
        goal="Write flexible functions with several parameters and defaults.",
        minutes=14,
        xp=30,
        concept="""
<p>Parameters can have <strong>default values</strong>. If the caller does not
supply one, the default is used:</p>
<pre><code>def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"</code></pre>
<p><code>greet("Sam")</code> gives <code>"Hello, Sam!"</code> and
<code>greet("Sam", "Hi")</code> gives <code>"Hi, Sam!"</code>.</p>
<p>You can also pass arguments <strong>by name</strong>, which makes calls much
easier to read: <code>greet(name="Sam", greeting="Yo")</code>. Parameters with
defaults must come after the ones without.</p>
""",
        example=(
            'def power(base, exponent=2):\n    return base ** exponent\n\n'
            "print(power(5))\nprint(power(2, 10))\nprint(power(base=3, exponent=3))"
        ),
        brief=(
            "Write <code>join_words(words, separator=\", \")</code> that glues a list "
            "of words into one string using the separator. "
            "<code>join_words([\"a\", \"b\"])</code> gives <code>\"a, b\"</code>."
        ),
        starter='def join_words(words, separator=", "):\n    \n',
        solution='def join_words(words, separator=", "):\n    return separator.join(words)',
        checks=[
            {
                "kind": "call",
                "func": "join_words",
                "args": [["red", "green", "blue"]],
                "expect": "red, green, blue",
                "label": "Default separator",
            },
            {
                "kind": "call",
                "func": "join_words",
                "args": [["a", "b", "c"], " - "],
                "expect": "a - b - c",
                "label": "Custom separator",
            },
            {"kind": "call", "func": "join_words", "args": [[]], "expect": "", "label": "Empty list"},
            {"kind": "call", "func": "join_words", "args": [["solo"]], "expect": "solo", "label": "One word"},
        ],
        hints=[
            "Strings have a .join() method that does exactly this.",
            "The separator is the string you call .join() on.",
            'return separator.join(words)',
        ],
    ),
    Lesson(
        slug="list-power",
        title="Slicing and Sorting",
        goal="Cut lists into pieces and put them in order.",
        minutes=14,
        xp=30,
        concept="""
<p>A <strong>slice</strong> takes part of a list with
<code>items[start:stop]</code>. As always, <code>stop</code> is not included.
Leave a side blank to mean "all the way": <code>items[:3]</code> is the first
three, <code>items[-2:]</code> is the last two.</p>
<p><code>sorted(items)</code> gives back a <em>new</em> sorted list.
<code>items.sort()</code> reorders the list in place and returns
<code>None</code> - a classic trap. Add <code>reverse=True</code> for
descending order.</p>
""",
        example=(
            "scores = [50, 90, 70, 20]\n\nprint(scores[:2])\nprint(scores[-1:])\n"
            "print(sorted(scores))\nprint(sorted(scores, reverse=True))"
        ),
        brief=(
            "Write <code>top_three(scores)</code> returning the three highest scores, "
            "biggest first. If there are fewer than three, return all of them in order."
        ),
        starter="def top_three(scores):\n    \n",
        solution="def top_three(scores):\n    return sorted(scores, reverse=True)[:3]",
        checks=[
            {
                "kind": "call",
                "func": "top_three",
                "args": [[10, 90, 50, 70, 30]],
                "expect": [90, 70, 50],
                "label": "Picks the top three",
            },
            {"kind": "call", "func": "top_three", "args": [[5, 1]], "expect": [5, 1], "label": "Short list"},
            {"kind": "call", "func": "top_three", "args": [[]], "expect": [], "label": "Empty list"},
            {
                "kind": "call",
                "func": "top_three",
                "args": [[4, 4, 4, 4]],
                "expect": [4, 4, 4],
                "label": "Handles duplicates",
            },
        ],
        hints=[
            "sorted() with reverse=True puts the biggest first.",
            "Then take a slice of the first three.",
            "A slice of [:3] on a short list just gives what exists - no error.",
        ],
    ),
    Lesson(
        slug="dictionaries",
        title="Look It Up",
        goal="Store labelled data in dictionaries.",
        minutes=16,
        xp=35,
        concept="""
<p>A list finds things by position. A <strong>dictionary</strong> finds them by
<strong>key</strong> - much better when the data has names.</p>
<pre><code>player = {"name": "Nova", "score": 42}
print(player["name"])</code></pre>
<p>Asking for a key that is not there raises a <code>KeyError</code>. Avoid that
with <code>player.get("lives", 3)</code>, which returns <code>3</code> when the
key is missing.</p>
<p>Loop over a dictionary with <code>for key, value in data.items():</code>, or
use <code>.keys()</code> and <code>.values()</code> on their own.</p>
""",
        example=(
            'stock = {"apples": 5, "pears": 0}\n\nstock["plums"] = 12\n\n'
            "for name, count in stock.items():\n"
            '    print(f"{name}: {count}")\n\nprint(stock.get("kiwis", 0))'
        ),
        brief=(
            "Write <code>count_letters(word)</code> returning a dictionary of how many "
            "times each letter appears. <code>count_letters(\"bee\")</code> gives "
            "<code>{\"b\": 1, \"e\": 2}</code>."
        ),
        starter="def count_letters(word):\n    counts = {}\n    \n    return counts\n",
        solution=(
            "def count_letters(word):\n"
            "    counts = {}\n"
            "    for letter in word:\n"
            "        counts[letter] = counts.get(letter, 0) + 1\n"
            "    return counts\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "count_letters",
                "args": ["bee"],
                "expect": {"b": 1, "e": 2},
                "label": "Counts 'bee'",
            },
            {
                "kind": "call",
                "func": "count_letters",
                "args": ["aaa"],
                "expect": {"a": 3},
                "label": "Counts repeats",
            },
            {"kind": "call", "func": "count_letters", "args": [""], "expect": {}, "label": "Empty word"},
            {
                "kind": "call",
                "func": "count_letters",
                "args": ["abc"],
                "expect": {"a": 1, "b": 1, "c": 1},
                "label": "All different",
            },
        ],
        hints=[
            "You can loop straight over a string: for letter in word.",
            "counts.get(letter, 0) gives 0 the first time you see a letter.",
            "counts[letter] = counts.get(letter, 0) + 1",
        ],
    ),
    Lesson(
        slug="string-toolkit",
        title="The String Toolkit",
        goal="Clean up and take apart messy text.",
        minutes=14,
        xp=30,
        concept="""
<p>Real text is messy. These methods tidy it:</p>
<ul>
  <li><code>text.strip()</code> - remove spaces from both ends</li>
  <li><code>text.split(",")</code> - break into a list at each comma
      (no argument splits on spaces)</li>
  <li><code>"-".join(items)</code> - the opposite of split</li>
  <li><code>text.replace("a", "b")</code> - swap one bit for another</li>
  <li><code>text.lower()</code> - level the playing field before comparing</li>
</ul>
<p>Strings are <strong>immutable</strong>: these methods never change the
original, they hand you a new string. You have to store the result.</p>
""",
        example=(
            'raw = "  Ada, Grace , Alan  "\n\nnames = raw.split(",")\n'
            "clean = [name.strip() for name in names]\nprint(clean)\n"
            'print(" & ".join(clean))'
        ),
        brief=(
            "Write <code>initials(full_name)</code> returning the capital initials of "
            "each word, separated by dots. <code>initials(\"ada lovelace\")</code> gives "
            "<code>\"A.L\"</code>. Extra spaces should not break it."
        ),
        starter="def initials(full_name):\n    \n",
        solution=(
            "def initials(full_name):\n"
            "    parts = full_name.split()\n"
            '    return ".".join(part[0].upper() for part in parts)\n'
        ),
        checks=[
            {
                "kind": "call",
                "func": "initials",
                "args": ["ada lovelace"],
                "expect": "A.L",
                "label": "Two names",
            },
            {
                "kind": "call",
                "func": "initials",
                "args": ["  grace   brewster   hopper  "],
                "expect": "G.B.H",
                "label": "Ignores extra spaces",
            },
            {"kind": "call", "func": "initials", "args": ["Alan"], "expect": "A", "label": "One name"},
            {"kind": "call", "func": "initials", "args": [""], "expect": "", "label": "Empty name"},
        ],
        hints=[
            "split() with no arguments handles runs of spaces for you.",
            "part[0] is the first character of a word.",
            'Build a list of upper-case initials, then ".".join() them.',
        ],
    ),
    Lesson(
        slug="nested-loops",
        title="Loops Inside Loops",
        goal="Work with grids and combinations.",
        minutes=16,
        xp=35,
        concept="""
<p>Put a loop inside another loop and the inner one runs completely for every
single step of the outer one. Two loops of 10 means 100 rounds - which is how you
walk a grid, build a times table, or compare every pair in a list.</p>
<p>Watch the indentation. Code indented once belongs to the outer loop; code
indented twice belongs to the inner one. Getting that wrong is the most common
bug in nested loops.</p>
""",
        example=(
            "for row in range(1, 4):\n"
            "    line = []\n"
            "    for col in range(1, 4):\n"
            "        line.append(row * col)\n"
            "    print(line)"
        ),
        brief=(
            "Write <code>grid(rows, cols)</code> returning a list of lists where each "
            "value is <code>row * col</code> using 1-based numbering. "
            "<code>grid(2, 3)</code> gives <code>[[1, 2, 3], [2, 4, 6]]</code>."
        ),
        starter="def grid(rows, cols):\n    table = []\n    \n    return table\n",
        solution=(
            "def grid(rows, cols):\n"
            "    table = []\n"
            "    for row in range(1, rows + 1):\n"
            "        line = []\n"
            "        for col in range(1, cols + 1):\n"
            "            line.append(row * col)\n"
            "        table.append(line)\n"
            "    return table\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "grid",
                "args": [2, 3],
                "expect": [[1, 2, 3], [2, 4, 6]],
                "label": "grid(2, 3)",
            },
            {"kind": "call", "func": "grid", "args": [1, 1], "expect": [[1]], "label": "grid(1, 1)"},
            {"kind": "call", "func": "grid", "args": [0, 5], "expect": [], "label": "No rows"},
            {
                "kind": "call",
                "func": "grid",
                "args": [3, 1],
                "expect": [[1], [2], [3]],
                "label": "Single column",
            },
        ],
        hints=[
            "Start a fresh inner list at the top of each outer loop.",
            "Append to the inner list inside the inner loop.",
            "Append the finished inner list to table after the inner loop ends.",
        ],
    ),
    Lesson(
        slug="handling-errors",
        title="When Things Go Wrong",
        goal="Catch errors instead of crashing.",
        minutes=14,
        xp=35,
        concept="""
<p>Some failures are not your fault - a user types "banana" when you wanted a
number. Rather than crashing, wrap the risky line in <code>try</code> and deal
with the failure in <code>except</code>:</p>
<pre><code>try:
    value = int(text)
except ValueError:
    value = 0</code></pre>
<p>Always name the specific error you expect. A bare <code>except:</code> swallows
every problem including your own typos, which makes bugs very hard to find.</p>
""",
        example=(
            'for text in ["12", "banana", "7"]:\n'
            "    try:\n"
            "        print(int(text) * 2)\n"
            "    except ValueError:\n"
            '        print("not a number")'
        ),
        brief=(
            "Write <code>safe_divide(a, b)</code> returning <code>a / b</code>, but "
            "returning <code>None</code> if <code>b</code> is zero. Use try/except, "
            "not an if."
        ),
        starter="def safe_divide(a, b):\n    \n",
        solution=(
            "def safe_divide(a, b):\n"
            "    try:\n"
            "        return a / b\n"
            "    except ZeroDivisionError:\n"
            "        return None\n"
        ),
        checks=[
            {"kind": "call", "func": "safe_divide", "args": [10, 2], "expect": 5.0, "label": "10 / 2"},
            {"kind": "call", "func": "safe_divide", "args": [7, 0], "expect": None, "label": "Divide by zero"},
            {"kind": "call", "func": "safe_divide", "args": [0, 5], "expect": 0.0, "label": "0 / 5"},
            {
                "kind": "source",
                "must_contain": [r"\btry\b", r"\bexcept\b"],
                "describe": "Uses try and except",
                "label": "Uses try/except",
            },
        ],
        hints=[
            "Dividing by zero raises ZeroDivisionError.",
            "Put the division inside try, and return None inside except.",
            "except ZeroDivisionError: return None",
        ],
    ),
    Lesson(
        slug="modules",
        title="Borrowing Other People's Code",
        goal="Use the standard library instead of reinventing it.",
        minutes=12,
        xp=30,
        concept="""
<p>Python ships with hundreds of ready-made tools grouped into
<strong>modules</strong>. <code>import</code> brings one in:</p>
<pre><code>import math
print(math.sqrt(16))

import random
print(random.randint(1, 6))</code></pre>
<p>Handy ones: <code>math.sqrt</code>, <code>math.floor</code>,
<code>math.pi</code>, <code>random.randint(a, b)</code> (both ends included),
<code>random.choice(items)</code>, <code>random.shuffle(items)</code>.</p>
<p>Because random results change every run, tests usually check that an answer is
<em>in the right range</em> rather than exactly equal to something.</p>
""",
        example=(
            "import math\nimport random\n\n"
            "print(math.sqrt(81))\nprint(math.floor(3.9))\n\n"
            'roll = random.randint(1, 6)\nprint(1 <= roll <= 6)'
        ),
        brief=(
            "Write <code>roll_dice(sides, count)</code> returning a list of "
            "<code>count</code> random rolls, each between 1 and <code>sides</code> "
            "inclusive. Use <code>random</code>."
        ),
        starter="import random\n\n\ndef roll_dice(sides, count):\n    \n",
        solution=(
            "import random\n\n\n"
            "def roll_dice(sides, count):\n"
            "    return [random.randint(1, sides) for _ in range(count)]\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "roll_dice",
                "args": [6, 0],
                "expect": [],
                "label": "Zero rolls gives an empty list",
            },
            {
                "kind": "call",
                "func": "roll_dice",
                "args": [1, 4],
                "expect": [1, 1, 1, 1],
                "label": "A one-sided die always rolls 1",
            },
            {
                "kind": "source",
                "must_contain": [r"import\s+random", r"random\.\w+"],
                "describe": "Imports and uses the random module",
                "label": "Uses the random module",
            },
        ],
        hints=[
            "random.randint(1, sides) gives one roll.",
            "Repeat it count times with a loop or a comprehension.",
            "[random.randint(1, sides) for _ in range(count)]",
        ],
    ),
    Lesson(
        slug="comprehensions",
        title="Building Lists in One Line",
        goal="Transform and filter lists compactly.",
        minutes=14,
        xp=35,
        concept="""
<p>This pattern comes up constantly: make an empty list, loop, append. A
<strong>list comprehension</strong> says the same thing in one line.</p>
<pre><code>squares = [n * n for n in range(5)]</code></pre>
<p>Add an <code>if</code> on the end to keep only some items:</p>
<pre><code>evens = [n for n in numbers if n % 2 == 0]</code></pre>
<p>Read it as: <em>the thing I want</em>, <em>for each item</em>, <em>if this is
true</em>. Keep them to one line of real work - if it needs a comment, use a
normal loop instead.</p>
""",
        example=(
            "numbers = [1, 2, 3, 4, 5, 6]\n\n"
            "doubled = [n * 2 for n in numbers]\n"
            "evens = [n for n in numbers if n % 2 == 0]\n\n"
            "print(doubled)\nprint(evens)"
        ),
        brief=(
            "Write <code>long_words(words, least)</code> returning the words with at "
            "least <code>least</code> characters, upper-cased. Use a comprehension."
        ),
        starter="def long_words(words, least):\n    \n",
        solution=(
            "def long_words(words, least):\n"
            "    return [word.upper() for word in words if len(word) >= least]\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "long_words",
                "args": [["cat", "horse", "ox", "zebra"], 4],
                "expect": ["HORSE", "ZEBRA"],
                "label": "Filters and upper-cases",
            },
            {
                "kind": "call",
                "func": "long_words",
                "args": [["a", "bb"], 5],
                "expect": [],
                "label": "Nothing long enough",
            },
            {
                "kind": "call",
                "func": "long_words",
                "args": [["four"], 4],
                "expect": ["FOUR"],
                "label": "Exactly the limit counts",
            },
            {
                "kind": "source",
                "must_contain": [r"\[[^\]]*\bfor\b[^\]]*\]"],
                "describe": "Uses a list comprehension",
                "label": "Uses a comprehension",
            },
        ],
        hints=[
            "The shape is [ WHAT for ITEM in LIST if CONDITION ].",
            "WHAT is word.upper() and the condition is len(word) >= least.",
            "[word.upper() for word in words if len(word) >= least]",
        ],
    ),
    Lesson(
        slug="inventory-project",
        title="Project: Shop Inventory",
        goal="Combine dictionaries, loops and conditions in one program.",
        minutes=22,
        xp=55,
        concept="""
<p>Real programs mostly move data between shapes. Here you will take a list of
sales and fold it into a summary.</p>
<p>The pattern - start with an empty accumulator, walk the data, update the
accumulator, return it - is one you will use for years. It is the same shape as
the letter counter, just with more interesting data.</p>
""",
        example=(
            'sales = [("pen", 2), ("book", 1), ("pen", 3)]\n\n'
            "totals = {}\nfor item, qty in sales:\n"
            "    totals[item] = totals.get(item, 0) + qty\n\nprint(totals)"
        ),
        brief=(
            "Write <code>restock(stock, minimum)</code>. <code>stock</code> is a "
            "dictionary of item to quantity. Return a sorted list of the item names "
            "whose quantity is below <code>minimum</code>."
        ),
        starter="def restock(stock, minimum):\n    \n",
        solution=(
            "def restock(stock, minimum):\n"
            "    low = [name for name, qty in stock.items() if qty < minimum]\n"
            "    return sorted(low)\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "restock",
                "args": [{"pens": 2, "books": 10, "bags": 0}, 5],
                "expect": ["bags", "pens"],
                "label": "Finds low stock, sorted",
            },
            {
                "kind": "call",
                "func": "restock",
                "args": [{"pens": 9, "books": 10}, 5],
                "expect": [],
                "label": "Nothing needs restocking",
            },
            {
                "kind": "call",
                "func": "restock",
                "args": [{"pens": 5}, 5],
                "expect": [],
                "label": "Exactly the minimum is fine",
            },
            {"kind": "call", "func": "restock", "args": [{}, 3], "expect": [], "label": "Empty stock"},
        ],
        hints=[
            "Loop with for name, qty in stock.items().",
            "Keep the names where qty < minimum - note it is 'below', not 'at or below'.",
            "Wrap the result in sorted() before returning it.",
        ],
    ),
]

TRACK = Track(
    slug="builders",
    title="Builders",
    tagline="Turn the basics into real programs.",
    ages="Ages 13-15",
    emoji="\N{HAMMER AND WRENCH}",
    blurb=(
        "Dictionaries, slicing, nested loops, error handling, modules and "
        "comprehensions - the toolkit that turns exercises into working software."
    ),
    lessons=LESSONS,
)
