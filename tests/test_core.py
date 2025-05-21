from askuser.core import validate_input


def test_yes_no(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    assert validate_input("Continue?", "yes_no") == "y"
