"""Creators track - typically ages 16-18, heading towards real engineering."""
from __future__ import annotations

from .schema import Lesson, Track

LESSONS = [
    Lesson(
        slug="classes",
        title="Designing Your Own Types",
        goal="Bundle data and behaviour together in a class.",
        minutes=18,
        xp=40,
        concept="""
<p>A <strong>class</strong> is a blueprint. It describes what an object knows (its
attributes) and what it can do (its methods).</p>
<pre><code>class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} says woof"</code></pre>
<p><code>__init__</code> runs when you create an instance and sets it up.
<code>self</code> is the particular object being worked on - it is the first
parameter of every method, and Python passes it for you.</p>
<p>Reach for a class when several pieces of data always travel together and have
operations that belong to them. Otherwise a plain function is usually better.</p>
""",
        example=(
            "class Counter:\n"
            "    def __init__(self, start=0):\n"
            "        self.value = start\n\n"
            "    def bump(self, by=1):\n"
            "        self.value += by\n"
            "        return self.value\n\n\n"
            "c = Counter()\nprint(c.bump())\nprint(c.bump(5))"
        ),
        brief=(
            "Write a class <code>BankAccount</code> with <code>__init__(self, owner, "
            "balance=0)</code>, a <code>deposit(amount)</code> method, and a "
            "<code>withdraw(amount)</code> method that returns <code>False</code> and "
            "changes nothing if there are insufficient funds, otherwise "
            "<code>True</code>."
        ),
        starter=(
            "class BankAccount:\n"
            "    def __init__(self, owner, balance=0):\n"
            "        \n\n"
            "    def deposit(self, amount):\n"
            "        \n\n"
            "    def withdraw(self, amount):\n"
            "        \n"
        ),
        solution=(
            "class BankAccount:\n"
            "    def __init__(self, owner, balance=0):\n"
            "        self.owner = owner\n"
            "        self.balance = balance\n\n"
            "    def deposit(self, amount):\n"
            "        self.balance += amount\n"
            "        return self.balance\n\n"
            "    def withdraw(self, amount):\n"
            "        if amount > self.balance:\n"
            "            return False\n"
            "        self.balance -= amount\n"
            "        return True\n\n\n"
            "def make_account(owner, balance=0):\n"
            "    return BankAccount(owner, balance)\n\n\n"
            "def try_withdraw(balance, amount):\n"
            "    account = BankAccount('test', balance)\n"
            "    ok = account.withdraw(amount)\n"
            "    return [ok, account.balance]\n"
        ),
        checks=[
            {
                "kind": "source",
                "must_contain": [r"class\s+BankAccount", r"def\s+__init__", r"def\s+deposit", r"def\s+withdraw"],
                "describe": "Defines BankAccount with the three methods",
                "label": "Class and methods exist",
            },
            {
                "kind": "call",
                "func": "try_withdraw",
                "args": [100, 30],
                "expect": [True, 70],
                "label": "Withdrawing 30 from 100 leaves 70",
            },
            {
                "kind": "call",
                "func": "try_withdraw",
                "args": [50, 80],
                "expect": [False, 50],
                "label": "Overdrawing is refused and balance is untouched",
            },
            {
                "kind": "call",
                "func": "try_withdraw",
                "args": [40, 40],
                "expect": [True, 0],
                "label": "Withdrawing the exact balance works",
            },
        ],
        hints=[
            "The starter includes helper functions the checks call - leave them in place.",
            "In __init__, save the arguments onto self.",
            "In withdraw, compare amount to self.balance before changing anything.",
        ],
    ),
    Lesson(
        slug="inheritance",
        title="Building on What Exists",
        goal="Extend a class and control how objects print.",
        minutes=18,
        xp=40,
        concept="""
<p>A class can <strong>inherit</strong> from another, getting all its behaviour and
adding or replacing pieces:</p>
<pre><code>class Animal:
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "meow"</code></pre>
<p>Call the parent's version with <code>super()</code> - especially in
<code>__init__</code>, so the parent's setup still runs.</p>
<p><code>__str__</code> decides what <code>print(obj)</code> shows.  Without it
you get an unhelpful <code>&lt;Cat object at 0x7f...&gt;</code>.</p>
""",
        example=(
            "class Shape:\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n\n"
            "    def area(self):\n"
            "        return 0\n\n"
            "    def __str__(self):\n"
            '        return f"{self.name} with area {self.area()}"\n\n\n'
            "class Square(Shape):\n"
            "    def __init__(self, side):\n"
            '        super().__init__("square")\n'
            "        self.side = side\n\n"
            "    def area(self):\n"
            "        return self.side ** 2\n\n\n"
            "print(Square(4))"
        ),
        brief=(
            "Given the <code>Vehicle</code> class in the starter, add a "
            "<code>Bicycle</code> subclass whose <code>wheels</code> is 2 and whose "
            "<code>describe()</code> returns <code>\"A bicycle with 2 wheels\"</code>. "
            "Keep <code>Vehicle</code>'s constructor working via <code>super()</code>."
        ),
        starter=(
            "class Vehicle:\n"
            "    wheels = 4\n\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n\n"
            "    def describe(self):\n"
            '        return f"A {self.name} with {self.wheels} wheels"\n\n\n'
            "class Bicycle(Vehicle):\n"
            "    \n\n\n"
            "def describe_bike():\n"
            '    return Bicycle().describe()\n\n\n'
            "def describe_car():\n"
            '    return Vehicle("car").describe()\n'
        ),
        solution=(
            "class Vehicle:\n"
            "    wheels = 4\n\n"
            "    def __init__(self, name):\n"
            "        self.name = name\n\n"
            "    def describe(self):\n"
            '        return f"A {self.name} with {self.wheels} wheels"\n\n\n'
            "class Bicycle(Vehicle):\n"
            "    wheels = 2\n\n"
            "    def __init__(self):\n"
            '        super().__init__("bicycle")\n\n\n'
            "def describe_bike():\n"
            '    return Bicycle().describe()\n\n\n'
            "def describe_car():\n"
            '    return Vehicle("car").describe()\n'
        ),
        checks=[
            {
                "kind": "call",
                "func": "describe_bike",
                "args": [],
                "expect": "A bicycle with 2 wheels",
                "label": "Bicycle describes itself",
            },
            {
                "kind": "call",
                "func": "describe_car",
                "args": [],
                "expect": "A car with 4 wheels",
                "label": "Vehicle still works",
            },
            {
                "kind": "source",
                "must_contain": [r"class\s+Bicycle\s*\(\s*Vehicle\s*\)", r"super\(\)"],
                "describe": "Bicycle inherits from Vehicle and calls super()",
                "label": "Uses inheritance and super()",
            },
        ],
        hints=[
            "Override the class attribute by writing wheels = 2 inside Bicycle.",
            "Bicycle's __init__ takes no arguments but must still set the name.",
            'super().__init__("bicycle") passes the name up to Vehicle.',
        ],
    ),
    Lesson(
        slug="recursion",
        title="Functions That Call Themselves",
        goal="Solve a problem by shrinking it.",
        minutes=18,
        xp=40,
        concept="""
<p>A <strong>recursive</strong> function calls itself on a smaller version of the
problem. Every one needs two parts:</p>
<ul>
  <li>a <strong>base case</strong> - the smallest input, answered directly</li>
  <li>a <strong>recursive case</strong> - which must move towards the base case</li>
</ul>
<p>Miss the base case and you get a <code>RecursionError</code>: the function
never stops calling itself.</p>
<pre><code>def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)</code></pre>
<p>Recursion shines on nested structures - folders inside folders, trees, nested
lists - where loops get awkward.</p>
""",
        example=(
            "def count_down(n):\n"
            "    if n == 0:\n"
            '        return ["liftoff"]\n'
            "    return [n] + count_down(n - 1)\n\n\n"
            "print(count_down(3))"
        ),
        brief=(
            "Write <code>deep_sum(items)</code> that adds up all the numbers in a list "
            "that may contain other lists, nested to any depth. "
            "<code>deep_sum([1, [2, [3, 4]], 5])</code> gives <code>15</code>."
        ),
        starter="def deep_sum(items):\n    \n",
        solution=(
            "def deep_sum(items):\n"
            "    total = 0\n"
            "    for item in items:\n"
            "        if isinstance(item, list):\n"
            "            total += deep_sum(item)\n"
            "        else:\n"
            "            total += item\n"
            "    return total\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "deep_sum",
                "args": [[1, [2, [3, 4]], 5]],
                "expect": 15,
                "label": "Nested three deep",
            },
            {"kind": "call", "func": "deep_sum", "args": [[1, 2, 3]], "expect": 6, "label": "Flat list"},
            {"kind": "call", "func": "deep_sum", "args": [[]], "expect": 0, "label": "Empty list"},
            {
                "kind": "call",
                "func": "deep_sum",
                "args": [[[[[7]]]]],
                "expect": 7,
                "label": "Deeply buried single value",
            },
        ],
        hints=[
            "isinstance(item, list) tells you whether to recurse.",
            "The base case is simply reaching the end of the loop with no lists left.",
            "Add deep_sum(item) for lists, and item itself for numbers.",
        ],
    ),
    Lesson(
        slug="higher-order",
        title="Functions as Values",
        goal="Pass functions around and sort by custom rules.",
        minutes=16,
        xp=40,
        concept="""
<p>In Python a function is just another value. You can store it in a variable and
hand it to another function - no brackets, because you are passing the function
itself, not calling it.</p>
<p><code>sorted()</code> takes a <code>key</code> function that says what to sort
<em>by</em>:</p>
<pre><code>people = [("Ada", 36), ("Alan", 41)]
by_age = sorted(people, key=lambda person: person[1])</code></pre>
<p><code>lambda</code> makes a small unnamed function inline. Keep them to a single
short expression; anything bigger deserves a real <code>def</code> with a name.</p>
""",
        example=(
            'words = ["banana", "fig", "cherry"]\n\n'
            "print(sorted(words, key=len))\n"
            "print(sorted(words, key=lambda w: w[-1]))\n"
            "print(list(filter(lambda w: len(w) > 3, words)))"
        ),
        brief=(
            "Write <code>rank(players)</code> where players is a list of "
            "<code>(name, score)</code> tuples. Return the names sorted by score "
            "highest first, breaking ties alphabetically by name."
        ),
        starter="def rank(players):\n    \n",
        solution=(
            "def rank(players):\n"
            "    ordered = sorted(players, key=lambda p: (-p[1], p[0]))\n"
            "    return [name for name, _ in ordered]\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "rank",
                "args": [[["Ada", 10], ["Alan", 30], ["Grace", 20]]],
                "expect": ["Alan", "Grace", "Ada"],
                "label": "Sorts by score descending",
            },
            {
                "kind": "call",
                "func": "rank",
                "args": [[["Zoe", 5], ["Amy", 5]]],
                "expect": ["Amy", "Zoe"],
                "label": "Ties break alphabetically",
            },
            {"kind": "call", "func": "rank", "args": [[]], "expect": [], "label": "No players"},
            {
                "kind": "call",
                "func": "rank",
                "args": [[["Solo", 1]]],
                "expect": ["Solo"],
                "label": "One player",
            },
        ],
        hints=[
            "A key can return a tuple - Python compares the first element, then the second.",
            "Negating the score turns a descending sort into an ascending one.",
            "key=lambda p: (-p[1], p[0])",
        ],
    ),
    Lesson(
        slug="algorithms",
        title="Search and Efficiency",
        goal="Understand why binary search beats scanning.",
        minutes=20,
        xp=45,
        concept="""
<p>Checking every item in a list of a million takes a million steps - that is
<strong>linear</strong> time, written O(n).</p>
<p>If the list is <strong>already sorted</strong> you can do far better. Look at
the middle: too big, throw away the right half; too small, throw away the left.
Each step halves what is left, so a million items takes about 20 steps. That is
<strong>logarithmic</strong> time, O(log n).</p>
<p>The classic bug is the loop condition. Use <code>while low &lt;= high</code>,
and always move <code>low</code> or <code>high</code> past <code>mid</code>, or
you will loop forever on a missing value.</p>
""",
        example=(
            "def linear_search(items, target):\n"
            "    for index, item in enumerate(items):\n"
            "        if item == target:\n"
            "            return index\n"
            "    return -1\n\n\n"
            "print(linear_search([4, 8, 15, 16], 15))"
        ),
        brief=(
            "Write <code>binary_search(items, target)</code> for a sorted list. Return "
            "the index of <code>target</code>, or <code>-1</code> if it is not there. "
            "Halve the range each step - do not just scan."
        ),
        starter=(
            "def binary_search(items, target):\n"
            "    low = 0\n"
            "    high = len(items) - 1\n"
            "    \n"
            "    return -1\n"
        ),
        solution=(
            "def binary_search(items, target):\n"
            "    low = 0\n"
            "    high = len(items) - 1\n"
            "    while low <= high:\n"
            "        mid = (low + high) // 2\n"
            "        if items[mid] == target:\n"
            "            return mid\n"
            "        if items[mid] < target:\n"
            "            low = mid + 1\n"
            "        else:\n"
            "            high = mid - 1\n"
            "    return -1\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "binary_search",
                "args": [[1, 3, 5, 7, 9, 11], 7],
                "expect": 3,
                "label": "Finds a value in the middle",
            },
            {
                "kind": "call",
                "func": "binary_search",
                "args": [[1, 3, 5, 7, 9, 11], 1],
                "expect": 0,
                "label": "Finds the first value",
            },
            {
                "kind": "call",
                "func": "binary_search",
                "args": [[1, 3, 5, 7, 9, 11], 11],
                "expect": 5,
                "label": "Finds the last value",
            },
            {
                "kind": "call",
                "func": "binary_search",
                "args": [[1, 3, 5, 7, 9, 11], 4],
                "expect": -1,
                "label": "Missing value returns -1",
            },
            {"kind": "call", "func": "binary_search", "args": [[], 5], "expect": -1, "label": "Empty list"},
            {
                "kind": "source",
                "must_contain": [r"\bmid\b|//\s*2"],
                "describe": "Halves the search range",
                "label": "Actually halves the range",
            },
        ],
        hints=[
            "mid = (low + high) // 2 finds the middle index.",
            "If the middle is too small, the answer is to its right: low = mid + 1.",
            "Loop while low <= high, and return -1 once the range is empty.",
        ],
    ),
    Lesson(
        slug="data-shapes",
        title="Modelling Real Data",
        goal="Reshape records the way real applications do.",
        minutes=20,
        xp=45,
        concept="""
<p>Most professional Python is data wrangling: you receive records in one shape
and need them in another.</p>
<p>A common job is <strong>grouping</strong>: turn a flat list of records into a
dictionary keyed by some field. The pattern is always the same - walk the
records, work out the key, and append into a list you create on first sight of
that key.</p>
<p><code>dict.setdefault(key, [])</code> does that in one step: it returns the
existing list, or inserts a new empty one and returns that.</p>
""",
        example=(
            "records = [\n"
            '    {"name": "Ada", "house": "red"},\n'
            '    {"name": "Alan", "house": "blue"},\n'
            '    {"name": "Grace", "house": "red"},\n'
            "]\n\n"
            "groups = {}\n"
            "for record in records:\n"
            '    groups.setdefault(record["house"], []).append(record["name"])\n\n'
            "print(groups)"
        ),
        brief=(
            "Write <code>group_by_subject(results)</code>. Each result is a dict with "
            "<code>student</code>, <code>subject</code> and <code>mark</code>. Return a "
            "dict mapping each subject to the <em>average</em> mark, rounded to one "
            "decimal place."
        ),
        starter="def group_by_subject(results):\n    \n",
        solution=(
            "def group_by_subject(results):\n"
            "    marks = {}\n"
            "    for result in results:\n"
            '        marks.setdefault(result["subject"], []).append(result["mark"])\n'
            "    return {\n"
            "        subject: round(sum(values) / len(values), 1)\n"
            "        for subject, values in marks.items()\n"
            "    }\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "group_by_subject",
                "args": [
                    [
                        {"student": "Ada", "subject": "maths", "mark": 90},
                        {"student": "Alan", "subject": "maths", "mark": 80},
                        {"student": "Grace", "subject": "art", "mark": 70},
                    ]
                ],
                "expect": {"maths": 85.0, "art": 70.0},
                "label": "Averages each subject",
            },
            {
                "kind": "call",
                "func": "group_by_subject",
                "args": [[]],
                "expect": {},
                "label": "No results",
            },
            {
                "kind": "call",
                "func": "group_by_subject",
                "args": [
                    [
                        {"student": "A", "subject": "sci", "mark": 10},
                        {"student": "B", "subject": "sci", "mark": 15},
                        {"student": "C", "subject": "sci", "mark": 12},
                    ]
                ],
                "expect": {"sci": 12.3},
                "label": "Rounds to one decimal place",
            },
        ],
        hints=[
            "First collect every mark per subject into a list.",
            "setdefault(subject, []).append(mark) does the grouping in one line.",
            "Then average each list with round(sum(v) / len(v), 1).",
        ],
    ),
    Lesson(
        slug="testing",
        title="Proving Your Code Works",
        goal="Write tests that catch your own mistakes.",
        minutes=18,
        xp=45,
        concept="""
<p>"It worked when I tried it" is not evidence. A <strong>test</strong> is code
that checks other code, so you find out immediately when a change breaks
something.</p>
<p>The simplest form is <code>assert</code>: it does nothing if the condition is
true, and raises <code>AssertionError</code> if it is false.</p>
<pre><code>assert add(2, 2) == 4, "adding two and two"</code></pre>
<p>Good tests cover three kinds of case: the ordinary one, the
<strong>edge</strong> cases (empty, zero, one item, the boundary value), and the
error cases. Most bugs live at the edges - which is exactly where the checks in
this course have been aiming all along.</p>
""",
        example=(
            "def average(numbers):\n"
            "    if not numbers:\n"
            "        return 0\n"
            "    return sum(numbers) / len(numbers)\n\n\n"
            "assert average([2, 4]) == 3\n"
            "assert average([]) == 0\n"
            'print("all tests passed")'
        ),
        brief=(
            "Fix the buggy <code>median()</code> in the starter so it handles "
            "even-length lists (average of the middle two), odd-length lists, and an "
            "empty list (return <code>None</code>). Then add at least three "
            "<code>assert</code> statements of your own."
        ),
        starter=(
            "def median(numbers):\n"
            "    ordered = sorted(numbers)\n"
            "    middle = len(ordered) // 2\n"
            "    return ordered[middle]  # bug: even lengths and empty lists are wrong\n\n\n"
            "# Add your assert statements below\n"
        ),
        solution=(
            "def median(numbers):\n"
            "    ordered = sorted(numbers)\n"
            "    count = len(ordered)\n"
            "    if count == 0:\n"
            "        return None\n"
            "    middle = count // 2\n"
            "    if count % 2 == 1:\n"
            "        return ordered[middle]\n"
            "    return (ordered[middle - 1] + ordered[middle]) / 2\n\n\n"
            "assert median([3, 1, 2]) == 2\n"
            "assert median([4, 1, 3, 2]) == 2.5\n"
            "assert median([]) is None\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "median",
                "args": [[3, 1, 2]],
                "expect": 2,
                "label": "Odd length",
            },
            {
                "kind": "call",
                "func": "median",
                "args": [[4, 1, 3, 2]],
                "expect": 2.5,
                "label": "Even length averages the middle two",
            },
            {"kind": "call", "func": "median", "args": [[]], "expect": None, "label": "Empty list is None"},
            {
                "kind": "call",
                "func": "median",
                "args": [[9]],
                "expect": 9,
                "label": "Single item",
            },
            {
                "kind": "source",
                "must_contain": [r"assert[\s\S]*assert[\s\S]*assert"],
                "describe": "Includes at least three assert statements",
                "label": "You wrote three tests",
            },
        ],
        hints=[
            "Handle the empty list before touching any index.",
            "len(ordered) % 2 tells you whether the length is odd.",
            "For even lengths average ordered[middle - 1] and ordered[middle].",
        ],
    ),
    Lesson(
        slug="library-project",
        title="Project: Library System",
        goal="Design a small system from scratch, with state and rules.",
        minutes=30,
        xp=70,
        concept="""
<p>The final project pulls together classes, dictionaries, error handling and
careful edge cases.</p>
<p>You are modelling a library. Books can be borrowed and returned, and the system
must never lose track of a copy. Think about the rules before you write code:
what happens if somebody borrows the last copy? Returns a book they never took?
Borrows an unknown title?</p>
<p>Deciding those rules first - and writing them down as checks - is the actual
skill of software design. The code is the easy part.</p>
""",
        example=(
            "class Library:\n"
            "    def __init__(self, stock):\n"
            "        self.stock = dict(stock)\n\n"
            "    def borrow(self, title):\n"
            "        if self.stock.get(title, 0) <= 0:\n"
            "            return False\n"
            "        self.stock[title] -= 1\n"
            "        return True"
        ),
        brief=(
            "Complete <code>Library</code> in the starter. <code>borrow(title)</code> "
            "returns <code>True</code> and reduces stock, or <code>False</code> if the "
            "title is unknown or out of copies. <code>give_back(title)</code> returns "
            "<code>True</code> and increases stock, or <code>False</code> for an unknown "
            "title. <code>available()</code> returns a sorted list of titles with at "
            "least one copy."
        ),
        starter=(
            "class Library:\n"
            "    def __init__(self, stock):\n"
            "        self.stock = dict(stock)\n\n"
            "    def borrow(self, title):\n"
            "        \n\n"
            "    def give_back(self, title):\n"
            "        \n\n"
            "    def available(self):\n"
            "        \n\n\n"
            "# Helpers used by the checks - leave these in place.\n"
            "def run(stock, actions):\n"
            "    library = Library(stock)\n"
            "    outcomes = []\n"
            "    for action, title in actions:\n"
            "        outcomes.append(getattr(library, action)(title))\n"
            "    return [outcomes, library.available()]\n"
        ),
        solution=(
            "class Library:\n"
            "    def __init__(self, stock):\n"
            "        self.stock = dict(stock)\n\n"
            "    def borrow(self, title):\n"
            "        if self.stock.get(title, 0) <= 0:\n"
            "            return False\n"
            "        self.stock[title] -= 1\n"
            "        return True\n\n"
            "    def give_back(self, title):\n"
            "        if title not in self.stock:\n"
            "            return False\n"
            "        self.stock[title] += 1\n"
            "        return True\n\n"
            "    def available(self):\n"
            "        return sorted(t for t, n in self.stock.items() if n > 0)\n\n\n"
            "# Helpers used by the checks - leave these in place.\n"
            "def run(stock, actions):\n"
            "    library = Library(stock)\n"
            "    outcomes = []\n"
            "    for action, title in actions:\n"
            "        outcomes.append(getattr(library, action)(title))\n"
            "    return [outcomes, library.available()]\n"
        ),
        checks=[
            {
                "kind": "call",
                "func": "run",
                "args": [{"Dune": 2, "Emma": 1}, [["borrow", "Dune"]]],
                "expect": [[True], ["Dune", "Emma"]],
                "label": "Borrowing one of two copies",
            },
            {
                "kind": "call",
                "func": "run",
                "args": [{"Dune": 1}, [["borrow", "Dune"], ["borrow", "Dune"]]],
                "expect": [[True, False], []],
                "label": "Cannot borrow the last copy twice",
            },
            {
                "kind": "call",
                "func": "run",
                "args": [{"Dune": 1}, [["borrow", "Hamlet"]]],
                "expect": [[False], ["Dune"]],
                "label": "Unknown title cannot be borrowed",
            },
            {
                "kind": "call",
                "func": "run",
                "args": [{"Dune": 1}, [["borrow", "Dune"], ["give_back", "Dune"]]],
                "expect": [[True, True], ["Dune"]],
                "label": "Returning restores the copy",
            },
            {
                "kind": "call",
                "func": "run",
                "args": [{"Dune": 1}, [["give_back", "Hamlet"]]],
                "expect": [[False], ["Dune"]],
                "label": "Unknown title cannot be returned",
            },
        ],
        hints=[
            "self.stock.get(title, 0) treats an unknown title as zero copies.",
            "give_back must reject unknown titles, so check 'title not in self.stock'.",
            "available() filters for counts above zero, then sorts the titles.",
        ],
    ),
]

TRACK = Track(
    slug="creators",
    title="Creators",
    tagline="Think like a software engineer.",
    ages="Ages 16-18",
    emoji="\N{ROCKET}",
    blurb=(
        "Classes, inheritance, recursion, algorithms and testing. The concepts "
        "that carry straight into A-level, university and real codebases."
    ),
    lessons=LESSONS,
)
