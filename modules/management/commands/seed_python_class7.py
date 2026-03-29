"""Seed Class 7 Python course module into the database."""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from modules.models import Module, Section, Concept, QuizQuestion, PracticalExercise


PYTHON_MODULE = {
    'order': 14,
    'title': 'Python for Beginners',
    'subtitle': 'Learn Python from scratch — variables, loops, functions, and your first programs.',
    'description': 'Python basics: variables, data types, input/output, conditions, loops, functions, lists, and simple projects. Built for Class 7 students with zero coding experience.',
    'difficulty': 'beginner',
    'tag': 'practical',
    'icon': '🐍',
    'color': '#9EC6F3',
    'estimated_time': 120,
    'grade_level': '7',
    'prerequisites': 'Basic computer usage (typing, browser)',
    'learning_objectives': (
        'Write and run your first Python program\n'
        'Understand variables and data types\n'
        'Use if/else conditions\n'
        'Write for and while loops\n'
        'Define and call functions\n'
        'Work with lists and dictionaries\n'
        'Build a simple mini-project'
    ),
    'sections': [
        {
            'order': 1,
            'title': 'Your First Python Program',
            'content_md': """# Hello, Python!

Python is one of the most popular programming languages in the world — and the easiest to start with.

## Why Python?
- Simple, readable syntax (almost like English)
- Used in AI, web development, data science, automation
- Free and works on any computer

## Your First Program

```python
print("Hello, World!")
```

Run this and Python will display: `Hello, World!`

The `print()` function displays text on the screen. The text inside the quotes is called a **string**.

## Try It Yourself
```python
print("My name is Arjun")
print("I am learning Python!")
```
""",
            'key_insight': 'Every programmer in the world started with `print("Hello, World!")` — you just joined them.',
            'has_visualizer': False,
        },
        {
            'order': 2,
            'title': 'Variables and Data Types',
            'content_md': """# Variables: Storing Information

A **variable** is like a labelled box — you store a value in it and use the label to get it back.

```python
name = "Priya"
age = 13
height = 4.9
is_student = True
```

## Data Types

| Type | Example | What it stores |
|------|---------|---------------|
| `str` | `"Hello"` | Text |
| `int` | `42` | Whole numbers |
| `float` | `3.14` | Decimal numbers |
| `bool` | `True` / `False` | Yes/No values |

## Using Variables
```python
name = "Ravi"
age = 12
print("My name is", name)
print("I am", age, "years old")
```

You can also do maths:
```python
x = 10
y = 5
print(x + y)   # 15
print(x * y)   # 50
```
""",
            'key_insight': 'Variables are how programs remember information. Every app you use stores data in variables.',
            'has_visualizer': False,
        },
        {
            'order': 3,
            'title': 'Getting Input & Making Decisions',
            'content_md': """# Input and If/Else

## Getting Input from the User
```python
name = input("What is your name? ")
print("Hello,", name + "!")
```

`input()` pauses the program and waits for the user to type something.

## Making Decisions with If/Else

```python
age = int(input("Enter your age: "))

if age >= 13:
    print("You are a teenager!")
else:
    print("You are still young!")
```

### If / Elif / Else
```python
marks = int(input("Enter your marks: "))

if marks >= 90:
    print("Grade: A")
elif marks >= 75:
    print("Grade: B")
elif marks >= 60:
    print("Grade: C")
else:
    print("Grade: D — keep trying!")
```

**Comparison operators:** `>`, `<`, `>=`, `<=`, `==`, `!=`
""",
            'key_insight': 'If/else is how computers make choices — every AI decision tree is just if/else at its core.',
            'has_visualizer': False,
        },
        {
            'order': 4,
            'title': 'Loops: Doing Things Repeatedly',
            'content_md': """# Loops

Loops let you repeat code without writing it multiple times.

## For Loop
```python
for i in range(5):
    print("Count:", i)
# Output: Count: 0, 1, 2, 3, 4
```

Loop through a list:
```python
fruits = ["mango", "banana", "apple"]
for fruit in fruits:
    print("I like", fruit)
```

## While Loop
```python
count = 1
while count <= 5:
    print("Step", count)
    count = count + 1
```

## Real Example: Multiplication Table
```python
n = int(input("Enter a number: "))
for i in range(1, 11):
    print(n, "×", i, "=", n * i)
```
""",
            'key_insight': 'Loops are why computers can do millions of calculations in seconds — they repeat instructions tirelessly.',
            'has_visualizer': False,
        },
        {
            'order': 5,
            'title': 'Functions: Reusable Code Blocks',
            'content_md': """# Functions

A function is a named block of code you can run whenever you need it.

## Defining a Function
```python
def greet():
    print("Namaste!")
    print("Welcome to Python!")

greet()   # Call the function
greet()   # Call it again — same result!
```

## Functions with Parameters
```python
def greet(name):
    print("Hello,", name + "!")

greet("Aarav")
greet("Diya")
```

## Functions that Return Values
```python
def add(a, b):
    return a + b

result = add(10, 20)
print(result)   # 30
```

## Real Example: Area Calculator
```python
def area_of_rectangle(length, width):
    return length * width

l = float(input("Enter length: "))
w = float(input("Enter width: "))
print("Area =", area_of_rectangle(l, w))
```
""",
            'key_insight': 'Functions prevent repetition. Every Python library you will ever use is just a collection of well-named functions.',
            'has_visualizer': False,
        },
        {
            'order': 6,
            'title': 'Lists and Dictionaries',
            'content_md': """# Lists and Dictionaries

## Lists: Ordered Collections
```python
marks = [85, 92, 78, 95, 88]
print(marks[0])    # 85 (first item)
print(marks[-1])   # 88 (last item)
print(len(marks))  # 5 (number of items)
```

### Useful List Operations
```python
marks.append(90)    # Add item
marks.sort()        # Sort the list
print(sum(marks))   # Total
print(max(marks))   # Highest
```

## Dictionaries: Key-Value Pairs
```python
student = {
    "name": "Ananya",
    "age": 12,
    "grade": "7A",
    "marks": 91
}

print(student["name"])    # Ananya
print(student["marks"])   # 91
```

### Real Example: Contact Book
```python
contacts = {}
contacts["Rohan"] = "9876543210"
contacts["Priya"] = "9123456789"

name = input("Who to call? ")
print("Number:", contacts[name])
```
""",
            'key_insight': 'Lists and dictionaries are the building blocks of all data in Python — AI datasets are just large lists of dictionaries.',
            'has_visualizer': False,
        },
        {
            'order': 7,
            'title': 'Mini Project: Quiz Game',
            'content_md': """# Mini Project: Build a Quiz Game

Let's put everything together and build a small quiz game!

```python
# Quiz Game in Python
questions = [
    {
        "question": "What is the capital of India?",
        "answer": "delhi"
    },
    {
        "question": "How many sides does a triangle have?",
        "answer": "3"
    },
    {
        "question": "Which planet is closest to the Sun?",
        "answer": "mercury"
    },
]

score = 0

for q in questions:
    print("\\n" + q["question"])
    user_answer = input("Your answer: ").lower().strip()

    if user_answer == q["answer"]:
        print("Correct! ✓")
        score += 1
    else:
        print("Wrong! The answer was:", q["answer"])

print("\\nYour final score:", score, "out of", len(questions))

if score == len(questions):
    print("Perfect score! 🎉")
elif score >= 2:
    print("Well done!")
else:
    print("Keep practising — you'll get it!")
```

**What concepts does this use?**
- Lists of dictionaries
- For loops
- If/else
- Functions (input, print, len)
- Variables and operators

**Challenge:** Add 5 more questions and keep a high score!
""",
            'key_insight': 'You just built a real application. Every game, app, and website is a bigger version of exactly this pattern.',
            'has_visualizer': False,
        },
    ],
    'concepts': ['Variable', 'Data Type', 'Loop', 'Function', 'List', 'Dictionary', 'Conditional'],
    'quiz': [
        {
            'question': 'Which function is used to display output in Python?',
            'option_a': 'display()',
            'option_b': 'show()',
            'option_c': 'print()',
            'option_d': 'output()',
            'correct_answer': 'c',
            'explanation': 'print() is the built-in Python function to display text or values on the screen.',
            'difficulty': 'beginner',
            'order': 1,
        },
        {
            'question': 'What does `range(5)` produce?',
            'option_a': '1, 2, 3, 4, 5',
            'option_b': '0, 1, 2, 3, 4',
            'option_c': '0, 1, 2, 3, 4, 5',
            'option_d': '5, 4, 3, 2, 1',
            'correct_answer': 'b',
            'explanation': 'range(5) generates numbers from 0 to 4 (5 is excluded). Python starts counting from 0.',
            'difficulty': 'beginner',
            'order': 2,
        },
        {
            'question': 'How do you store text "Hello" in a variable called msg?',
            'option_a': 'msg == "Hello"',
            'option_b': 'msg = Hello',
            'option_c': 'msg = "Hello"',
            'option_d': 'variable msg = "Hello"',
            'correct_answer': 'c',
            'explanation': 'Use a single = sign to assign values. Text must be in quotes to make it a string.',
            'difficulty': 'beginner',
            'order': 3,
        },
        {
            'question': 'What is the output of: print(10 + 3 * 2)',
            'option_a': '26',
            'option_b': '16',
            'option_c': '17',
            'option_d': '11',
            'correct_answer': 'b',
            'explanation': 'Multiplication is done before addition (BODMAS). 3*2=6, then 10+6=16.',
            'difficulty': 'beginner',
            'order': 4,
        },
    ],
    'exercises': [
        {
            'order': 1,
            'title': 'Hello World',
            'description': 'Write your first Python program that prints your name and school.',
            'exercise_type': 'code',
            'instructions_md': 'Use `print()` to display:\n1. Your name\n2. Your school name\n3. Your favourite subject',
            'starter_code': '# Write your code below\nprint("My name is ")\n',
            'solution_code': 'print("My name is Arjun")\nprint("My school is Delhi Public School")\nprint("My favourite subject is Maths")\n',
            'hints': ['Use print() for each line', 'Put text inside quotes'],
            'grade_level': '7',
            'difficulty': 'beginner',
        },
        {
            'order': 2,
            'title': 'Multiplication Table',
            'description': 'Use a for loop to print the multiplication table of any number entered by the user.',
            'exercise_type': 'code',
            'instructions_md': '1. Ask the user to enter a number using `input()`\n2. Use a `for` loop with `range(1, 11)` \n3. Print each row of the table',
            'starter_code': 'n = int(input("Enter a number: "))\n# Write the loop below\n',
            'solution_code': 'n = int(input("Enter a number: "))\nfor i in range(1, 11):\n    print(n, "×", i, "=", n * i)\n',
            'hints': ['Use int(input()) to get a number', 'for i in range(1, 11): loops 1 to 10', 'Use n * i to calculate each product'],
            'grade_level': '7',
            'difficulty': 'beginner',
        },
        {
            'order': 3,
            'title': 'Quiz Game',
            'description': 'Build a 3-question quiz game that tracks the score.',
            'exercise_type': 'project',
            'instructions_md': '1. Store 3 questions in a list of dictionaries\n2. Loop through each question\n3. Compare the user\'s answer\n4. Add 1 to score for each correct answer\n5. Print the final score',
            'starter_code': 'questions = [\n    {"question": "Capital of India?", "answer": "delhi"},\n    # Add 2 more questions\n]\n\nscore = 0\n# Write your loop here\n',
            'solution_code': 'questions = [\n    {"question": "Capital of India?", "answer": "delhi"},\n    {"question": "Sides of a triangle?", "answer": "3"},\n    {"question": "Planet closest to Sun?", "answer": "mercury"},\n]\nscore = 0\nfor q in questions:\n    ans = input(q["question"] + " ").lower().strip()\n    if ans == q["answer"]:\n        print("Correct!")\n        score += 1\n    else:\n        print("Wrong! Answer:", q["answer"])\nprint("Score:", score, "/", len(questions))\n',
            'hints': ['Use a for loop over the questions list', 'Use .lower() to ignore capital letters', 'score += 1 adds 1 to score'],
            'grade_level': '7',
            'difficulty': 'beginner',
        },
    ],
}


class Command(BaseCommand):
    help = 'Seed Class 7 Python course module'

    def handle(self, *args, **options):
        data = PYTHON_MODULE
        slug = slugify(data['title'])

        module, created = Module.objects.update_or_create(
            slug=slug,
            defaults={
                'order': data['order'],
                'title': data['title'],
                'subtitle': data.get('subtitle', ''),
                'description': data['description'],
                'difficulty': data['difficulty'],
                'tag': data['tag'],
                'icon': data['icon'],
                'color': data['color'],
                'estimated_time': data['estimated_time'],
                'grade_level': data['grade_level'],
                'prerequisites': data.get('prerequisites', ''),
                'learning_objectives': data.get('learning_objectives', ''),
                'is_published': True,
            }
        )
        action = 'Created' if created else 'Updated'
        self.stdout.write(f'{action} module: {module.title}')

        # Sections
        for s in data.get('sections', []):
            Section, _ = __import__('modules.models', fromlist=['Section']).Section.objects.update_or_create(
                module=module,
                order=s['order'],
                defaults={
                    'title': s['title'],
                    'content_md': s['content_md'],
                    'key_insight': s.get('key_insight', ''),
                    'has_visualizer': s.get('has_visualizer', False),
                    'visualizer_type': s.get('visualizer_type', ''),
                }
            )

        # Concepts
        for concept_name in data.get('concepts', []):
            concept, _ = Concept.objects.get_or_create(name=concept_name)
            concept.modules.add(module)

        # Quiz Questions
        QuizQuestion.objects.filter(module=module).delete()
        for q in data.get('quiz', []):
            QuizQuestion.objects.create(
                module=module,
                question=q['question'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q.get('option_c', ''),
                option_d=q.get('option_d', ''),
                correct_answer=q['correct_answer'],
                explanation=q.get('explanation', ''),
                difficulty=q.get('difficulty', 'beginner'),
                order=q.get('order', 0),
            )

        # Practical Exercises
        PracticalExercise.objects.filter(module=module).delete()
        for ex in data.get('exercises', []):
            PracticalExercise.objects.create(
                module=module,
                order=ex['order'],
                title=ex['title'],
                description=ex['description'],
                exercise_type=ex['exercise_type'],
                instructions_md=ex['instructions_md'],
                starter_code=ex.get('starter_code', ''),
                solution_code=ex.get('solution_code', ''),
                hints=ex.get('hints', []),
                grade_level=ex.get('grade_level', '7'),
                difficulty=ex.get('difficulty', 'beginner'),
            )

        self.stdout.write(self.style.SUCCESS(
            f'Done! Class 7 Python module seeded with '
            f'{len(data["sections"])} sections, '
            f'{len(data["quiz"])} quiz questions, '
            f'{len(data["exercises"])} exercises.'
        ))
