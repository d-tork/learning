# Clean Code - Notes for the office

## Vertical Separation
Variables and functions should be defined closed to where they are used. 

## Consistency
* ensure classes, functions, and variables have consistent names (in that order)

## Remove Clutter
Default constructors with no implementation, variables that aren't used, functions that are never
called, comments that add no information.

## Artificial Coupling
* move the hdfs paths to a more appropriate location (the AvroGetter subclass, where they're 
actually used, rather than the data class). I put them where they are out of convenience. 
* keep classes small; subclasses should be smaller than their parents

## Feature Envy
When a class uses another class's methods or accessors to manipulate its data objects. It "envies"
the scope of another class, it wants to be in its namespace.

### Implementation
* hdfspath updater?
* Couple other instances, probably in FDPData and that new class I created for Garn (start and end
date filler)

## Selector Arguments
The ambiguous True/False flag arguments in a function's caller. It's generally better to have 
many functions than to pass some code into a function to select the behavior.

## Polymorphism 
Defining abstract classes (not directly implemented) that defines the structure (in the form of
functions) for all its child classes to flesh out. Example:

```python
class Document:
    def __init__(self, name):
        self.name = name

    def show(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Pdf(Document):
    def show(self):
        return 'Show pdf contents!'

class Word(Document):
    def show(self):
        return 'Show word contents!'

documents = [Pdf('Document1'),
Pdf('Document2'),
Word('Document3')]

for document in documents:
    print document.name + ': ' + document.show()
```

### Implementation
* For `FDPData`, etc. inheriting from abstract class `DataSource`

## Enums
Use enumerated sets for unique, constant values. (https://docs.python.org/3/library/enum.html)

### Implementation
* For the timeline viz, enumerate colors and swim lane position constants.

## Be Precise
* If you decide to call a function that might return `null`, make sure you check for `null`.
* Use integers for currency, never floats. Consider a `Money` class to handle conversions.

## Encapsulate Conditionals
Extract functions that explain the intent of the conditional.

	if (shouldBeDeleted(timer))

is preferable to

	if (timer.hasExpired() && ~timer.isRecurrent())

## Enforce Temporal Coupling (where required)
When order of execution matters, structure arguments such that the order in which they should be
called is obvious. 

```java
public class MoogDiver {
  Gradient gradient;
  List<Spline> splines;

  public void dive(String reason) {
    saturateGradient();
	reticulateSplines();
	diveForMoog(reason);
	}
	...
}
```
Order is important, but the code does not enforce this temporal coupling. Another programmer could
call `reticulateSplines` before `saturateGradient` was called, leading to an 
`UnsaturatedGradientException`. A better solution is:

```java
public class MoogDiver {
  Gradient gradient;
  List<Spline> splines;

  public void dive(String reason) {
    Gradient gradient = saturateGradient();
	List<Spline> splines = reticulateSplines(gradient);
	diverForMoog(splines, reason);
  }
  ...
}
```
This creates a bucket brigade; each function produces a result that the next function needs, so there is no reasonable way to call them out of order. 

### Implementation
* the order of functions in preparing a dataset for join (i.e. create all columns before slicing,
renaming, or changing to lowercase)

## Names should describe their side effects

## Python Decorators
should I need them 

```python
import functools

def decorator(func):
	@functools.wraps(func)
	def wrapper_decorator(*args, **kwargs):
		# Do something before
		value = func(*args, **kwargs)
		# Do something after
		return value
	return wrapper_decorator
```

# A project skeleton (Python)
For Azure Shell / Continuous Integration
## A Makefile:
```Makefile
setup:
	python3 -m venv venv

install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

test:
	python -m pytest -vv test_hello.py

lint:
	pylint --disable=R,C hello.py

all: install lint test
```

## Github actions
```yaml
# pythonapp.yml
---
name: Azure Python 3.5
on: [push]
jobs:
	build:
		runs-on: ubuntu-latest
		steps:
		- uses: actions/checkout@v2
		- name: Set up Python 3.5.10
		  uses: actions/setup-python@v1
		  with:
		  	python-version: 3.5.10
		- name: Install dependencies
		  run: |
		  	make install
		- name: Lint
		  run: |
		  	make lint
		- name: Test
		  run: |
		  	make test
```
