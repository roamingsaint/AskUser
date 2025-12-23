# AskUser

**AskUser** is a smart CLI utility for collecting and validating user input in Python. It wraps common prompt patterns—validation, menus, defaults, and autocompletion—into a simple, consistent API.

---

## 📦 Installation

```bash
pip install askuser
```

---

## 📖 API Overview

| Function / Class                                 | What It Does                                                                                                                         |
|--------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| `validate_input(...)`                            | Prompt for free-form input, validate type/pattern, show hints (min/max/default) and retry until valid                                |
| `pretty_menu(*args, **kwargs)`                   | Print a formatted menu of positional (`0:`) and keyword (`x:`) options                                                               |
| `validate_user_option(...)`                      | Show a menu, auto-add `q: quit` (unless `q=False`), prompt user, and return the selected **key**                                     |
| `validate_user_option_value(...)`                | Like `validate_user_option`, but maps the chosen **key** to its **value**                                                            |
| `validate_user_option_enumerated(dict,...)`      | Enumerate a `dict` into numbered options, add `q: quit`, and return `(key, value)`                                                   |
| `validate_user_option_multi(...)`                | **Multi-select** version of `validate_user_option`, returns **keys** in pick order; exit with `d: done` (or `xd`, `xd2`, ...)          |
| `validate_user_option_value_multi(...)`          | **Multi-select** version of `validate_user_option_value`, returns **values** in pick order; exit with `d: done`                      |
| `choose_from_db(list_of_dicts,...)`              | Tabulate DB rows, prompt for an **existing** `id`, optionally accept `xq: quit`, and return `(id, row_dict)`                         |
| `choose_dict_from_list_of_dicts(list, field)`    | Display each item’s `field` as a menu, return the selected **dict**                                                                  |
| `yes(prompt, default=None)`                      | Shorthand for `validate_input(prompt, "yes_no", default) == "y"` → returns **bool**                                                  |
| `SubstringCompleter`                             | A `prompt_toolkit` completer that finds substring matches in suggestions                                                             |
| `user_prompt(prompt, items, return_value=False)` | Prompt with autocomplete over a list/dict of `items`; if `return_value=True` (and `items` is a dict), returns the **value** instead. |

> 🔎 **Key types:** When you pass options via `**kwargs`, selected **keys are returned in their original types** (e.g., `int` stays `int`). With positional `*args`, menu keys are enumerated strings: `'0'`, `'1'`, ...

---

## 🔍 `validate_input`

```python
validate_input(
    input_msg: str,
    validation_type: str,
    expected_inputs: list = None,
    not_in:        list = None,
    maximum:       int | float = None,
    minimum:       int | float = None,
    allowed_chars: str = None,
    allowed_regex: str = None,
    default:       object = None
) -> object
```

- **Default values**
  - If you set `default`, pressing Enter returns the default.
- **Hints added automatically**
  - `yes_no` adds ` (y/n)`
  - `none_if_blank` adds ` (optional)`
  - `time` adds ` (hh:mm:ss)`
  - `maximum`/`minimum` display `(max: ...)` / `(min: ...)`
  - `default` displays `(default: ...)`
- **Validation types**
  - **Built-in:** `int`, `float`, `decimal`, `alpha`, `alphanum`, `date`, `future_date`, `time`, `url`, `email`, `phone`, `slug`, `language`.
  - **List/pattern helpers:**
    - `custom` with `expected_inputs=[...]`
    - `not_in` with `not_in=[...]`
    - `custom_chars` with `allowed_chars="abc123"`
    - `regex` with `allowed_regex="^[A-Z]+$"`

**Example:**

```python
# integer with bounds & default
count = validate_input(
    "How many items?", "int",
    minimum=1, maximum=100,
    default=10
)
# • Blank → count == 10
# • Invalid/out-of-range → re-prompt
```

---

## 🧠 Case sensitivity: what happens with `custom` vs `yes_no`?

AskUser intentionally mixes both behaviors:

- `custom` is **case-sensitive** (exact match)
- `yes_no` is **case-insensitive** (accepts `Y`, `y`, `N`, `n`)

**Example (case-sensitive `custom`):**

```python
# expected_inputs contains lowercase 'y'
v = validate_input("Pick:", "custom", expected_inputs=["y", "n"])
```

- user enters `y` → ✅ accepted
- user enters `Y` → ❌ rejected (reprompt), because `"Y" != "y"`

**Example (case-insensitive `yes_no`):**

```python
ok = yes("Continue?")   # uses validation_type="yes_no" internally
```

- user enters `Y` → ✅ accepted (normalized to lowercase, returns True)
- user enters `N` → ✅ accepted (returns False)

---

## 🧭 Menus & Options

### `pretty_menu(*args, **kwargs)`

Prints a menu—no prompt:

```python
pretty_menu("List", "Add", d="Delete", q="Quit")
# 0: List    1: Add    d: Delete    q: Quit
```

> Menu keys are **case-sensitive** (what you see is what you type).

---

### `validate_user_option(...)`

```python
validate_user_option(
    input_msg: str = "Option:",
    *args,
    **kwargs  # pass q=False to suppress quit
) -> object  # key (kwargs preserves original key types; args return '0','1',...)
```

- **Auto-adds** `q: quit` unless `q=False`.
- Returns the chosen **key** (preserving original type for `**kwargs`).

**Examples:**

```python
opt = validate_user_option("Pick:", "Red", "Blue", g="Green")
# keys: '0','1','g','q'

opt = validate_user_option("Pick:", "One", "Two", q=False)
# keys: '0','1'
```

---

### `validate_user_option_value(...)`

```python
validate_user_option_value(
    input_msg: str = "Option:",
    *args,
    **kwargs  # key -> value
) -> object
```

- Builds same menu, returns the **value**.
- **No `q` by default** (legacy behavior).

```python
genre = validate_user_option_value(a="Action", c="Comedy", d="Drama")
# 'c' → "Comedy"
```

---

### `validate_user_option_multi(...)`

```python
validate_user_option_multi(
    input_msg: str = "Option:",
    *args,
    **kwargs  # key -> label
) -> list
```

- **Multi-select** version of `validate_user_option`.
- Exit with **`d: done`** by default. If `d` is already used in your options, exit appears as **`xd`**, or **`xd2`**, **`xd3`**, ...
- Pass **`d=False`** to disable exit and force “pick until exhausted.”
- Returns a list of **keys** in the order picked (kwargs preserve original key types).

```python
STATUS = {0: "new", 1: "active", 7: "rejected"}
picked = validate_user_option_multi("Select statuses:", **STATUS)
# → [1, 7]
```

---

### `validate_user_option_value_multi(...)`

```python
validate_user_option_value_multi(
    input_msg: str = "Option:",
    *args,
    **kwargs  # key -> value
) -> list
```

- **Multi-select** version of `validate_user_option_value`.
- Exit with **`d: done`** (or `xd`, `xd2`, ... if `d` is taken). Use **`d=False`** to disable exit.
- Returns a list of **values** in the order picked.

```python
vals = validate_user_option_value_multi("Pick genres", a="Action", c="Comedy", d="Drama")
# user picks: c, a → ['Comedy', 'Action']
```

---

### `validate_user_option_enumerated(dict, msg="Option:", start=1)`

```python
validate_user_option_enumerated(
    a_dict: dict,
    msg: str = "Option:",
    start: int = 1
) -> tuple
```

- Enumerates `.items()` starting at `start`.
- Adds `q: quit`.
- Returns `(key, value)` or `('q', None)`.

```python
movies = {101: "Inception", 202: "Memento"}
mid, title = validate_user_option_enumerated(movies, start=1)
```

---

## 🗄 Database-Style Selection

### `choose_from_db(db_result, input_msg=None, table_desc=None, xq=False)`

```python
choose_from_db(
    db_result: list[dict],
    input_msg: str = None,
    table_desc: str = None,
    xq: bool = False
) -> tuple
```

- Pretty-prints rows with `tabulate`.
- Only **existing** `id` values in `db_result` are valid.
- If `xq=True`, also accepts `xq` → returns `('xq', 'quit')`.
- Invalid entries re-prompt.

---

### `choose_dict_from_list_of_dicts(list_of_dicts, key_to_choose)`

```python
choose_dict_from_list_of_dicts(
    list_of_dicts: list[dict],
    key_to_choose: str
) -> dict
```

- Menu of `dict[key_to_choose]`.
- Returns selected dict.

```python
fruits = [{"name": "Apple", "color": "red"}, {"name": "Banana", "color": "yellow"}]
choice = choose_dict_from_list_of_dicts(fruits, "name")
```

---

## ✅ Yes/No Shortcut

```python
yes("Continue?", default="y")  # True if 'y', False if 'n'; blank → default
```

---

## 💬 Autocomplete

Top-level import (recommended):

```python
from askuser import user_prompt

res = user_prompt("Country: ", ["USA", "UK", "IN"], return_value=False)
# ≥2 chars → suggestions

opts = {"us": "United States", "uk": "United Kingdom"}
code = user_prompt("Code: ", opts, return_value=True)
# returns 'us'
```

If you want to build your own prompt_toolkit session, you can also import:

```python
from askuser import SubstringCompleter
```

---

## 🧩 Extending AskUser with custom validators

AskUser supports registering additional validators at runtime without mutating internal globals directly.

```python
from askuser import register_validator, validate_input

def is_even(user_input: str) -> int:
    n = int(user_input)
    if n % 2 != 0:
        raise ValueError("Must be even")
    return n

register_validator("even_int", is_even)
x = validate_input("Enter even:", "even_int")
```

Helpers:

- `get_validators()`
- `register_validator(name, func, overwrite=False)`
- `register_validators({name: func, ...}, overwrite=False)`
- `unregister_validator(name)`

---

## 🔍 All Validation Types

| Type                        | Description                                       |
|-----------------------------|---------------------------------------------------|
| `int` / `float` / `decimal` | Numeric with optional `minimum` / `maximum`       |
| `alpha` / `alphanum`        | Only letters / letters+digits                     |
| `date` / `future_date`      | `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`             |
| `time`                      | `HH:MM:SS`                                        |
| `email`                     | Standard RFC email                                |
| `phone`                     | Digits with optional `+`, strips spaces/dashes    |
| `url`                       | Hostname + optional path/query                    |
| `slug`                      | `[a-z0-9-]` only, single delimiter                |
| `custom`                    | Only values in `expected_inputs` (case-sensitive) |
| `not_in`                    | Reject values in `not_in` (case-insensitive)      |
| `custom_chars`              | Only chars in `allowed_chars`                     |
| `regex`                     | Match your regex                                  |
| `language`                  | ISO-639 via `pycountry`                           |

---

## 🧪 Testing

Under `tests/`, examples:

```python
import pytest
from askuser import validate_input, yes, validate_user_option

def test_default(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    assert validate_input("Prompt?", "int", default=7) == 7

def test_no_quit(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '0')
    assert validate_user_option("Pick:", "A", "B", q=False) == '0'
```

Run:
```bash
pytest tests/
```

---

## 📜 License

MIT — free to use, modify, and distribute.
