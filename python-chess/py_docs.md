# Python Documentation Notes

https://docs.python.org/3/tutorial/

Now On 5.5

## Up to 5.1.3

### Questions
- Binary form libraries working in python, what is an Application for this?
- Uses for changing the coding ie: UTF-8
- There are links to additional reasources linked on the page, should I look at all of it?
- Shallow copies - very interesting, how important to everyday development?
- else: after loops?
- *arg is converted to multiple positional arguments for a function, **args is a dictionary?\
- Explination of 4.8.6 ex.2
  
### Notes
- Monty Python Documentation
- Use '_' in python interactive mode to reference the previous result
- String Splicing: [included:excluded] or [:excluded] or [included:]
- Strings are Immutable
- Lists support slice assignment (list[2:5] = [4,3,2])
- Remember to use enumerate(list) in place of range(len(list))
- Match case can use '_' that will catch anything
- can use '|' as or for match/case statements
- can use an if statement to 'guard' a case
- when reading the documentation of functions, [] around a parameter mean it is optional
- when using Lists as a Queue, import deque from collections for fast appending and popping from both sides

## 5.1.3 -> 6

### Questions

### Notes
- List comprehension: Using for loops inside of [] is a list comprehension and will <br>
  create a list to match the for statements, can also inclue if statements to match
  ```
  [(x, y)for x in iterable for y in iterable if x == y] --> [(1,1), (2,2), (3,3)]

  # or 
  [x**2 for x in iterable] --> [1, 4, 9]

  # and if statements like:
  [x**2 for x in iterable if x % 2 != 0] -> [1, 9]

  # or apply functions:
  [abs(x) for x in range(-3, 3)] --> [3, 2, 1, 0, 1, 2, 3]

  # or flatten lists like this:
  [number for element in [[1,2,3][4,5,6][7,8,9]] for number in element] -> [1, 2, 3, 4, 5, 6, 7, 8, 9]
  ```

- del statement is similar to pop() but does not return a value and ca also deleter variables
- Tuples are very similar to sting as they are a sequence data type like lists 
- Tuples are immutable like strings as well
- empty tuples and single item tuples are created as so:
    ```
    empty = ()
    single_item = ("item", )
    ```
- you can pack and uncpack tuples using a simliar syntax as multiple assignment
    ```
    # multiple assignment
    a, b = c, d

    # instanciating tuple
    a = b, c, d

    # unpacking tuples (len(a) = 3)
    b, c, d = a
    ```
- sets are similar to lists however there are a few key    differences, <br>
  most importantly, they are unordered, can have no duplicates and mamatical comutations can be performed directly on the set and no the individual items
- Here is how to use sets in code:
    ```
    # to instanciate a set use {} (like dics with no keys)
    a = {1, 2, 3, 3}

    # but it will remove any duplicates
    >>> a
    {2, 1, 3}

    # how to use operators on sets 
    a = set('abracadabra')
    b = set('alacazam')
    >>> a
    {'a', 'r', 'b', 'c', 'd'}

    >>> a - b                              # letters in a but not in b
    {'r', 'd', 'b'}

    >>> a | b                              # letters in a or b or both
    {'a', 'c', 'r', 'd', 'b', 'm', 'z', 'l'}

    >>> a & b                              # letters in both a and b
    {'a', 'c'}

    >>> a ^ b                              # letters in a or b but not both
    {'r', 'd', 'b', 'm', 'z', 'l'}
    ```
- Set Comprehension is also supported
    ```
    a = {x for x in 'abracadabra' if x not in 'abc'}
    >>> a
    {'r', 'd'}
    ```

