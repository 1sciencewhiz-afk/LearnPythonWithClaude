"""Builders track - typically ages 13-15, assumes the Foundations basics."""
from __future__ import annotations

from .schema import GlossaryTerm, Lesson, Track

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
<p>You can also pass arguments <strong>by name</strong>, known as <strong>keyword
arguments</strong>, which makes calls much easier to read:
<code>greet(name="Sam", greeting="Yo")</code>. Order stops mattering once you
name them, which is handy for a function with several optional settings.
Parameters with defaults must come after the ones without, since Python reads
the parameter list left to right and cannot allow a required value to appear
after an optional one.</p>
<h4>Why this matters</h4>
<p>Defaults let a function cover the common case with a short call, while still
allowing a caller to override any detail when they need to. Most real APIs -
including ones you will meet in Python's own standard library - lean heavily on
this pattern, offering sensible defaults for almost everything.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Putting a parameter without a default after one that has one, e.g.
      <code>def f(a="x", b):</code> - Python refuses to even run the file.</li>
  <li>Using a mutable value like <code>[]</code> or <code>{}</code> as a
      default - it is created once, not fresh on every call, so surprising bugs
      appear if the function ever modifies it. This is a well-known Python trap
      you will meet again later.</li>
  <li>Forgetting that keyword arguments must come after positional ones in a
      call, e.g. <code>greet(greeting="Hi", "Sam")</code> is invalid.</li>
</ul>
<h4>Try it yourself</h4>
<p>Call <code>join_words</code> with the separator passed by name:
<code>join_words(words=["a", "b"], separator=" + ")</code>. Then add a second
default parameter of your own to a function and check what order Python
requires it in.</p>
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
        glossary=[
            GlossaryTerm(
                "default value",
                "A value a parameter uses automatically when the caller does not "
                "supply one, written as name=value in the function definition.",
            ),
            GlossaryTerm(
                "keyword argument",
                "An argument passed by writing the parameter's name in the call, "
                "e.g. greet(name=\"Sam\"), so order no longer matters for it.",
            ),
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
three, <code>items[-2:]</code> is the last two. You can add a third number, the
step - <code>items[::2]</code> takes every second item, and <code>items[::-1]</code>
reverses the whole list.</p>
<p><code>sorted(items)</code> gives back a <em>new</em> sorted list, leaving the
original untouched. <code>items.sort()</code> reorders the list in place and
returns <code>None</code> - a classic trap: if you write
<code>items = items.sort()</code>, <code>items</code> is now <code>None</code>,
not the sorted list. Add <code>reverse=True</code> to either one for descending
order.</p>
<h4>Why this matters</h4>
<p>Slicing and sorting are how you turn raw data into something presentable: the
top three scores on a leaderboard, the last five messages in a chat, a list of
names in alphabetical order. They come up in almost every program that deals
with more than one piece of data.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Assuming <code>items[2:5]</code> includes index 5 - it stops just before
      it, giving you indexes 2, 3 and 4.</li>
  <li>Assigning the result of <code>.sort()</code> to a variable, losing the
      list entirely because <code>.sort()</code> returns <code>None</code>.</li>
  <li>Forgetting a slice beyond the end of a list does not crash - Python just
      gives you whatever exists, which is convenient but can hide a mistake.</li>
</ul>
<h4>Try it yourself</h4>
<p>Try <code>scores[::-1]</code> to reverse a list without calling
<code>sorted()</code> at all. Then try <code>print(scores.sort())</code> on its
own line and see the <code>None</code> it prints - a reminder of exactly the
trap described above.</p>
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
        glossary=[
            GlossaryTerm(
                "slice",
                "A piece of a list (or string) taken with items[start:stop], where "
                "stop is not included in the result.",
            ),
            GlossaryTerm(
                "sorted()",
                "Returns a new list with the items in order, leaving the original "
                "list unchanged. Add reverse=True for descending order.",
            ),
        ],
    ),
    Lesson(
        slug="sets",
        title="No Duplicates Allowed",
        goal="Use a set to work with unique values and compare groups of them.",
        minutes=12,
        xp=30,
        concept="""
<p>A <strong>set</strong> is a collection like a list, but it never keeps
duplicates and does not remember order. Build one with <code>set(...)</code>,
and Python throws away repeats automatically.</p>
<p>Sets are brilliant for two jobs: removing duplicates, and comparing groups
with <code>&amp;</code> (items in <strong>both</strong> - the intersection),
<code>|</code> (items in <strong>either</strong> - the union), and
<code>-</code> (items in the first set but not the second - the difference).
Checking whether something is in a set with <code>in</code> is also much
faster than checking a list, once the collection gets large, because Python
does not have to look through every item one by one.</p>
<h4>Why this matters</h4>
<p>"Have I seen this before?" and "what do these two groups have in common?"
are extremely common questions in real programs - deduplicating a list of
email addresses, finding mutual friends, checking which items are in stock
in two different warehouses. Sets answer both directly, in one expression.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Expecting a set to remember the order items were added - it does not,
      so printing one can show items in a different order than you typed them.</li>
  <li>Writing <code>{}</code> for an empty set - that actually makes an empty
      dictionary. An empty set needs <code>set()</code>.</li>
  <li>Trying to put a list inside a set - sets can only hold values that do not
      change, so a list (which can) is not allowed, but a tuple is.</li>
</ul>
<h4>Try it yourself</h4>
<p>Type <code>{1, 2, 2, 3}</code> straight into <code>print()</code> and watch
the duplicate vanish immediately. Then try <code>set_a - set_b</code> (the
difference) instead of <code>&amp;</code>, and compare it with
<code>set_b - set_a</code> - the two are not the same.</p>
""",
        example=(
            'seen = ["red", "blue", "red", "green", "blue"]\n'
            "unique = set(seen)\nprint(sorted(unique))\n\n"
            'morning = {"Ana", "Ben", "Cleo"}\n'
            'afternoon = {"Ben", "Cleo", "Dae"}\n'
            "print(sorted(morning & afternoon))"
        ),
        brief=(
            "Write <code>shared_fans(list_a, list_b)</code> returning a sorted list of "
            "names that appear in <strong>both</strong> lists, with no duplicates, using sets."
        ),
        starter="def shared_fans(list_a, list_b):\n    \n",
        solution="def shared_fans(list_a, list_b):\n    return sorted(set(list_a) & set(list_b))\n",
        checks=[
            {
                "kind": "call",
                "func": "shared_fans",
                "args": [["Ana", "Ben", "Cleo"], ["Ben", "Cleo", "Dae"]],
                "expect": ["Ben", "Cleo"],
                "label": "Finds the shared names",
            },
            {
                "kind": "call",
                "func": "shared_fans",
                "args": [["Ana", "Ana", "Ben"], ["Ana"]],
                "expect": ["Ana"],
                "label": "Removes duplicates from the result",
            },
            {"kind": "call", "func": "shared_fans", "args": [[], ["Ana"]], "expect": [], "label": "Nothing shared"},
            {
                "kind": "call",
                "func": "shared_fans",
                "args": [["Zoe", "Amy"], ["Amy", "Zoe"]],
                "expect": ["Amy", "Zoe"],
                "label": "Result comes back sorted",
            },
            {
                "kind": "source",
                "must_contain": [r"set\("],
                "describe": "Uses set() to find the overlap",
                "label": "Uses a set",
            },
        ],
        hints=[
            "Turn each list into a set with set(list_a) and set(list_b).",
            "& between two sets gives the items that are in both.",
            "sorted(set(list_a) & set(list_b))",
        ],
        glossary=[
            GlossaryTerm(
                "set",
                "An unordered collection of unique values, built with set(...) or "
                "curly braces, that automatically drops duplicates.",
            ),
            GlossaryTerm(
                "intersection (&)",
                "The items that appear in both of two sets, found with the & "
                "operator.",
            ),
            GlossaryTerm(
                "union (|)",
                "The items that appear in either of two sets, found with the | "
                "operator.",
            ),
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
<strong>key</strong> - much better when the data has names. Each entry is a
<code>key: value</code> pair, and a dictionary can hold as many as you like.</p>
<pre><code>player = {"name": "Nova", "score": 42}
print(player["name"])</code></pre>
<p>Asking for a key that is not there raises a <code>KeyError</code>. Avoid that
with <code>player.get("lives", 3)</code>, which returns <code>3</code> when the
key is missing instead of crashing - this is the safe way to look something up
when you are not sure it exists.</p>
<p>Loop over a dictionary with <code>for key, value in data.items():</code>, or
use <code>.keys()</code> and <code>.values()</code> on their own when you only
need one side.</p>
<h4>Why this matters</h4>
<p>Dictionaries are how you model a "record" - a player with a name and a score,
a product with a price and a stock count, a user with a username and an email.
Almost any real-world entity with several named properties becomes a dictionary
(or, later, an object) in code.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Using square brackets, <code>player["lives"]</code>, on a key that might
      not exist - use <code>.get()</code> with a default instead when you are
      not certain.</li>
  <li>Assuming dictionaries are ordered the way you would sort them - modern
      Python does remember insertion order, but that is not the same as being
      sorted alphabetically or numerically.</li>
  <li>Looping with <code>for key in data:</code> and then trying to use
      <code>key</code> as if it were the value - a plain loop over a dictionary
      gives you the keys, not the values.</li>
</ul>
<h4>Try it yourself</h4>
<p>Try <code>player["lives"]</code> on a dictionary that has no
<code>"lives"</code> key and read the <code>KeyError</code>. Then rewrite the
same lookup with <code>player.get("lives", 3)</code> so it never crashes.</p>
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
        glossary=[
            GlossaryTerm(
                "dictionary",
                "A collection of key: value pairs, written in curly braces, that "
                "looks values up by key instead of by position.",
            ),
            GlossaryTerm(
                "key",
                "The name used to look up a value in a dictionary, e.g. \"name\" in "
                "{\"name\": \"Nova\"}.",
            ),
            GlossaryTerm(
                ".get()",
                "A dictionary method that looks up a key and returns a default "
                "value instead of crashing when the key is missing.",
            ),
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
      (no argument splits on runs of whitespace)</li>
  <li><code>"-".join(items)</code> - the opposite of split, glueing a list of
      strings back together</li>
  <li><code>text.replace("a", "b")</code> - swap one bit for another</li>
  <li><code>text.lower()</code> - level the playing field before comparing</li>
</ul>
<p>Strings are <strong>immutable</strong>: these methods never change the
original, they hand you a new string. You have to store the result, usually by
assigning it back to the same name, e.g. <code>text = text.strip()</code>.</p>
<h4>Why this matters</h4>
<p>Data from the outside world - typed by a user, read from a file, pasted from
somewhere else - is almost never perfectly formatted. Cleaning and splitting
text like this is one of the most common tasks in real programming, well
before you get to anything that looks like a "proper" algorithm.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Calling <code>text.strip()</code> and expecting <code>text</code> itself
      to change - immutability means you must capture the returned value.</li>
  <li>Calling <code>.join()</code> on the list instead of the separator - it is
      <code>separator.join(list)</code>, which reads backwards the first few
      times you use it.</li>
  <li>Splitting on the wrong character, or forgetting that <code>split()</code>
      with no argument also collapses multiple spaces into one gap.</li>
</ul>
<h4>Try it yourself</h4>
<p>Try <code>"a,b,,c".split(",")</code> and notice the empty string it produces
between the two commas. Then try <code>"a  b   c".split()</code> with no
argument on a string that uses spaces instead - see how it collapses runs of
whitespace in a way <code>split(",")</code> does not for repeated commas.</p>
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
        glossary=[
            GlossaryTerm(
                "immutable",
                "Cannot be changed after it is created. Strings are immutable, so "
                "every string method returns a brand new string instead of editing "
                "the original.",
            ),
            GlossaryTerm(
                "split()",
                "A string method that breaks text into a list of pieces, cutting at "
                "a given character or, with no argument, at runs of whitespace.",
            ),
            GlossaryTerm(
                "join()",
                'A string method that glues a list of strings together with the '
                'string it is called on in between, e.g. "-".join(["a", "b"]).',
            ),
        ],
    ),
    Lesson(
        slug="number-formatting",
        title="Formatting Numbers Neatly",
        goal="Control decimal places and thousands separators in f-strings.",
        minutes=12,
        xp=30,
        concept="""
<p>An f-string can do more than drop a value in place - add a
<strong>format spec</strong> after a colon to control how it looks.</p>
<ul>
  <li><code>{value:.2f}</code> - always show exactly two decimal places</li>
  <li><code>{value:,}</code> - add a comma every three digits</li>
  <li><code>{value:,.2f}</code> - both at once</li>
</ul>
<p>These specs work on numbers, not text - trying them on a string raises an
error, so convert first if you need to. The letter at the end names the
presentation type: <code>f</code> for a fixed-point decimal is the one you will
use most, but there are others for percentages, scientific notation and more,
which you can look up as you need them.</p>
<h4>Why this matters</h4>
<p>Raw numbers are rarely how you want to show them to a person - nobody wants
to see <code>1234.5</code> on a receipt when <code>$1,234.50</code> is what a
till would print. Presentation-quality output is part of what separates a
finished program from a working one.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting the leading dot before the number of decimal places -
      <code>{value:2f}</code> is not the same as <code>{value:.2f}</code>.</li>
  <li>Applying a numeric format spec to a value that is actually a string,
      which raises a <code>ValueError</code>.</li>
  <li>Rounding surprises: <code>{2.675:.2f}</code> can print <code>2.67</code>
      rather than <code>2.68</code>, because 2.675 cannot be stored exactly as
      a float - worth knowing before you rely on it for money.</li>
</ul>
<h4>Try it yourself</h4>
<p>Try the format spec <code>{value:+.2f}</code> - the <code>+</code> shows a
sign on positive numbers too. Then pass a negative amount through
<code>format_price</code> and check whether the minus sign ends up in a sensible
place next to the dollar sign.</p>
""",
        example=(
            "price = 3.5\ntotal = 125000\n\n"
            'print(f"${price:.2f}")\n'
            'print(f"{total:,}")\n'
            'print(f"${total:,.2f}")'
        ),
        brief=(
            "Write <code>format_price(amount)</code> returning a string like "
            "<code>$1,234.50</code> for the given amount - a dollar sign, comma "
            "thousands separator, and exactly two decimal places."
        ),
        starter="def format_price(amount):\n    \n",
        solution='def format_price(amount):\n    return f"${amount:,.2f}"\n',
        checks=[
            {"kind": "call", "func": "format_price", "args": [1234.5], "expect": "$1,234.50", "label": "Comma and two decimals"},
            {"kind": "call", "func": "format_price", "args": [0], "expect": "$0.00", "label": "Zero"},
            {"kind": "call", "func": "format_price", "args": [1000000], "expect": "$1,000,000.00", "label": "Two commas"},
            {"kind": "call", "func": "format_price", "args": [42.4], "expect": "$42.40", "label": "Pads to two decimals"},
            {
                "kind": "source",
                "must_contain": [r",\.2f"],
                "describe": "Uses the ,.2f format spec",
                "label": "Uses a format spec",
            },
        ],
        hints=[
            "The format spec goes after a colon, inside the curly brackets.",
            "Combine both specs in one go: {amount:,.2f}",
            'f"${amount:,.2f}"',
        ],
        glossary=[
            GlossaryTerm(
                "format spec",
                "The part after the colon inside an f-string's curly brackets that "
                "controls how a value is displayed, e.g. :.2f for two decimal places.",
            ),
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
walk a grid, build a times table, or compare every pair in a list. This kind of
loop is called a <strong>nested loop</strong>.</p>
<p>Watch the indentation. Code indented once belongs to the outer loop; code
indented twice belongs to the inner one. Getting that wrong is the most common
bug in nested loops - a line that should run once per outer step accidentally
ends up running once per inner step, or the other way round.</p>
<h4>Why this matters</h4>
<p>Anything laid out in rows and columns - a spreadsheet, a game board, an
image's pixels - is naturally processed with a nested loop: the outer loop
walks the rows, the inner loop walks each column within that row. Comparing
every item in a list against every other item also needs two loops.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Resetting a variable (like the inner list in the example) in the wrong
      place - it usually needs to happen once per outer loop, not once overall
      and not once per inner loop.</li>
  <li>Losing track of which loop variable is which once you have <code>row</code>
      and <code>col</code> both in scope - clear, different names help far more
      than <code>i</code> and <code>j</code> once loops are nested.</li>
  <li>Not noticing how quickly the work grows: two loops of size <code>n</code>
      do <code>n * n</code> rounds of work, which gets slow fast for large
      <code>n</code>.</li>
</ul>
<h4>Try it yourself</h4>
<p>Change the inner loop's range so it depends on the outer counter, e.g.
<code>range(1, row + 1)</code>, and see the triangle shape it produces instead
of a rectangle.</p>
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
        glossary=[
            GlossaryTerm(
                "nested loop",
                "A loop written inside the body of another loop, so the inner loop "
                "runs to completion once for every round of the outer loop.",
            ),
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
<p>Python runs the <code>try</code> block; if a matching <strong>exception</strong>
(the object Python creates to describe an error) is raised partway through, it
immediately jumps to the matching <code>except</code> block instead of crashing
the whole program. If nothing goes wrong, the <code>except</code> block is
simply skipped.</p>
<p>Always name the specific error you expect, such as <code>ValueError</code> or
<code>ZeroDivisionError</code>. A bare <code>except:</code> swallows every
problem including your own typos, which makes bugs very hard to find - you want
to handle the failure you predicted, not silently hide every possible one.</p>
<h4>Why this matters</h4>
<p>Software that talks to the real world - reading user input, opening a file,
calling another service - will eventually meet bad data. The choice is between
crashing every time that happens, or deciding in advance what a sensible
fallback looks like. <code>try</code>/<code>except</code> is how Python
expresses that decision.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Using a bare <code>except:</code> that catches everything, hiding real
      bugs alongside the error you meant to handle.</li>
  <li>Wrapping far more code than necessary inside <code>try</code>, so it
      becomes unclear which line could actually fail.</li>
  <li>Forgetting that code after the point of failure inside <code>try</code>
      never runs - execution jumps straight to <code>except</code> the moment
      the error happens.</li>
</ul>
<h4>Try it yourself</h4>
<p>Change <code>except ZeroDivisionError</code> to <code>except ValueError</code>
and call <code>safe_divide(10, 0)</code> again - the program now crashes,
because you are no longer catching the error that actually happens.</p>
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
        glossary=[
            GlossaryTerm(
                "exception",
                "An object Python creates to describe an error while a program is "
                "running, such as ValueError or ZeroDivisionError.",
            ),
            GlossaryTerm(
                "try",
                "Marks a block of code that might fail, so a matching except block "
                "can handle the failure instead of crashing the program.",
            ),
            GlossaryTerm(
                "except",
                "Catches a named kind of exception raised inside the matching try "
                "block and runs its own block of recovery code instead.",
            ),
        ],
    ),
    Lesson(
        slug="modules",
        title="Borrowing Other People's Code",
        goal="Use the standard library instead of reinventing it.",
        minutes=12,
        xp=30,
        concept="""
<p>Python ships with hundreds of ready-made tools grouped into modules, together
called the <strong>standard library</strong>. <code>import</code> brings one in:</p>
<pre><code>import math
print(math.sqrt(16))

import random
print(random.randint(1, 6))</code></pre>
<p>Handy ones: <code>math.sqrt</code>, <code>math.floor</code>,
<code>math.pi</code>, <code>random.randint(a, b)</code> (both ends included),
<code>random.choice(items)</code>, <code>random.shuffle(items)</code>.</p>
<p>Because random results change every run, tests usually check that an answer is
<em>in the right range</em> rather than exactly equal to something - which is
also why the roll_dice checks below only test the edge cases where the answer
is forced to be a specific value.</p>
<h4>Why this matters</h4>
<p>Nobody writes everything from scratch. Knowing that the standard library
exists - and getting into the habit of checking it before writing your own
version of something common, like square roots or shuffling a list - saves an
enormous amount of time and avoids reinventing code that is already
well-tested.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Calling a module's function without the module name in front, e.g.
      <code>sqrt(16)</code> instead of <code>math.sqrt(16)</code>.</li>
  <li>Importing a module you never actually use, or forgetting to import one
      you do - both are easy to spot from the error message Python gives you.</li>
  <li>Assuming every useful tool must be a module function - some, like
      <code>len()</code> and <code>print()</code>, are always available and
      need no import at all.</li>
</ul>
<h4>Try it yourself</h4>
<p>Try <code>random.choice(["rock", "paper", "scissors"])</code> a few times in
a row. Then look up one <code>math</code> function you have not used yet, such
as <code>math.ceil</code>, and try it on a few different numbers.</p>
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
        glossary=[
            GlossaryTerm(
                "standard library",
                "The large collection of ready-made modules that ships with Python "
                "itself, covering maths, randomness, dates, files and much more.",
            ),
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
normal loop instead. A comprehension is not a new idea, just a more compact way
to write a pattern you already know from the for-loops lesson.</p>
<h4>Why this matters</h4>
<p>Transforming and filtering a list - "give me the upper-cased version of every
word longer than three letters" - is one of the single most common things code
does with data. A comprehension says exactly that, in roughly the same number of
words, instead of four lines of loop scaffolding.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Cramming too much logic into one comprehension until it becomes harder to
      read than the loop it replaced - that is a sign to switch back to a
      normal <code>for</code> loop.</li>
  <li>Using round brackets <code>(...)</code> by accident instead of square
      ones - that creates a different kind of object (a generator) rather than
      a list.</li>
  <li>Forgetting the <code>if</code> goes at the <em>end</em>, after the
      <code>for</code>, not at the start like in a normal sentence.</li>
</ul>
<h4>Try it yourself</h4>
<p>Rewrite <code>long_words</code> with a normal <code>for</code> loop, an empty
list, and an <code>if</code> inside it, then compare the two versions side by
side - same result, several more lines.</p>
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
        glossary=[
            GlossaryTerm(
                "list comprehension",
                "A compact way to build a list by transforming and optionally "
                "filtering another iterable in one line: [expr for item in items "
                "if condition].",
            ),
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
<p>The pattern - start with an empty <strong>accumulator</strong>, walk the
data, update the accumulator, return it - is one you will use for years. It is
the same shape as the letter counter from the dictionaries lesson, just with
more interesting data. An accumulator can be a number you add to, a list you
append to, or, as here, a dictionary you update - the shape changes, but the
"start empty, update as you go" idea stays the same.</p>
<h4>Why this matters</h4>
<p>This is the shape behind most real reporting code: totalling up sales,
counting votes, building a leaderboard, summarising log files. Recognising
"I need to walk some data and build up a result" as this exact pattern will
save you from reinventing it every time.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Starting the accumulator inside the loop instead of before it, which
      resets it back to empty on every single item.</li>
  <li>Using <code>&lt;=</code> when the brief says "below" (which means
      strictly less than) or vice versa - re-read the exact wording of a
      requirement rather than assuming.</li>
  <li>Forgetting to sort the final result when the brief asks for a specific,
      predictable order.</li>
</ul>
<h4>Try it yourself</h4>
<p>Add a brand new item straight into the <code>stock</code> dictionary before
calling <code>restock</code>, and check your function handles a key it has
never seen in these examples just as well as the ones it has.</p>
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
        glossary=[
            GlossaryTerm(
                "accumulator pattern",
                "Start with an empty result (a number, list or dictionary), walk "
                "through some data updating it, then return it - the shape behind "
                "most summarising code.",
            ),
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
