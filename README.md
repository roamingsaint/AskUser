# AskUser

**AskUser** is a lightweight utility package that provides clean, validated CLI prompts with autocompletion, menus, and friendly user input handling.

## ✨ Features
- Validates user input types (date, email, float, yes/no, etc.)
- Provides user-friendly menus
- Autocompletion for structured prompts
- Supports default values, optional fields, and range checks

## 🚀 Usage

```python
from askuser import validate_input, validate_user_option

# Simple input validation
age = validate_input("Enter your age", "int", minimum=0)

# Menu
choice = validate_user_option("Choose action", a="Add movie", d="Delete movie", q="Quit")
```

## 📦 Installation

```bash
pip install askuser
```

## 🧪 Tests

```bash
pytest tests/
```
