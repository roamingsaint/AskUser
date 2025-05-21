# AskUser

**AskUser** is a smart CLI utility for collecting and validating user input in Python. It wraps common prompt patterns—validation, menus, defaults, and autocompletion—into a simple, consistent API.

---

## 📦 Installation

```bash
pip install askuser
```

---

## 📖 API Overview

| Function / Class                              | What It Does                                                                                                                           |
|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| `validate_input(...)`                         | Prompt for free-form input, validate type/pattern, show hints (min/max/default) and retry until valid                                  |
| `pretty_menu(*args, **kwargs)`                | Print a formatted menu of positional (`0:`) and keyword (`x:`) options                                                                 |
| `validate_user_option(...)`                   | Show a menu, auto-add `q: quit` (unless `q=False`), prompt user, and return the selected **key**                                       |
| `validate_user_option_value(...)`             | Like `validate_user_option`, but maps the chosen **key** to its **value**                                                               |
| `validate_user_option_enumerated(dict,...)`   | Enumerate a `dict` into numbered options, add `q: quit`, and return `(key, value)`                                                      |
| `choose_from_db(list_of_dicts,...)`           | Tabulate DB rows, prompt for an **existing** `id`, optionally accept `xq: quit`, and return `(id, row_dict)`                           |
| `choose_dict_from_list_of_dicts(list, field)` | Display each item’s `field` as a menu, return the selected **dict**                                                                     |
| `yes(prompt, default=None)`                   | Shorthand for `validate_input(prompt, "yes_no", default) == "y"` → returns **bool**                                                     |
| `SpeechCompleter`                             | *(internal)* a `prompt_toolkit` completer that finds substring matches in suggestions                                                   |
| `user_prompt(prompt, items, return_value=False)` | Prompt with autocomplete over a list/dict of `items`; if `return_value=True` (and `items` is a dict), returns the **value** instead.   |

---

## 🔍 `validate_input`

```python
validate_input(
    input_msg: str,
    validation_type: Literal[
      'custom','required','not_in','none_if_blank','yes_no',
      'int','float','alpha','alphanum','custom_chars','regex',
      'date','future_date','time','url','ms_url','slug','email','phone',
      'currency','country','language','movie_ids','ss_video_ids','bundle_ids'
    ],
    expected_inputs: list = None,
    not_in:        list = None,
    maximum:       Union[int, float] = None,
    minimum:       Union[int, float] = None,
    allowed_chars: str = None,
    allowed_regex: str = None,
    default:       Any = None
) -> Union[str,int,float,None]
```

- **Default values**  
  - If you set `default`, pressing Enter returns the default.  
- **Hints added automatically**  
  - `yes_no` adds ` (y/n)`  
  - `none_if_blank` adds ` (optional)`  
  - `time` adds ` (hh:mm:ss)`  
  - `maximum`/`minimum` display `(max: …)` / `(min: …)`  
  - `default` displays `(default: …)`  
- **Validation types**  
  - **Built-in**: `int`, `float`, `alpha`, `alphanum`, `date`, `future_date`, `time`, `url`, `email`, `phone`, `slug`, etc.  
  - **Custom**:  
    - `custom` with `expected_inputs=[…]`  
    - `not_in` with `not_in=[…]`  
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

## 🧭 Menus & Options

### `pretty_menu(*args, **kwargs)`

Prints a menu—no prompt:

```python
pretty_menu("List", "Add", d="Delete", q="Quit")
# 0: List    1: Add    d: Delete    q: Quit
```

---

### `validate_user_option(...)`

```python
validate_user_option(
    input_msg: str = "Option:",
    *args: str,
    **kwargs: str|bool  # pass q=False to suppress quit
) -> str
```

- **Auto-adds** `q: quit` unless `q=False`.  
- Returns the chosen **key**.

**Examples:**

```python
opt = validate_user_option("Pick:", "Red","Blue", g="Green")
# keys: '0','1','g','q'

opt = validate_user_option("Pick:", "One","Two", q=False)
# keys: '0','1'
```

---

### `validate_user_option_value(...)`

```python
validate_user_option_value(
    input_msg: str = "Option:",
    *args,
    **kwargs: Any  # key -> value
) -> Any
```

- Builds same menu, returns the **value**.

```python
genre = validate_user_option_value(a="Action", c="Comedy", d="Drama")
# 'c' → "Comedy"
```

---

### `validate_user_option_enumerated(dict, msg="Option:", start=1)`

```python
validate_user_option_enumerated(
    a_dict: Dict[Any, str],
    msg: str = "Option:",
    start: int = 1
) -> Tuple[Any, str]
```

- Enumerates `.items()` starting at `start`.  
- Adds `q: quit`.  
- Returns `(key, value)` or `('q', None)`.

```python
movies = {101:"Inception", 202:"Memento"}
mid, title = validate_user_option_enumerated(movies)
```

---

## 🗄 Database-Style Selection

### `choose_from_db(db_result, input_msg=None, table_desc=None, xq=False)`

```python
choose_from_db(
    db_result: List[Dict[str,Any]],
    input_msg: str = None,
    table_desc: str = None,
    xq: bool = False
) -> Tuple[int, Dict]
```

- Pretty-prints rows with `tabulate`.  
- Only **existing** `id` values in `db_result` are valid.  
- If `xq=True`, also accepts `xq` → returns `('xq','quit')`.  
- Invalid entries re-prompt.

---

### `choose_dict_from_list_of_dicts(list_of_dicts, key_to_choose)`

```python
choose_dict_from_list_of_dicts(
    list_of_dicts: List[Dict],
    key_to_choose: str
) -> Dict
```

- Menu of `dict[key_to_choose]`.  
- Returns selected dict.

```python
fruits = [{"name":"Apple"},{"name":"Banana"}]
choice = choose_dict_from_list_of_dicts(fruits, "name")
```

---

## ✅ Yes/No Shortcut

```python
yes("Continue?", default="y")  # True if 'y', False if 'n'; blank → default
```

---

## 💬 Autocomplete

```python
from askuser.autocomplete import user_prompt

res = user_prompt("Country: ", ["USA","UK","IN"], return_value=False)
# ≥2 chars → suggestions

opts = {"us":"United States","uk":"United Kingdom"}
code = user_prompt("Code: ", opts, return_value=True)
# returns 'us'
```

---

## 🔍 All Validation Types

| Type                     | Description                                      |
|--------------------------|--------------------------------------------------|
| `int` / `float`          | Numeric with optional `minimum` / `maximum`      |
| `alpha` / `alphanum`     | Only letters / letters+digits                    |
| `date` / `future_date`   | `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`            |
| `time`                   | `HH:MM:SS`                                       |
| `email`                  | Standard RFC email                               |
| `phone`                  | Digits with optional `+`, strips spaces/dashes  |
| `url`                    | Hostname + optional path/query                   |
| `slug`                   | `[a-z0-9-]` only, single delimiter               |
| `custom`                 | Only values in `expected_inputs`                 |
| `not_in`                 | Reject values in `not_in`                        |
| `custom_chars`           | Only chars in `allowed_chars`                    |
| `regex`                  | Match your regex                                 |
| `language`               | ISO-639 via `pycountry`                          |
| `country`                | Recognizes common abbreviations for countries    |

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
    assert validate_user_option("Pick:", "A","B", q=False) == '0'
```

Run:
```bash
pytest tests/
```

---

## 📜 License

MIT — free to use, modify, and distribute.
