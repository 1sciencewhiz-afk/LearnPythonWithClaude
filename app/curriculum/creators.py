"""Creators track - typically ages 16-18, heading towards real engineering."""
from __future__ import annotations

from .schema import GlossaryTerm, Lesson, Track

LESSONS = [
    Lesson(
        slug="classes",
        title="Designing Your Own Types",
        goal="Bundle data and behaviour together in a class.",
        minutes=18,
        xp=40,
        concept="""
<p>A <strong>class</strong> is a blueprint. It describes what an object knows (its
<strong>attributes</strong>) and what it can do (its <strong>methods</strong>).
Creating an object from a class is called <strong>instantiating</strong> it, and
the object itself is called an <strong>instance</strong> of that class.</p>
<pre><code>class Dog:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} says woof"</code></pre>
<p><code>__init__</code> runs when you create an instance and sets it up.
<code>self</code> is the particular object being worked on - it is the first
parameter of every method, and Python passes it for you automatically, so you
never write it in the call, only in the definition.</p>
<p>Reach for a class when several pieces of data always travel together and have
operations that belong to them. Otherwise a plain function is usually better -
not everything needs to be a class, and forcing one on a problem that is really
just a calculation adds ceremony without adding clarity.</p>
<h4>Why this matters</h4>
<p>Classes are how you model "things" in code: a bank account, a player, a book.
Bundling the data (balance, owner) with the operations that are allowed on it
(deposit, withdraw) keeps related code together and makes it much harder for
another part of the program to put the object into an invalid state by
accident.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting <code>self</code> as the first parameter of a method, or
      forgetting to write <code>self.</code> before an attribute inside a
      method - without it, Python treats the name as a local variable that
      disappears when the method ends.</li>
  <li>Confusing the class itself with an instance of it - <code>BankAccount</code>
      is the blueprint; <code>BankAccount("Sam")</code> is one actual account
      built from it.</li>
  <li>Writing logic in <code>__init__</code> that belongs in a proper method -
      <code>__init__</code> should just set up the starting attributes.</li>
</ul>
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
        glossary=[
            GlossaryTerm(
                "class",
                "A blueprint for creating objects, describing the attributes they "
                "hold and the methods they support.",
            ),
            GlossaryTerm(
                "object (instance)",
                "One concrete thing built from a class, e.g. BankAccount(\"Sam\") "
                "is an instance of the BankAccount class.",
            ),
            GlossaryTerm(
                "self",
                "The first parameter of every method, standing for the particular "
                "instance the method was called on. Python supplies it automatically.",
            ),
            GlossaryTerm(
                "__init__()",
                "The method that runs automatically when a new instance is created, "
                "used to set up its starting attributes.",
            ),
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
adding or replacing pieces. The class being built on is the
<strong>parent</strong> (or base) class; the new one is the
<strong>subclass</strong>:</p>
<pre><code>class Animal:
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "meow"</code></pre>
<p>Call the parent's version with <code>super()</code> - especially in
<code>__init__</code>, so the parent's setup still runs before the subclass
adds its own. Overriding a method - giving it a new body in the subclass, as
<code>Cat</code> does with <code>speak</code> - is how a subclass changes
behaviour while keeping everything else from the parent.</p>
<p><code>__str__</code> decides what <code>print(obj)</code> shows.  Without it
you get an unhelpful <code>&lt;Cat object at 0x7f...&gt;</code>. Methods with
double underscores either side, like <code>__init__</code> and
<code>__str__</code>, are called <strong>dunder methods</strong> ("double
underscore") and are Python's way of plugging your class into built-in
behaviour like printing, equality checks and more.</p>
<h4>Why this matters</h4>
<p>Inheritance avoids repeating the shared behaviour of similar things.
Different vehicle types share a lot of behaviour (they all have wheels and can
be described); inheritance lets you write that once in <code>Vehicle</code> and
only write what is genuinely different in each subclass.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Overriding <code>__init__</code> in a subclass and forgetting to call
      <code>super().__init__(...)</code> - the parent's setup code never runs,
      so attributes it would have set are missing.</li>
  <li>Reaching for inheritance when the relationship is not really "is a kind
      of" - a <code>Car</code> is a kind of <code>Vehicle</code>, but an
      <code>Engine</code> is not; it belongs <em>inside</em> a car instead.</li>
  <li>Forgetting that overriding a method completely replaces it unless you
      explicitly call <code>super().method_name()</code> inside the override.</li>
</ul>
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
        glossary=[
            GlossaryTerm(
                "inheritance",
                "A class taking on the attributes and methods of another (its "
                "parent), then adding or overriding some of its own.",
            ),
            GlossaryTerm(
                "subclass",
                "A class that inherits from another, written as "
                "class Child(Parent):.",
            ),
            GlossaryTerm(
                "super()",
                "Refers to the parent class from inside a subclass, most often used "
                "to call the parent's __init__ so its setup still runs.",
            ),
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
  <li>a <strong>base case</strong> - the smallest input, answered directly, with
      no further recursive call</li>
  <li>a <strong>recursive case</strong> - which must move towards the base case,
      by working on a smaller piece of the problem each time</li>
</ul>
<p>Miss the base case and you get a <code>RecursionError</code>: the function
never stops calling itself, because nothing ever tells it to stop.</p>
<pre><code>def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)</code></pre>
<p>Recursion shines on nested structures - folders inside folders, trees, nested
lists - where loops get awkward, because you do not know in advance how many
levels deep you will need to go. A loop has to guess that in advance; a
recursive function just keeps calling itself until it runs out of nesting.</p>
<h4>Why this matters</h4>
<p>Some problems are naturally defined in terms of themselves: a folder's total
size is the size of its files plus the total size of every folder inside it -
which is the exact same question, just smaller. Recursion lets you write the
code in the same shape as the definition, which is often far clearer than the
equivalent loop.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting the base case entirely, or writing one that is never actually
      reached because the recursive case does not shrink towards it.</li>
  <li>Shrinking the problem in the wrong direction, e.g. adding to <code>n</code>
      instead of subtracting from it.</li>
  <li>Doing real work <em>after</em> the recursive call when it needed to happen
      before, or the other way round - trace through a small example by hand if
      the order feels uncertain.</li>
</ul>
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
        glossary=[
            GlossaryTerm(
                "recursion",
                "A function solving a problem by calling itself on a smaller "
                "version of the same problem.",
            ),
            GlossaryTerm(
                "base case",
                "The smallest version of a recursive problem, answered directly "
                "with no further recursive call - without one, recursion never stops.",
            ),
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
itself, not calling it. A function that takes another function as an argument
(or returns one) is called a <strong>higher-order function</strong>;
<code>sorted()</code>, <code>filter()</code> and <code>map()</code> are all
examples from the standard library.</p>
<p><code>sorted()</code> takes a <code>key</code> function that says what to sort
<em>by</em>:</p>
<pre><code>people = [("Ada", 36), ("Alan", 41)]
by_age = sorted(people, key=lambda person: person[1])</code></pre>
<p><code>lambda</code> makes a small unnamed function inline. Keep them to a single
short expression; anything bigger deserves a real <code>def</code> with a name -
a lambda that needs a comment to explain it has outgrown being a lambda.</p>
<h4>Why this matters</h4>
<p>Sorting, filtering and transforming data "by some rule" is everywhere - sort
players by score, keep only the products in stock, apply a discount to every
price. Passing a small function in as the rule is far more flexible than
writing a separate, nearly-identical loop for every possible rule.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Writing <code>key=my_function()</code> with the brackets - that calls the
      function immediately and passes its result, instead of passing the
      function itself.</li>
  <li>Trying to cram a multi-step calculation, or a statement like
      <code>print</code>, into a lambda - lambdas can only contain a single
      expression.</li>
  <li>Forgetting that <code>sorted()</code> compares tuples element by element,
      so <code>key=lambda p: (-p[1], p[0])</code> means "by score descending,
      then by name" rather than something more complicated.</li>
</ul>
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
        glossary=[
            GlossaryTerm(
                "higher-order function",
                "A function that takes another function as an argument, or returns "
                "one, such as sorted(), filter() and map().",
            ),
            GlossaryTerm(
                "lambda",
                "A small, unnamed function written inline as lambda arguments: "
                "expression, limited to a single expression with no statements.",
            ),
        ],
    ),
    Lesson(
        slug="decorators",
        title="Wrapping Functions With Decorators",
        goal="Write a decorator that adds behaviour to a function without changing it.",
        minutes=18,
        xp=45,
        concept="""
<p>A <strong>decorator</strong> is a function that takes a function and returns
a new one that wraps it. The wrapper can run code before and after the
original, then hands back its result - the original never has to change.</p>
<p><code>@decorator_name</code> just above a <code>def</code> is shorthand for
<code>my_func = decorator_name(my_func)</code>. Inside the wrapper, use
<code>*args, **kwargs</code> to accept and forward any arguments, whatever the
wrapped function needs - <code>*args</code> collects any number of positional
arguments into a tuple, and <code>**kwargs</code> collects any keyword arguments
into a dictionary, so the wrapper works for a function with any signature at
all without needing to know it in advance.</p>
<h4>Why this matters</h4>
<p>Decorators let you add behaviour - logging, timing, access checks, caching -
to many functions without copying that code into every single one of them.
Python's own standard library and most popular frameworks use decorators
constantly, so recognising the <code>@name</code> syntax on sight is a genuinely
useful skill.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Forgetting to <code>return func(*args, **kwargs)</code> inside the
      wrapper - the wrapped function silently stops giving back a real result.</li>
  <li>Forgetting to <code>return wrapper</code> from the decorator itself, so
      the decorated name ends up bound to <code>None</code> instead of a
      working function.</li>
  <li>Adding attributes (like a counter) to the wrong function - they belong on
      <code>wrapper</code>, the function that actually gets called from now on,
      not on the original.</li>
</ul>
""",
        example=(
            "def shout(func):\n"
            "    def wrapper(*args, **kwargs):\n"
            "        result = func(*args, **kwargs)\n"
            "        return result.upper()\n"
            "    return wrapper\n\n\n"
            "@shout\n"
            "def greet(name):\n"
            '    return f"hello {name}"\n\n\n'
            'print(greet("ada"))'
        ),
        brief=(
            "Write a decorator <code>counted(func)</code> that gives the wrapped "
            "function a <code>.calls</code> attribute, starting at <code>0</code> and "
            "increasing by one on every call. Then write <code>ping_three_times()</code>: "
            "inside it, define <code>ping()</code> returning <code>\"pong\"</code>, "
            "decorate it with <code>@counted</code>, call it three times, and return "
            "<code>ping.calls</code>. Also write <code>shout_hello()</code>: define "
            "<code>hello()</code> returning <code>\"hi\"</code>, decorate it with "
            "<code>@counted</code>, and return the tuple "
            "<code>(hello(), hello.calls)</code>."
        ),
        starter=(
            "def counted(func):\n"
            "    def wrapper(*args, **kwargs):\n"
            "        \n"
            "    wrapper.calls = 0\n"
            "    return wrapper\n\n\n"
            "def ping_three_times():\n"
            "    \n\n\n"
            "def shout_hello():\n"
            "    \n"
        ),
        solution=(
            "def counted(func):\n"
            "    def wrapper(*args, **kwargs):\n"
            "        wrapper.calls += 1\n"
            "        return func(*args, **kwargs)\n"
            "    wrapper.calls = 0\n"
            "    return wrapper\n\n\n"
            "def ping_three_times():\n"
            "    @counted\n"
            "    def ping():\n"
            '        return "pong"\n\n'
            "    for _ in range(3):\n"
            "        ping()\n"
            "    return ping.calls\n\n\n"
            "def shout_hello():\n"
            "    @counted\n"
            "    def hello():\n"
            '        return "hi"\n\n'
            "    return hello(), hello.calls\n"
        ),
        checks=[
            {"kind": "call", "func": "ping_three_times", "args": [], "expect": 3, "label": "Counts three calls"},
            {
                "kind": "call",
                "func": "shout_hello",
                "args": [],
                "expect": ["hi", 1],
                "label": "Forwards the return value and counts once",
            },
            {
                "kind": "source",
                "must_contain": [r"@counted", r"\.calls"],
                "describe": "Uses @counted and reads .calls",
                "label": "Uses the decorator",
            },
        ],
        hints=[
            "wrapper.calls += 1 keeps a running total across calls.",
            "wrapper must still call func(*args, **kwargs) and return its result.",
            "Set the starting count straight after defining wrapper: wrapper.calls = 0",
        ],
        glossary=[
            GlossaryTerm(
                "decorator",
                "A function that takes a function and returns a wrapped version of "
                "it, applied with @decorator_name just above a def.",
            ),
            GlossaryTerm(
                "*args and **kwargs",
                "Catch-all parameters in a function definition: *args collects "
                "extra positional arguments into a tuple, **kwargs collects extra "
                "keyword arguments into a dictionary.",
            ),
        ],
    ),
    Lesson(
        slug="generators",
        title="Generators and yield",
        goal="Write a generator function that produces values lazily.",
        minutes=16,
        xp=40,
        concept="""
<p>A <strong>generator</strong> function looks like a normal function but uses
<code>yield</code> instead of <code>return</code>. Each <code>yield</code>
pauses the function and hands out one value; calling it again picks up right
where it left off, with all its local variables exactly as they were.</p>
<p>This means a generator can represent a huge - or endless - sequence without
ever building the whole thing in memory, which is what people mean by
<strong>lazy evaluation</strong>: each value is only produced at the moment it
is actually needed. Loop over it with <code>for</code>, or collect every value
at once with <code>list(...)</code> - though doing that for an endless
generator would never finish, which is exactly the situation generators are
built to avoid needing.</p>
<h4>Why this matters</h4>
<p>Sometimes you want "the next value" without ever holding "all the values" in
memory at once - reading a huge file line by line, generating an endless
sequence of test data, or streaming results as they are produced instead of
waiting for everything to finish. Generators are Python's tool for exactly that
shape of problem.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Using <code>return</code> instead of <code>yield</code> by habit - that
      turns the function back into a normal one that gives a single value,
      rather than a generator.</li>
  <li>Trying to index into a generator like a list, e.g.
      <code>even_numbers(10)[0]</code> - generators only support being stepped
      through in order, not jumped into directly.</li>
  <li>Calling <code>list()</code> on a generator that never stops, which will
      hang forever trying to collect every value first.</li>
</ul>
""",
        example=(
            "def countdown(n):\n"
            "    while n > 0:\n"
            "        yield n\n"
            "        n -= 1\n\n\n"
            "for number in countdown(3):\n"
            "    print(number)\n\n"
            "print(list(countdown(3)))"
        ),
        brief=(
            "Write a generator function <code>even_numbers(limit)</code> that yields "
            "every even number from <code>0</code> up to (but not including) "
            "<code>limit</code>, in order. Then write "
            "<code>even_numbers_list(limit)</code> that returns "
            "<code>list(even_numbers(limit))</code>."
        ),
        starter=(
            "def even_numbers(limit):\n"
            "    \n\n\n"
            "def even_numbers_list(limit):\n"
            "    return list(even_numbers(limit))\n"
        ),
        solution=(
            "def even_numbers(limit):\n"
            "    for n in range(limit):\n"
            "        if n % 2 == 0:\n"
            "            yield n\n\n\n"
            "def even_numbers_list(limit):\n"
            "    return list(even_numbers(limit))\n"
        ),
        checks=[
            {"kind": "call", "func": "even_numbers_list", "args": [10], "expect": [0, 2, 4, 6, 8], "label": "Evens below 10"},
            {"kind": "call", "func": "even_numbers_list", "args": [1], "expect": [0], "label": "Zero counts as even"},
            {"kind": "call", "func": "even_numbers_list", "args": [0], "expect": [], "label": "Empty range"},
            {"kind": "call", "func": "even_numbers_list", "args": [7], "expect": [0, 2, 4, 6], "label": "Stops before the limit"},
            {
                "kind": "source",
                "must_contain": [r"\byield\b"],
                "describe": "Uses yield to make a generator",
                "label": "Uses yield",
            },
        ],
        hints=[
            "Loop through range(limit) and check n % 2 == 0.",
            "Use yield, not return, or it will not be a generator.",
            "for n in range(limit):\\n    if n % 2 == 0:\\n        yield n",
        ],
        glossary=[
            GlossaryTerm(
                "generator",
                "A function that uses yield to produce values one at a time, "
                "pausing between each one instead of building a full list upfront.",
            ),
            GlossaryTerm(
                "yield",
                "Pauses a generator function and hands out one value; the function "
                "resumes from that exact point the next time a value is requested.",
            ),
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
<strong>linear</strong> time, written <strong>O(n)</strong>. This notation, called
<strong>Big O</strong>, describes how the amount of work grows as the input
grows, ignoring constant details like exactly how fast the computer is - it
answers "if the list gets ten times bigger, how much slower does this get?"</p>
<p>If the list is <strong>already sorted</strong> you can do far better. Look at
the middle: too big, throw away the right half; too small, throw away the left.
Each step halves what is left, so a million items takes about 20 steps. That is
<strong>logarithmic</strong> time, O(log n) - doubling the input only adds one
more step, rather than doubling the work.</p>
<p>The classic bug is the loop condition. Use <code>while low &lt;= high</code>,
and always move <code>low</code> or <code>high</code> past <code>mid</code>, or
you will loop forever on a missing value.</p>
<h4>Why this matters</h4>
<p>The same correct answer can come back in a fraction of a second or take
minutes, purely because of which algorithm was used - this is the difference
between an app that feels instant and one that feels broken, once the amount of
data gets large. Binary search is the simplest possible example of an algorithm
that is dramatically faster than the obvious one, and the reasoning behind it
(cut the problem in half every step) reappears throughout computer science.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Running binary search on a list that is not actually sorted - the
      halving logic silently gives wrong answers instead of an error.</li>
  <li>Using <code>low &lt; high</code> instead of <code>low &lt;= high</code>,
      which misses the case where only one candidate is left.</li>
  <li>Forgetting to move <code>low</code> or <code>high</code> on every round,
      which leaves the range unchanged and loops forever.</li>
</ul>
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
        glossary=[
            GlossaryTerm(
                "Big O notation",
                "A way of describing how an algorithm's work grows as its input "
                "grows, e.g. O(n) for linear, O(log n) for logarithmic.",
            ),
            GlossaryTerm(
                "binary search",
                "A search algorithm that repeatedly halves a sorted list's search "
                "range, finding an item in O(log n) steps instead of scanning it all.",
            ),
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
existing list for that key, or inserts a new empty one and returns that -
either way you get a list back that you can immediately <code>.append()</code>
to, without writing an <code>if key not in dict</code> check yourself.</p>
<h4>Why this matters</h4>
<p>Data almost never arrives in exactly the shape you need it in. A spreadsheet
export, an API response, a database query result - all typically come back as a
flat list of records, and turning that into "totals per category" or "records
grouped by owner" is one of the single most common things real code does with
data.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Using <code>dict[key].append(...)</code> directly on a key that might not
      exist yet, which raises a <code>KeyError</code> - <code>setdefault</code>
      or <code>.get(key, [])</code> sidesteps this.</li>
  <li>Grouping correctly but forgetting the second step - turning each group's
      raw list of values into the actual summary the brief asked for, such as
      an average.</li>
  <li>Rounding at the wrong point, e.g. rounding each mark before averaging
      instead of rounding the final average.</li>
</ul>
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
        glossary=[
            GlossaryTerm(
                "setdefault()",
                "A dictionary method that returns a key's existing value, or "
                "inserts and returns a given default if the key is missing - handy "
                "for building up groups.",
            ),
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
something - including changes you make months later, once you have forgotten
exactly how the function works.</p>
<p>The simplest form is <code>assert</code>: it does nothing if the condition is
true, and raises <code>AssertionError</code> if it is false.</p>
<pre><code>assert add(2, 2) == 4, "adding two and two"</code></pre>
<p>Good tests cover three kinds of case: the ordinary one, the
<strong>edge cases</strong> (empty, zero, one item, the boundary value), and the
error cases. Most bugs live at the edges - which is exactly where the checks in
this course have been aiming all along, and exactly why so many briefs in this
course have specifically asked about empty lists and boundary values.</p>
<h4>Why this matters</h4>
<p>Every lesson in this course has been graded by exactly this technique: a set
of <code>assert</code>-like checks written before (or instead of) trusting that
the code "looks right". Writing your own tests is how you get that same safety
net for code nobody else has already checked for you.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Only testing the case you already know works, rather than the edge cases
      most likely to expose a real bug.</li>
  <li>Writing a test that depends on something changeable, like the current
      date or a random number, so it passes sometimes and fails other times for
      no reason connected to the code being wrong.</li>
  <li>Fixing the bug the test happened to catch without asking whether the same
      mistake exists anywhere else in the function.</li>
</ul>
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
        glossary=[
            GlossaryTerm(
                "assert",
                "A statement that does nothing if its condition is True, and raises "
                "an AssertionError if it is False - the simplest way to write a test.",
            ),
            GlossaryTerm(
                "edge case",
                "An unusual or boundary input - empty, zero, one item, the largest "
                "or smallest allowed value - where bugs are most likely to hide.",
            ),
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
skill of software design. The code is the easy part. Notice, too, that the
<code>Library</code> class keeps its stock as a private implementation detail:
nothing outside the class edits <code>self.stock</code> directly, every change
goes through <code>borrow</code> or <code>give_back</code>, which is what
enforces the rules. Hiding the data behind methods like this is called
<strong>encapsulation</strong>, and it is the same idea the very first classes
lesson introduced with <code>BankAccount</code>.</p>
<h4>Why this matters</h4>
<p>This project has no single new idea to introduce - it is where classes,
dictionaries, edge cases and careful rule-writing from every earlier lesson in
this track come together into one small but complete system, which is exactly
what building real software feels like.</p>
<h4>Common mistakes</h4>
<ul>
  <li>Checking <code>title in self.stock</code> without also checking the
      count is above zero, which lets a title with 0 copies be borrowed.</li>
  <li>Forgetting that <code>give_back</code> must still reject an unknown
      title, even though it is adding a copy rather than removing one.</li>
  <li>Changing <code>self.stock</code> before confirming the action is valid,
      which can leave it changed even when the method should have returned
      <code>False</code> and done nothing.</li>
</ul>
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
        glossary=[
            GlossaryTerm(
                "encapsulation",
                "Hiding an object's data behind its methods, so outside code changes "
                "it only through rules the object enforces, never directly.",
            ),
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
