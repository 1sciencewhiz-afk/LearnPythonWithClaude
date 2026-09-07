"""Foundations track - typically ages 10-12, no prior coding needed."""
from __future__ import annotations

from .schema import GlossaryTerm, Lesson, Track

LESSONS = [
    Lesson(
        slug="hello-world",
        title="Your First Words",
        goal="Make the computer say something out loud.",
        minutes=6,
        xp=20,
        concept="""
<p>Every program you will ever write does one basic thing: it tells the computer
what to do, one step at a time. Python reads your file from the top down and
runs each line in order - that ordered list of steps is called an
<strong>instruction</strong>. The very first instruction most people learn is
<code>print()</code>.</p>
<p><code>print()</code> puts text on the screen. The words you want shown go
inside the brackets, wrapped in quote marks:</p>
<p>The quote marks tell Python "this is text, not an instruction". Miss one out
and Python gets confused - which is completely normal and happens to everyone.
<code>print</code> with the round brackets is called <strong>calling a
function</strong>: you are asking a ready-made tool, written by someone else, to
do its job for you. You will write your own functions soon.</p>
<h4>Why this matters</h4>
<p>Nearly every program - a website, a game, a phone app - eventually shows text
to a human being. <code>print()</code> is the simplest possible version of that,
and it is also how you will peek inside your programs later to see what they are
doing while you are debugging them.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting one of the quote marks - Python will point at the line and
      complain that the string never ends.</li>
  <li>Forgetting the round brackets - <code>print "hi"</code> is not valid
      Python (it was valid in a much older version, so you may see it in old
      tutorials).</li>
  <li>Mixing a double quote with a single quote, like <code>print("hi')</code>
      - the two ends must match.</li>
</ul>
""",
        example='print("Hello, world!")\nprint("I am learning Python.")',
        brief="Print exactly one line that says: I am learning Python!",
        starter='# Type your print() below\n',
        solution='print("I am learning Python!")',
        checks=[
            {
                "kind": "stdout",
                "expect": "I am learning Python!",
                "match": "exact",
                "label": "Prints 'I am learning Python!'",
            }
        ],
        hints=[
            "Start with the word print followed by round brackets.",
            'Put the text inside quote marks: print("...")',
            'The whole answer is one line: print("I am learning Python!")',
        ],
        glossary=[
            GlossaryTerm(
                "print()",
                "A built-in function that displays text or values on the screen. "
                "Whatever you put inside the brackets is shown when the line runs.",
            ),
            GlossaryTerm(
                "string",
                "Text data, always wrapped in quote marks - single ('...') or "
                'double ("...") both work, as long as the two ends match.',
            ),
            GlossaryTerm(
                "function call",
                "Running a function by writing its name followed by round brackets, "
                "such as print(\"hi\"). The brackets may contain the information the "
                "function needs.",
            ),
        ],
    ),
    Lesson(
        slug="variables",
        title="Boxes That Remember",
        goal="Store information in variables and use it later.",
        minutes=10,
        xp=25,
        concept="""
<p>A <strong>variable</strong> is a name that remembers a value. Think of it as a
labelled box: you put something in, and later you ask for it back by name.</p>
<p>You make one with an equals sign. The name goes on the left, the value on the
right. This is called an <strong>assignment</strong> - it does not test whether
two things are equal (that is a different symbol, coming up soon); it stores
the right-hand value under the left-hand name.</p>
<p>Values come in types. A <code>str</code> (string) is text in quotes, an
<code>int</code> is a whole number, and a <code>float</code> is a number with a
decimal point. Notice that numbers do <em>not</em> get quote marks - if you write
<code>age = "12"</code> Python treats it as text, not a number you can do maths
with. You can always check what type something is with <code>type(age)</code>.</p>
<h4>Why this matters</h4>
<p>Without variables every program would be a single, fixed calculation. Variables
let a program remember a player's score, a user's name, or how many lives are
left, and update that memory as the program runs - which is the difference
between a calculator and software.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Using a variable before you have assigned it a value - Python raises a
      <code>NameError</code> because there is nothing in the box yet.</li>
  <li>Quoting a number by accident (<code>legs = "4"</code>) - it will print fine,
      but <code>legs + 1</code> will crash, because you cannot add a number to
      text.</li>
  <li>Variable names are case-sensitive: <code>pet</code> and <code>Pet</code> are
      two different boxes.</li>
</ul>
""",
        example='player = "Sam"\nscore = 0\nspeed = 1.5\n\nprint(player)\nprint(score)',
        brief=(
            "Create a variable called <code>pet</code> holding the text <code>Rex</code>, "
            "and a variable called <code>legs</code> holding the number <code>4</code>. "
            "Print <code>pet</code> first, then <code>legs</code>."
        ),
        starter="pet = \nlegs = \n\n",
        solution='pet = "Rex"\nlegs = 4\n\nprint(pet)\nprint(legs)',
        checks=[
            {"kind": "stdout", "expect": "Rex\n4", "match": "exact", "label": "Prints Rex then 4"},
            {
                "kind": "source",
                "must_contain": [r"\bpet\s*=", r"\blegs\s*="],
                "describe": "Uses variables named pet and legs",
                "label": "Uses both variables",
            },
        ],
        hints=[
            "Text needs quote marks. Numbers do not.",
            "You need two print() lines, one for each variable.",
            'pet = "Rex" then legs = 4, then print each of them.',
        ],
        glossary=[
            GlossaryTerm(
                "variable",
                "A name that remembers a value, created with an equals sign, so the "
                "value can be used or changed later in the program.",
            ),
            GlossaryTerm(
                "assignment (=)",
                "Storing a value under a name, e.g. score = 0. The name goes on the "
                "left, the value on the right.",
            ),
            GlossaryTerm(
                "str (string)",
                "Python's type for text. String values are always written in quote "
                "marks in your code.",
            ),
            GlossaryTerm(
                "int (integer)",
                "Python's type for whole numbers, positive or negative, with no "
                "decimal point.",
            ),
            GlossaryTerm(
                "float",
                "Python's type for numbers with a decimal point, such as 1.5 - "
                'short for "floating-point number".',
            ),
        ],
    ),
    Lesson(
        slug="doing-maths",
        title="Python Is a Calculator",
        goal="Use arithmetic to work out an answer.",
        minutes=10,
        xp=25,
        concept="""
<p>Python does maths with the symbols you already know, plus a couple of new ones:</p>
<ul>
  <li><code>+</code> add, <code>-</code> subtract</li>
  <li><code>*</code> multiply (a star, not an x)</li>
  <li><code>/</code> divide - always gives a decimal, so <code>10 / 2</code> is <code>5.0</code></li>
  <li><code>//</code> divide and throw away the remainder: <code>7 // 2</code> is <code>3</code></li>
  <li><code>%</code> the remainder only: <code>7 % 2</code> is <code>1</code></li>
</ul>
<p>You can do maths with variables just as easily as with numbers, and store the
answer in a new variable. Python also follows the maths order of operations you
learned in school (multiply and divide before add and subtract), and you can use
round brackets to force a different order, just like on paper.</p>
<h4>Why this matters</h4>
<p><code>//</code> and <code>%</code> come up constantly once you notice them:
sharing items evenly between friends, converting seconds into minutes and
seconds, checking whether a number is even (<code>n % 2 == 0</code>), and laying
items out into a grid all use exactly this pair of operators.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Using <code>/</code> when you wanted a whole number - it always returns a
      float, even when the division is exact.</li>
  <li>Mixing up <code>//</code> (the answer) and <code>%</code> (the leftover) -
      it helps to say them out loud as "how many whole times" and "what's left
      over".</li>
  <li>Forgetting that <code>*</code> and <code>/</code> run before <code>+</code>
      and <code>-</code>, the same as in maths class.</li>
</ul>
""",
        example="apples = 12\nfriends = 5\n\neach = apples // friends\nleft_over = apples % friends\n\nprint(each)\nprint(left_over)",
        brief=(
            "A cinema seat costs 9 pounds. Work out the cost for 7 tickets, store it "
            "in a variable called <code>total</code>, and print it."
        ),
        starter="price = 9\ntickets = 7\n\n",
        solution="price = 9\ntickets = 7\n\ntotal = price * tickets\nprint(total)",
        checks=[
            {"kind": "stdout", "expect": "63", "match": "exact", "label": "Prints 63"},
            {
                "kind": "source",
                "must_contain": [r"\btotal\s*="],
                "must_not_contain": [r"total\s*=\s*63\b"],
                "describe": "Calculates total instead of typing the answer",
                "label": "Works out the answer with maths",
            },
        ],
        hints=[
            "Multiplication uses the * symbol.",
            "Store the result: total = price * tickets",
            "Then print(total) - do not just print 63.",
        ],
        glossary=[
            GlossaryTerm(
                "operator",
                "A symbol that does a job on values, such as + for addition or * for "
                "multiplication.",
            ),
            GlossaryTerm(
                "integer division (//)",
                "Division that throws away any remainder and keeps only the whole "
                "number of times one value fits into another, e.g. 7 // 2 is 3.",
            ),
            GlossaryTerm(
                "modulo (%)",
                "Gives the remainder left over after dividing, e.g. 7 % 2 is 1. "
                "Handy for checking even/odd numbers or wrapping values around.",
            ),
        ],
    ),
    Lesson(
        slug="strings",
        title="Playing With Text",
        goal="Join text together and format it neatly.",
        minutes=12,
        xp=25,
        concept="""
<p>Text in Python is called a <strong>string</strong>. You can glue strings
together with <code>+</code>, but the tidiest way to mix text and variables is an
<strong>f-string</strong>. Put an <code>f</code> just before the opening quote,
then wrap any variable in curly brackets:</p>
<p>Strings also come with built-in tools you call with a dot, known as
<strong>string methods</strong>:</p>
<ul>
  <li><code>name.upper()</code> - SHOUTING</li>
  <li><code>name.lower()</code> - quiet</li>
  <li><code>len(name)</code> - how many characters</li>
</ul>
<p>A method is just a function that belongs to a value - you call it by writing
a dot after the value, then the method's name and brackets. <code>len()</code>
is different: it is a regular function that works on strings (and, later, lists),
so it goes before the value rather than after a dot.</p>
<h4>Why this matters</h4>
<p>Almost every program that talks to a human formats text: a greeting with the
player's name in it, a scoreboard, an error message. f-strings are the
Python-native way to build a sentence out of pieces, and you will use them in
nearly every remaining lesson.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting the <code>f</code> before the opening quote - without it, the
      curly brackets print as literal <code>{}</code> characters instead of the
      variable's value.</li>
  <li>Trying to <code>+</code> a string and a number directly, like
      <code>"Score: " + 10</code> - Python refuses; an f-string sidesteps the
      problem entirely.</li>
  <li>Misspelling a variable name inside the curly brackets - Python still
      raises a <code>NameError</code> even though it is inside quote marks.</li>
</ul>
""",
        example='name = "Ada"\nage = 12\n\nprint(f"{name} is {age} years old.")\nprint(name.upper())\nprint(len(name))',
        brief=(
            "Using the variables given, print one line in exactly this shape:<br>"
            "<code>Nova scored 42 points!</code><br>Use an f-string."
        ),
        starter='player = "Nova"\npoints = 42\n\n',
        solution='player = "Nova"\npoints = 42\n\nprint(f"{player} scored {points} points!")',
        checks=[
            {
                "kind": "stdout",
                "expect": "Nova scored 42 points!",
                "match": "exact",
                "label": "Prints the sentence exactly",
            },
            {
                "kind": "source",
                "must_contain": [r'f"', r"\{player\}", r"\{points\}"],
                "describe": "Uses an f-string with both variables",
                "label": "Uses an f-string",
            },
        ],
        hints=[
            'An f-string starts like this: f"..."',
            "Put variable names inside curly brackets: {player}",
            'print(f"{player} scored {points} points!")',
        ],
        glossary=[
            GlossaryTerm(
                "f-string",
                'A string written as f"..." that lets you drop variables straight '
                "into the text by wrapping them in curly brackets, e.g. f\"{name}\".",
            ),
            GlossaryTerm(
                "string method",
                "A built-in tool that belongs to a string, called with a dot, such "
                "as name.upper() or name.lower().",
            ),
            GlossaryTerm(
                "len()",
                "A built-in function that counts how many items something contains "
                "- characters in a string, or later, entries in a list.",
            ),
        ],
    ),
    Lesson(
        slug="asking-questions",
        title="Talking Back",
        goal="Read what somebody types and reply to it.",
        minutes=10,
        xp=25,
        concept="""
<p><code>input()</code> pauses your program, waits for somebody to type something
and press Enter, then hands you back what they typed.</p>
<p>Whatever comes out of <code>input()</code> is <strong>always a string</strong>,
even if they typed digits. To do maths with it you must convert it first with
<code>int()</code> - this is called <strong>type conversion</strong>, turning a
value from one type into another:</p>
<pre><code>age = int(input())</code></pre>
<p>In the lesson player there is a box below the editor where you can type the
input your program will receive, one line per <code>input()</code> call. When
your program is graded, that box's contents are fed in automatically, in order -
so the checks can run your program without a human typing anything.</p>
<h4>Why this matters</h4>
<p>A program that only ever does the same thing is not very useful. Reading
input is the first step towards programs that react to a real person: quizzes,
calculators, chatbots and games all start with <code>input()</code>.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting that <code>input()</code> always returns text, then trying to
      do maths with it and getting a <code>TypeError</code>.</li>
  <li>Printing an extra question before reading the input, when the checks
      expect only the final answer - read the brief carefully for exactly what
      should be printed.</li>
  <li>Converting with <code>int()</code> when the input might have a decimal
      point - that needs <code>float()</code> instead.</li>
</ul>
""",
        example='print("What is your name?")\nname = input()\nprint(f"Nice to meet you, {name}.")',
        brief=(
            "Read a name with <code>input()</code>, then print "
            "<code>Hello NAME, welcome!</code> with the typed name in place of NAME."
        ),
        starter="name = input()\n",
        solution='name = input()\nprint(f"Hello {name}, welcome!")',
        checks=[
            {
                "kind": "stdout",
                "stdin": "Maya\n",
                "expect": "Hello Maya, welcome!",
                "match": "exact",
                "label": "Greets Maya",
            },
            {
                "kind": "stdout",
                "stdin": "Ravi\n",
                "expect": "Hello Ravi, welcome!",
                "match": "exact",
                "label": "Greets Ravi too",
            },
        ],
        hints=[
            "Store the input in a variable first: name = input()",
            "Do not print a question - the checks only want the greeting line.",
            'print(f"Hello {name}, welcome!")',
        ],
        glossary=[
            GlossaryTerm(
                "input()",
                "A built-in function that pauses the program, waits for someone to "
                "type a line and press Enter, and returns what they typed as a string.",
            ),
            GlossaryTerm(
                "type conversion",
                "Turning a value from one type into another, e.g. int(\"12\") turns "
                "the string \"12\" into the number 12.",
            ),
        ],
    ),
    Lesson(
        slug="decisions",
        title="Making Choices",
        goal="Run different code depending on a condition.",
        minutes=14,
        xp=30,
        concept="""
<p>An <code>if</code> statement lets your program choose. The line ends with a
colon, and everything that belongs to it is <strong>indented</strong> by four
spaces - Python uses that indentation to know which lines are "inside" the
if, instead of curly brackets like some other languages use.</p>
<p>Add <code>elif</code> (short for "else if") for more options, and
<code>else</code> for everything that is left over. Python checks them top to
bottom and stops at the first one that is true - later conditions are not even
looked at once one has matched.</p>
<p>Conditions are built from comparisons: <code>==</code> equal to (two equals
signs - one equals sign is assignment, from the variables lesson, and mixing
the two up is one of the most common early bugs), <code>!=</code> not equal,
<code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code>. A
comparison always produces a <strong>boolean</strong>: the special value
<code>True</code> or <code>False</code>.</p>
<h4>Why this matters</h4>
<p>Branching is what separates a program from a fixed sequence of steps: log in
or show an error, level up or not, discount price or full price. Every piece of
software you have ever used is full of <code>if</code> statements deciding what
to show you next.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Writing <code>if temp = 25:</code> instead of <code>if temp == 25:</code> -
      Python will refuse to run and explain that assignment cannot be used here.</li>
  <li>Forgetting the colon at the end of the <code>if</code>/<code>elif</code>/
      <code>else</code> line.</li>
  <li>Indenting inconsistently (mixing tabs and spaces, or using a different
      number of spaces on different lines) - Python will raise an
      <code>IndentationError</code>.</li>
</ul>
""",
        example='score = 85\n\nif score >= 90:\n    print("Gold")\nelif score >= 70:\n    print("Silver")\nelse:\n    print("Bronze")',
        brief=(
            "Write a function <code>weather(temp)</code> that returns "
            "<code>\"Hot\"</code> when temp is 25 or more, <code>\"Mild\"</code> when it "
            "is 15 to 24, and <code>\"Cold\"</code> below 15."
        ),
        starter="def weather(temp):\n    # your if statement goes here\n",
        solution=(
            "def weather(temp):\n"
            "    if temp >= 25:\n"
            '        return "Hot"\n'
            "    elif temp >= 15:\n"
            '        return "Mild"\n'
            "    else:\n"
            '        return "Cold"\n'
        ),
        checks=[
            {"kind": "call", "func": "weather", "args": [30], "expect": "Hot", "label": "30 is Hot"},
            {"kind": "call", "func": "weather", "args": [25], "expect": "Hot", "label": "25 is Hot"},
            {"kind": "call", "func": "weather", "args": [18], "expect": "Mild", "label": "18 is Mild"},
            {"kind": "call", "func": "weather", "args": [15], "expect": "Mild", "label": "15 is Mild"},
            {"kind": "call", "func": "weather", "args": [3], "expect": "Cold", "label": "3 is Cold"},
        ],
        hints=[
            "Check the biggest number first, then work downwards.",
            "Use return, not print - the checks look at what comes back.",
            "if temp >= 25: ... elif temp >= 15: ... else: ...",
        ],
        glossary=[
            GlossaryTerm(
                "if statement",
                "Runs its indented block only when its condition is True, and skips "
                "it otherwise.",
            ),
            GlossaryTerm(
                "elif",
                "Short for 'else if' - an extra condition checked only when every "
                "condition above it was False.",
            ),
            GlossaryTerm(
                "else",
                "Catches everything left over: it runs when every if/elif above it "
                "was False.",
            ),
            GlossaryTerm(
                "comparison operator",
                "A symbol that compares two values and produces True or False, such "
                "as ==, !=, >, <, >= or <=.",
            ),
            GlossaryTerm(
                "indentation",
                "The spaces at the start of a line. Python uses indentation, not "
                "brackets, to show which lines belong inside an if, loop or function.",
            ),
        ],
    ),
    Lesson(
        slug="combining-conditions",
        title="And, Or, and Not",
        goal="Combine more than one condition in a single check.",
        minutes=12,
        xp=25,
        concept="""
<p>Sometimes one comparison is not enough. <code>and</code>, <code>or</code> and
<code>not</code> - the <strong>boolean operators</strong> - let you combine
conditions.</p>
<p><code>and</code> is only true when <strong>both</strong> sides are true.
<code>or</code> is true when <strong>at least one</strong> side is true.
<code>not</code> flips a condition from true to false, or false to true.</p>
<p>You can put several comparisons on one line - Python checks each one and
combines the results. Python also stops checking as soon as the overall answer
is certain: in <code>a and b</code>, if <code>a</code> is already False the
whole thing must be False, so Python never even looks at <code>b</code>.
This is called <strong>short-circuiting</strong>, and it is why
<code>lst and lst[0]</code> is a safe way to check a list is non-empty before
looking at its first item.</p>
<h4>Why this matters</h4>
<p>Real-world rules are rarely a single fact: "tall enough <em>and</em> old
enough", "it's the weekend <em>or</em> it's a holiday". Being able to combine
conditions is what lets your code match how people actually describe rules.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Using <code>or</code> when you meant <code>and</code> (or the reverse) -
      read the rule out loud and check which word you actually used.</li>
  <li>Writing <code>5 &lt; age &lt; 30</code> when you meant two separate
      checks joined with <code>and</code> - Python actually allows chained
      comparisons like this, but it is easy to get confused about what they mean
      until you are comfortable with them.</li>
  <li>Forgetting that <code>not</code> applies to the whole condition after it,
      so <code>not a and b</code> means <code>(not a) and b</code>, not
      <code>not (a and b)</code>.</li>
</ul>
""",
        example=(
            'age = 13\nhas_ticket = True\n\n'
            'if age >= 12 and has_ticket:\n'
            '    print("Welcome to the show")\n\n'
            'if age < 5 or not has_ticket:\n'
            '    print("Not allowed in")'
        ),
        brief=(
            "Write a function <code>can_ride(height_cm, age)</code> that returns "
            "<code>True</code> only when the rider is at least <code>120</code> cm tall "
            "<strong>and</strong> at least <code>8</code> years old. Otherwise return "
            "<code>False</code>."
        ),
        starter="def can_ride(height_cm, age):\n    \n",
        solution="def can_ride(height_cm, age):\n    return height_cm >= 120 and age >= 8\n",
        checks=[
            {"kind": "call", "func": "can_ride", "args": [130, 10], "expect": True, "label": "Tall and old enough"},
            {"kind": "call", "func": "can_ride", "args": [100, 10], "expect": False, "label": "Too short"},
            {"kind": "call", "func": "can_ride", "args": [130, 5], "expect": False, "label": "Too young"},
            {"kind": "call", "func": "can_ride", "args": [120, 8], "expect": True, "label": "Exactly at both minimums"},
            {
                "kind": "source",
                "must_contain": [r"\band\b"],
                "describe": "Uses and to combine both conditions",
                "label": "Uses and",
            },
        ],
        hints=[
            "Both conditions must be true, so join them with and.",
            "height_cm >= 120 and age >= 8",
            "You can return the combined comparison directly - no if needed.",
        ],
        glossary=[
            GlossaryTerm(
                "boolean",
                "A value that is either True or False. Comparisons and the and/or/"
                "not operators all produce booleans.",
            ),
            GlossaryTerm(
                "and",
                "Combines two conditions; the result is True only when both sides "
                "are True.",
            ),
            GlossaryTerm(
                "or",
                "Combines two conditions; the result is True when at least one side "
                "is True.",
            ),
            GlossaryTerm(
                "not",
                "Flips a condition: True becomes False, and False becomes True.",
            ),
        ],
    ),
    Lesson(
        slug="for-loops",
        title="Doing It Again",
        goal="Repeat work with a for loop.",
        minutes=12,
        xp=30,
        concept="""
<p>Computers are brilliant at repeating things. A <code>for</code> loop runs the
same indented block once for every item it is given - that block is called the
loop <strong>body</strong>, and each time through it is one
<strong>iteration</strong>.</p>
<p><code>range(5)</code> counts <code>0, 1, 2, 3, 4</code> - it starts at zero and
stops <em>before</em> the number you give it. <code>range(1, 6)</code> counts
<code>1</code> to <code>5</code>, and <code>range(0, 10, 2)</code> counts in
twos. <code>range()</code> is an example of an <strong>iterable</strong>: anything
a <code>for</code> loop can step through one item at a time. Strings and lists
are iterables too, so <code>for letter in "cat":</code> works exactly the same
way, visiting <code>"c"</code>, then <code>"a"</code>, then <code>"t"</code>.</p>
<h4>Why this matters</h4>
<p>Without loops, printing the 7 times table would mean writing ten separate
<code>print()</code> lines - and processing a list of a thousand names would be
impossible to write by hand at all. Loops are what let a handful of lines of
code do work that scales to any amount of data.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Off-by-one errors: forgetting that <code>range(10)</code> stops
      <em>before</em> 10, so it never includes it.</li>
  <li>Writing code outside the indented block by mistake, so it only runs once
      after the loop finishes instead of every time round.</li>
  <li>Trying to use the loop variable (<code>i</code>) after the loop as if it
      still has a special meaning - it just holds whatever value it was on the
      last time round.</li>
</ul>
""",
        example='for i in range(3):\n    print(f"Lap {i}")\n\nfor colour in ["red", "green"]:\n    print(colour)',
        brief=(
            "Print the 7 times table from 7 up to 70 - one number per line, "
            "nothing else. Use a loop, not ten print lines."
        ),
        starter="for i in range(1, 11):\n    \n",
        solution="for i in range(1, 11):\n    print(i * 7)",
        checks=[
            {
                "kind": "stdout",
                "expect": [7, 14, 21, 28, 35, 42, 49, 56, 63, 70],
                "match": "lines",
                "label": "Prints 7 to 70 in sevens",
            },
            {
                "kind": "source",
                "must_contain": [r"\bfor\b"],
                "describe": "Uses a for loop",
                "label": "Uses a loop",
            },
        ],
        hints=[
            "range(1, 11) gives you 1 up to 10.",
            "Inside the loop, multiply the counter by 7.",
            "print(i * 7) - remember it must be indented.",
        ],
        glossary=[
            GlossaryTerm(
                "for loop",
                "Repeats its indented block once for every item in something, such "
                "as a range() or a list.",
            ),
            GlossaryTerm(
                "range()",
                "Produces a sequence of whole numbers to loop over. range(5) counts "
                "0 to 4; range(1, 6) counts 1 to 5.",
            ),
            GlossaryTerm(
                "iterable",
                "Anything a for loop can step through one item at a time - ranges, "
                "strings and lists are all iterables.",
            ),
        ],
    ),
    Lesson(
        slug="lists",
        title="Keeping a Collection",
        goal="Store many values in one list and work through them.",
        minutes=14,
        xp=30,
        concept="""
<p>A <strong>list</strong> holds many values in order, inside square brackets.</p>
<p>Each item has a position called an <strong>index</strong>, and Python starts
counting at <strong>0</strong>. So in <code>["a", "b", "c"]</code>, item
<code>0</code> is <code>"a"</code> and item <code>2</code> is <code>"c"</code>.
The last item is always <code>-1</code>, the second-last <code>-2</code>, and so
on - negative indexes count backwards from the end, so you never need to know
exactly how long a list is just to reach its last item.</p>
<p>Useful tools: <code>len(items)</code> counts them, <code>items.append(x)</code>
adds to the end, <code>sum(numbers)</code> adds them up, and
<code>max()</code> / <code>min()</code> find the extremes. Because a list
remembers order and can grow, it is a natural match for a <code>for</code> loop:
<code>for item in items:</code> visits every value, in order, without you
needing to think about indexes at all.</p>
<h4>Why this matters</h4>
<p>Almost nothing interesting is a single value - a game has a list of players, a
todo app has a list of tasks, a shop has a list of prices. Lists plus loops are
the combination that lets a program handle "many of something" instead of just
one.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Asking for an index that does not exist, like <code>scores[10]</code> on a
      3-item list - Python raises an <code>IndexError</code>.</li>
  <li>Confusing the index with the value: <code>scores[0]</code> is "the first
      item", not "the item with the value 0".</li>
  <li>Forgetting that <code>append()</code> changes the list in place and does
      not return the new list - <code>scores = scores.append(4)</code> throws
      away your list and replaces it with <code>None</code>.</li>
</ul>
""",
        example='scores = [4, 8, 15]\nprint(scores[0])\nprint(scores[-1])\n\nscores.append(23)\nprint(len(scores))\nprint(sum(scores))',
        brief=(
            "Write a function <code>highest(numbers)</code> that returns the biggest "
            "number in the list it is given."
        ),
        starter="def highest(numbers):\n    \n",
        solution="def highest(numbers):\n    return max(numbers)",
        checks=[
            {"kind": "call", "func": "highest", "args": [[3, 9, 2]], "expect": 9, "label": "Finds 9"},
            {"kind": "call", "func": "highest", "args": [[10]], "expect": 10, "label": "Works with one item"},
            {
                "kind": "call",
                "func": "highest",
                "args": [[-5, -1, -9]],
                "expect": -1,
                "label": "Works with negative numbers",
            },
        ],
        hints=[
            "Python has a built-in tool that finds the biggest value.",
            "It is called max().",
            "return max(numbers)",
        ],
        glossary=[
            GlossaryTerm(
                "list",
                "An ordered collection of values written in square brackets, such as "
                "[4, 8, 15], that can grow and shrink.",
            ),
            GlossaryTerm(
                "index",
                "A position inside a list or string, counting from 0 for the first "
                "item. Negative indexes count backwards from the end.",
            ),
            GlossaryTerm(
                "append()",
                "A list method that adds one new value to the end of the list, "
                "changing it in place.",
            ),
        ],
    ),
    Lesson(
        slug="while-loops",
        title="Keep Going Until",
        goal="Loop while a condition stays true.",
        minutes=12,
        xp=30,
        concept="""
<p>A <code>for</code> loop runs a set number of times. A <code>while</code> loop
keeps going for as long as its condition is true - useful when you do not know in
advance how many rounds you need, such as "keep asking until they guess right" or
"keep dealing cards until someone wins".</p>
<p>The danger: if the condition never becomes false, the loop runs forever - this
is called an <strong>infinite loop</strong>. Something inside the loop must move
you towards stopping, usually by changing the variable the condition checks. The
lesson player will stop a runaway loop after a few seconds, so nothing breaks -
but the check will fail, and in a real program an infinite loop would freeze it
completely.</p>
<h4>Why this matters</h4>
<p>Plenty of real problems do not have a known number of steps in advance: retry
a network request until it succeeds, keep a game running until the player quits,
keep halving a number until it reaches 1. Those all need a <code>while</code>
loop rather than a <code>for</code> loop.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting to update the variable the condition depends on, which creates
      an infinite loop.</li>
  <li>Updating the variable in the wrong direction (adding instead of
      subtracting), so the condition is never satisfied.</li>
  <li>Using <code>while</code> when a <code>for</code> loop would be simpler -
      if you already know exactly how many times to repeat, prefer
      <code>for i in range(n):</code>.</li>
</ul>
""",
        example='count = 3\nwhile count > 0:\n    print(count)\n    count = count - 1\nprint("Go!")',
        brief=(
            "Write a function <code>countdown(start)</code> that returns a list "
            "counting down from <code>start</code> to <code>1</code>. "
            "<code>countdown(3)</code> gives <code>[3, 2, 1]</code>. Use a while loop."
        ),
        starter="def countdown(start):\n    numbers = []\n    \n    return numbers\n",
        solution=(
            "def countdown(start):\n"
            "    numbers = []\n"
            "    while start > 0:\n"
            "        numbers.append(start)\n"
            "        start = start - 1\n"
            "    return numbers\n"
        ),
        checks=[
            {"kind": "call", "func": "countdown", "args": [3], "expect": [3, 2, 1], "label": "countdown(3)"},
            {"kind": "call", "func": "countdown", "args": [1], "expect": [1], "label": "countdown(1)"},
            {"kind": "call", "func": "countdown", "args": [0], "expect": [], "label": "countdown(0) is empty"},
            {
                "kind": "source",
                "must_contain": [r"\bwhile\b"],
                "describe": "Uses a while loop",
                "label": "Uses while",
            },
        ],
        hints=[
            "Loop while start is greater than 0.",
            "Add the current number with numbers.append(start).",
            "Then make start smaller, or the loop never ends.",
        ],
        glossary=[
            GlossaryTerm(
                "while loop",
                "Repeats its indented block for as long as its condition stays "
                "True, checking the condition again before every round.",
            ),
            GlossaryTerm(
                "infinite loop",
                "A loop whose condition never becomes False, so it never stops on "
                "its own - almost always caused by forgetting to update a variable.",
            ),
        ],
    ),
    Lesson(
        slug="functions",
        title="Naming Your Own Instructions",
        goal="Write reusable functions that take input and give back a result.",
        minutes=15,
        xp=35,
        concept="""
<p>A <strong>function</strong> is a chunk of code with a name. You write it once
and use it as many times as you like - this avoids repeating yourself, and gives
a name to what the code is <em>for</em>, not just what it does line by line.</p>
<p><code>def</code> starts the definition. The names in the brackets are
<strong>parameters</strong> - the information the function needs. When you
actually call the function, the values you pass in are called
<strong>arguments</strong>; the parameter is the labelled space waiting for a
value, the argument is the value you hand over. <code>return</code> hands a
value back to whoever called it.</p>
<p><code>print</code> and <code>return</code> are not the same thing.
<code>print</code> shows something to a human; <code>return</code> gives a value
back to the program so it can be used again - stored in a variable, passed to
another function, or compared with something else. Almost every check in this
course looks at what you <code>return</code>, not what you print.</p>
<h4>Why this matters</h4>
<p>Functions are how programs stay manageable as they grow. A function you write
once - "work out the ticket price for this age" - can be reused everywhere that
question comes up, and if the pricing rule changes later, you only have to fix
it in one place.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Using <code>print()</code> inside a function instead of
      <code>return</code> - the output looks right when you run it, but the
      checks (and any other code that calls your function) receive
      <code>None</code> because nothing was returned.</li>
  <li>Writing code after a <code>return</code> in the same branch and expecting
      it to run - a function stops immediately the moment a
      <code>return</code> executes.</li>
  <li>Forgetting the parentheses when calling a function, e.g. writing
      <code>ticket_price</code> instead of <code>ticket_price(5)</code>, which
      refers to the function itself rather than running it.</li>
</ul>
""",
        example='def area(width, height):\n    return width * height\n\nprint(area(3, 4))\nprint(area(10, 2))',
        brief=(
            "Write a function <code>ticket_price(age)</code>. Children under 5 go free "
            "(return <code>0</code>), under 16 pay <code>7</code>, and everyone else "
            "pays <code>12</code>."
        ),
        starter="def ticket_price(age):\n    \n",
        solution=(
            "def ticket_price(age):\n"
            "    if age < 5:\n"
            "        return 0\n"
            "    if age < 16:\n"
            "        return 7\n"
            "    return 12\n"
        ),
        checks=[
            {"kind": "call", "func": "ticket_price", "args": [3], "expect": 0, "label": "Age 3 is free"},
            {"kind": "call", "func": "ticket_price", "args": [5], "expect": 7, "label": "Age 5 pays 7"},
            {"kind": "call", "func": "ticket_price", "args": [15], "expect": 7, "label": "Age 15 pays 7"},
            {"kind": "call", "func": "ticket_price", "args": [16], "expect": 12, "label": "Age 16 pays 12"},
            {"kind": "call", "func": "ticket_price", "args": [40], "expect": 12, "label": "Age 40 pays 12"},
        ],
        hints=[
            "Deal with the youngest case first.",
            "Once a return runs, the function stops - so you may not need else.",
            "if age < 5: return 0, then if age < 16: return 7, then return 12.",
        ],
        glossary=[
            GlossaryTerm(
                "function",
                "A named, reusable block of code, defined once with def and run as "
                "many times as needed by calling its name.",
            ),
            GlossaryTerm(
                "parameter",
                "A name inside a function's brackets that stands for information the "
                "function needs, filled in with a real value each time it is called.",
            ),
            GlossaryTerm(
                "argument",
                "The actual value passed in when a function is called, matched up "
                "with its parameter.",
            ),
            GlossaryTerm(
                "return",
                "Sends a value back out of a function to whoever called it, and "
                "immediately stops the function running.",
            ),
        ],
    ),
    Lesson(
        slug="random-numbers",
        title="Adding Some Randomness",
        goal="Use the random module to make programs unpredictable - on purpose.",
        minutes=12,
        xp=30,
        concept="""
<p>Python ships with a <code>random</code> <strong>module</strong> - a ready-made
collection of extra tools you can bring into your program. <code>import random</code>
brings it in, then <code>random.randint(a, b)</code> gives you a whole number
between <code>a</code> and <code>b</code>, <strong>including both ends</strong>.</p>
<p>Because the result changes every run, it is hard to write a test for it -
unless you <code>random.seed(number)</code> first. Seeding tells Python to
start from a fixed point, so the "random" numbers that follow are always the
same. Real games skip the seed; this lesson uses one so your answer can be
checked.</p>
<h4>Why this matters</h4>
<p>Randomness is everywhere in games and simulations: shuffling a deck, rolling
dice, picking a random enemy to spawn, choosing a quiz question. Learning to
reach for a module instead of writing everything yourself is also its own
skill - Python's standard library already has tools for hundreds of common
jobs.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting the <code>import random</code> line - every
      <code>random.something</code> call needs the module imported first,
      usually at the very top of the file.</li>
  <li>Thinking <code>random.randint(1, 10)</code> can never return 10 - it can;
      unlike <code>range()</code>, both ends are included.</li>
  <li>Seeding once per program when you actually wanted a fresh random number
      each time - seeding is only for making randomness repeatable for testing.</li>
</ul>
""",
        example=(
            "import random\n\n"
            "random.seed(42)\n"
            "print(random.randint(1, 10))\n\n"
            "random.seed(42)\n"
            "print(random.randint(1, 10))  # same number both times"
        ),
        brief=(
            "Write <code>lucky_number(seed, low, high)</code>: call "
            "<code>random.seed(seed)</code> first, then return "
            "<code>random.randint(low, high)</code>."
        ),
        starter="import random\n\n\ndef lucky_number(seed, low, high):\n    \n",
        solution=(
            "import random\n\n\n"
            "def lucky_number(seed, low, high):\n"
            "    random.seed(seed)\n"
            "    return random.randint(low, high)\n"
        ),
        checks=[
            {"kind": "call", "func": "lucky_number", "args": [42, 1, 10], "expect": 2, "label": "Seed 42 between 1 and 10"},
            {"kind": "call", "func": "lucky_number", "args": [1, 1, 6], "expect": 2, "label": "Seed 1 between 1 and 6"},
            {"kind": "call", "func": "lucky_number", "args": [7, 1, 100], "expect": 42, "label": "Seed 7 between 1 and 100"},
            {"kind": "call", "func": "lucky_number", "args": [0, 5, 5], "expect": 5, "label": "A range of exactly one number"},
            {
                "kind": "source",
                "must_contain": [r"import\s+random", r"random\.seed", r"random\.randint"],
                "describe": "Seeds random, then calls randint",
                "label": "Uses random.seed and random.randint",
            },
        ],
        hints=[
            "random.seed(seed) must run before random.randint, and use the seed argument, not a fixed number.",
            "random.randint(low, high) includes both low and high.",
            "random.seed(seed)\\nreturn random.randint(low, high)",
        ],
        glossary=[
            GlossaryTerm(
                "module",
                "A file of ready-made Python code you bring into your program with "
                "import, such as random or math.",
            ),
            GlossaryTerm(
                "import",
                "The keyword that loads a module so you can use the tools inside it, "
                "e.g. import random.",
            ),
            GlossaryTerm(
                "random.randint()",
                "Returns a random whole number between the two values given, "
                "including both ends.",
            ),
        ],
    ),
    Lesson(
        slug="quiz-project",
        title="Project: Quiz Scorer",
        goal="Put it all together and score a quiz.",
        minutes=20,
        xp=50,
        concept="""
<p>Time to combine everything: lists, loops, comparisons and functions.</p>
<p>A quiz has a list of correct answers and a list of what the player gave. Walk
through both at the same time and count the matches. <code>zip()</code> pairs two
lists up for you, giving you one item from each list per round of the loop, or
you can loop over the positions with <code>range(len(answers))</code> and index
into both lists yourself. Either approach works; <code>zip()</code> is usually
considered the tidier one once you are comfortable with it.</p>
<p>To turn a count into a percentage: <code>round(correct / total * 100)</code>.
This is also a good moment to think defensively: what should your function do
with an empty quiz, where <code>total</code> is <code>0</code>? Dividing by zero
crashes the program, so that case needs handling before the division happens.</p>
<h4>Why this matters</h4>
<p>This is your first small project rather than a single new idea - real
programming is almost always about combining a handful of familiar tools
(a loop, a condition, a function) to solve one concrete problem, not learning
an endless stream of brand new syntax.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Dividing by <code>len(answers)</code> without checking it is not zero
      first, which crashes on an empty quiz.</li>
  <li>Comparing the wrong pair of items - <code>zip()</code> pairs items in the
      order the lists are given, so the order you pass them in to
      <code>zip()</code> matters.</li>
  <li>Forgetting <code>round()</code>, so the checks see a long decimal like
      <code>66.66666...</code> instead of the expected whole number.</li>
</ul>
""",
        example=(
            'correct = ["a", "b", "c"]\ngiven = ["a", "x", "c"]\n\n'
            "score = 0\nfor right, chosen in zip(correct, given):\n"
            "    if right == chosen:\n        score = score + 1\n\nprint(score)"
        ),
        brief=(
            "Write <code>grade(answers, given)</code> that returns the percentage "
            "correct, rounded to a whole number. Two empty lists should return "
            "<code>0</code> (do not divide by zero)."
        ),
        starter="def grade(answers, given):\n    \n",
        solution=(
            "def grade(answers, given):\n"
            "    if len(answers) == 0:\n"
            "        return 0\n"
            "    score = 0\n"
            "    for right, chosen in zip(answers, given):\n"
            "        if right == chosen:\n"
            "            score = score + 1\n"
            "    return round(score / len(answers) * 100)\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "grade",
                "args": [["a", "b", "c", "d"], ["a", "b", "c", "d"]],
                "expect": 100,
                "label": "All right is 100",
            },
            {
                "kind": "call",
                "func": "grade",
                "args": [["a", "b", "c", "d"], ["a", "x", "c", "x"]],
                "expect": 50,
                "label": "Half right is 50",
            },
            {
                "kind": "call",
                "func": "grade",
                "args": [["a", "b", "c"], ["x", "x", "x"]],
                "expect": 0,
                "label": "None right is 0",
            },
            {"kind": "call", "func": "grade", "args": [[], []], "expect": 0, "label": "Empty quiz is 0"},
        ],
        hints=[
            "Guard the empty list first so you never divide by zero.",
            "Count matches with a loop and an if.",
            "Finish with round(score / len(answers) * 100).",
        ],
        glossary=[
            GlossaryTerm(
                "zip()",
                "Pairs up items from two (or more) lists position by position, so "
                "a for loop can walk through both at once.",
            ),
        ],
    ),
]

TRACK = Track(
    slug="foundations",
    title="Foundations",
    tagline="Start here. No experience needed.",
    ages="Ages 10-12",
    emoji="\N{SEEDLING}",
    blurb=(
        "Meet Python from scratch: printing, variables, maths, decisions, loops "
        "and your first functions. Every lesson ends with code you wrote yourself."
    ),
    lessons=LESSONS,
)
