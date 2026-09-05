"""Foundations track - typically ages 10-12, no prior coding needed."""
from __future__ import annotations

from .schema import Lesson, Track

LESSONS = [
    Lesson(
        slug="hello-world",
        title="Your First Words",
        goal="Make the computer say something out loud.",
        minutes=6,
        xp=20,
        concept="""
<p>Every program you will ever write does one basic thing: it tells the computer
what to do, one step at a time. The very first instruction most people learn is
<code>print()</code>.</p>
<p><code>print()</code> puts text on the screen. The words you want shown go
inside the brackets, wrapped in quote marks:</p>
<p>The quote marks tell Python "this is text, not an instruction". Miss one out
and Python gets confused - which is completely normal and happens to everyone.</p>
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
right:</p>
<p>Values come in types. A <code>str</code> (string) is text in quotes, an
<code>int</code> is a whole number, and a <code>float</code> is a number with a
decimal point. Notice that numbers do <em>not</em> get quote marks - if you write
<code>age = "12"</code> Python treats it as text, not a number you can do maths
with.</p>
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
answer in a new variable.</p>
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
<p>Strings also come with built-in tools you call with a dot:</p>
<ul>
  <li><code>name.upper()</code> - SHOUTING</li>
  <li><code>name.lower()</code> - quiet</li>
  <li><code>len(name)</code> - how many characters</li>
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
<code>int()</code>:</p>
<pre><code>age = int(input())</code></pre>
<p>In the lesson player there is a box below the editor where you can type the
input your program will receive.</p>
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
spaces:</p>
<p>Add <code>elif</code> (short for "else if") for more options, and
<code>else</code> for everything that is left over. Python checks them top to
bottom and stops at the first one that is true.</p>
<p>Conditions are built from comparisons: <code>==</code> equal to (two equals
signs!), <code>!=</code> not equal, <code>&gt;</code>, <code>&lt;</code>,
<code>&gt;=</code>, <code>&lt;=</code>.</p>
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
    ),
    Lesson(
        slug="for-loops",
        title="Doing It Again",
        goal="Repeat work with a for loop.",
        minutes=12,
        xp=30,
        concept="""
<p>Computers are brilliant at repeating things. A <code>for</code> loop runs the
same indented block once for every item it is given.</p>
<p><code>range(5)</code> counts <code>0, 1, 2, 3, 4</code> - it starts at zero and
stops <em>before</em> the number you give it. <code>range(1, 6)</code> counts
<code>1</code> to <code>5</code>, and <code>range(0, 10, 2)</code> counts in
twos.</p>
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
The last item is always <code>-1</code>.</p>
<p>Useful tools: <code>len(items)</code> counts them, <code>items.append(x)</code>
adds to the end, <code>sum(numbers)</code> adds them up, and
<code>max()</code> / <code>min()</code> find the extremes.</p>
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
advance how many rounds you need.</p>
<p>The danger: if the condition never becomes false, the loop runs forever.
Something inside the loop must move you towards stopping. The lesson player will
stop a runaway loop after a few seconds, so nothing breaks - but the check will
fail.</p>
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
    ),
    Lesson(
        slug="functions",
        title="Naming Your Own Instructions",
        goal="Write reusable functions that take input and give back a result.",
        minutes=15,
        xp=35,
        concept="""
<p>A <strong>function</strong> is a chunk of code with a name. You write it once
and use it as many times as you like.</p>
<p><code>def</code> starts the definition. The names in the brackets are
<strong>parameters</strong> - the information the function needs.
<code>return</code> hands a value back to whoever called it.</p>
<p><code>print</code> and <code>return</code> are not the same thing.
<code>print</code> shows something to a human; <code>return</code> gives a value
back to the program so it can be used again. Almost every check in this course
looks at what you <code>return</code>.</p>
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
lists up for you, or you can loop over the positions with
<code>range(len(answers))</code>.</p>
<p>To turn a count into a percentage: <code>round(correct / total * 100)</code>.</p>
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
