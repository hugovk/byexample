<!--
Check that we have byexample installed first
$ hash byexample                                    # byexample: +fail-fast

$ alias byexample=byexample\ --pretty\ none

--
-->

# Terminal Emulation

``byexample`` can use different emulation modes to process the output of the
runners.

By default ``byexample`` uses a *dumb terminal* (``+term=dumb``) which
is fast and works well in most cases.

But you can change this to disable emulation with ``+term=as-is`` or
to enable full ANSI terminal emulation with ``+term=ansi``.

## Dumb terminal

In this mode, ``byexample`` emulates a very simple terminal, processing
only the white spaces.

It does not have the concept of a cursor, does not
interpret escape codes and does not break lines automatically.

Even if a [geometry](/{{ site.uprefix }}/advanced/geometry) is defined
with ``+geometry``, the *dumb terminal*
does not force any boundaries: the following example
will print a string longer than the width of the terminal.

```python
>>> print("aaaabbbb" * 8)      # byexample: +geometry 24x32
aaaabbbbaaaabbbbaaaabbbbaaaabbbbaaaabbbbaaaabbbbaaaabbbbaaaabbbb
```

### White space processing

The dumb terminal removes any trailing whitespace, converts tabs to spaces
and standardizes the new lines.

This suits most examples, reducing the need to add tabs into the
examples or requiring the
[normalization of whitespace](/{{ site.uprefix }}/basic/normalize-whitespace)
with ``+norm-ws``.

```python
>>> print("\tfoo\tbar\nbaz\tsaz    \rtaz")
        foo     bar
baz     saz
taz
```

If you need to check whitespace characters, you can use ``+term=as-is`` to
disable terminal emulation.

## As-is terminal

When ``+term=as-is`` is activated the output is passed *as is* without
any modification except for *standardization* of new lines.

It can be useful in some special cases to check white spaces
that are removed by the dumb or ANSI terminals.

```python
>>> print("\tfoo\tbar\nbaz\tsaz    \rtaz")       # byexample: +term=as-is
	foo	bar
baz	saz    
taz
```

## ANSI terminal

Some programs may need a real terminal or at least an
*emulated ANSI terminal*.

``byexample`` can emulate one capable of interpreting and emulating
all the control sequences and escape codes using ``+term=ansi``.

> **Note:** terminal emulation is not fully supported in ``Python 2.7``.
> It should work but using a modern ``Python`` version is recommended.

### Removing color

If you have an example that is printing text with color, you will probably see
something like:

```shell
$ echo -e "\033[31mmessage in red\033[0m"
<...>[31mmessage in red<...>[0m
```

To get rid of those weird symbols you can enable terminal emulation:

```shell
$ echo -e "\033[31mmessage in red\033[0m"      # byexample: +term=ansi
message in red
```

### Terminal boundaries

Keep in mind that an *emulated terminal* will honor its own boundaries
or [geometry](/{{ site.uprefix }}/advanced/geometry): if
an example prints a string longer than the width of the terminal, the string
will spawn multiple lines (a newline is added automatically).

```python
>>> print("aaaabbbb" * 8)      # byexample: +term=ansi +geometry 24x32
aaaabbbbaaaabbbbaaaabbbbaaaabbbb
aaaabbbbaaaabbbbaaaabbbbaaaabbbb
```

This is especially useful to work with ``ncurses`` or other advanced programs.

### ncurses support

Some applications use advanced terminal features (like the ones
that use ``ncurses``) and require a terminal emulator.

Examples of this are programs like ``less``, ``more``, ``top`` and ``man``.

```shell
$ less test/ds/python-tutorial.v2.md # byexample: +term=ansi +rm=~ +stop-on-timeout
~This is a 101 Python tutorial
~The following is an example written in Python about arithmetics
~
~    ```
~    >>> from __future__ import print_function
~    >>> 1 + 2
~    3
~    ```
~
~The next examples show you about complex numbers in Python
~
~    ```
~    >>> 2j * 2
~    4j
~
~    >>> 2j + 4j
~    6j
~    ```
~
~<...>(END)
```

> Try the above example without ``+term=ansi`` and see what happens.

<!--
$ kill %%     # byexample: -skip +pass
-->

### Pagination

``byexample`` will not emulate pagination. When the output is larger than
the height of the terminal, lines that scroll off the top are discarded.

The following example prints more lines than are available in the terminal so
only the last lines are shown.

```python
>>> for i in range(1,33):       # byexample: +term=ansi +geometry=5x80
...     print("line %i" % i)
line 29
line 30
line 31
line 32
```

If this is a problem change the [geometry](/{{ site.uprefix }}/advanced/geometry):
increase the count of rows that the terminal has with ``+geometry``.

<!--

The following tests make sure that the runners for C++, PHP and Elixir
are working as they use a special mechanism for _get_output
even if the terminal is too small (under the hood the +geometry
never changes)

?: #include <iostream>                 // byexample: +geometry=5x80
?: for (int i = 1; i < 100; ++i) {
::    std::cout << "line " << i << "\n";
:: }
line 1
line 2
line 3
line 4
line 5
line 6
line 7
line 8
line 9
line 10
line 11
line 12
line 13
line 14
line 15
line 16
line 17
line 18
line 19
line 20
line 21
line 22
line 23
line 24
line 25
line 26
line 27
line 28
line 29
line 30
line 31
line 32
line 33
line 34
line 35
line 36
line 37
line 38
line 39
line 40
line 41
line 42
line 43
line 44
line 45
line 46
line 47
line 48
line 49
line 50
line 51
line 52
line 53
line 54
line 55
line 56
line 57
line 58
line 59
line 60
line 61
line 62
line 63
line 64
line 65
line 66
line 67
line 68
line 69
line 70
line 71
line 72
line 73
line 74
line 75
line 76
line 77
line 78
line 79
line 80
line 81
line 82
line 83
line 84
line 85
line 86
line 87
line 88
line 89
line 90
line 91
line 92
line 93
line 94
line 95
line 96
line 97
line 98
line 99


php> for ($i = 1; $i < 100; $i += 1) {  // byexample: +geometry=5x80
...>    echo "line $i\n";
...> }
line 1
line 2
line 3
line 4
line 5
line 6
line 7
line 8
line 9
line 10
line 11
line 12
line 13
line 14
line 15
line 16
line 17
line 18
line 19
line 20
line 21
line 22
line 23
line 24
line 25
line 26
line 27
line 28
line 29
line 30
line 31
line 32
line 33
line 34
line 35
line 36
line 37
line 38
line 39
line 40
line 41
line 42
line 43
line 44
line 45
line 46
line 47
line 48
line 49
line 50
line 51
line 52
line 53
line 54
line 55
line 56
line 57
line 58
line 59
line 60
line 61
line 62
line 63
line 64
line 65
line 66
line 67
line 68
line 69
line 70
line 71
line 72
line 73
line 74
line 75
line 76
line 77
line 78
line 79
line 80
line 81
line 82
line 83
line 84
line 85
line 86
line 87
line 88
line 89
line 90
line 91
line 92
line 93
line 94
line 95
line 96
line 97
line 98
line 99

iex> Enum.each(1..99, fn i -> IO.puts("line #{i}") end)  # byexample: +geometry=5x80
line 1
line 2
line 3
line 4
line 5
line 6
line 7
line 8
line 9
line 10
line 11
line 12
line 13
line 14
line 15
line 16
line 17
line 18
line 19
line 20
line 21
line 22
line 23
line 24
line 25
line 26
line 27
line 28
line 29
line 30
line 31
line 32
line 33
line 34
line 35
line 36
line 37
line 38
line 39
line 40
line 41
line 42
line 43
line 44
line 45
line 46
line 47
line 48
line 49
line 50
line 51
line 52
line 53
line 54
line 55
line 56
line 57
line 58
line 59
line 60
line 61
line 62
line 63
line 64
line 65
line 66
line 67
line 68
line 69
line 70
line 71
line 72
line 73
line 74
line 75
line 76
line 77
line 78
line 79
line 80
line 81
line 82
line 83
line 84
line 85
line 86
line 87
line 88
line 89
line 90
line 91
line 92
line 93
line 94
line 95
line 96
line 97
line 98
line 99
-->

### Performance

Emulation is typically 3 times slower than the normal mode
(``+term=dumb``).
Keep that in mind and try to not enable it by default.
