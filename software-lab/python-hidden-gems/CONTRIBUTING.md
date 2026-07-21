# Contributing to Python Hidden Gems

## Pick a WIP Project

1. Browse projects 21-100 in the repository
2. Each project folder has a name that describes what it should do
3. Check the [README.md](README.md) catalog for the suggested package
4. Open an issue claiming the project (e.g., "I'll take #23_folder-guardian")

## Write the Code

Each project should:

- **Be self-contained** — one `main.py` file, no external services required
- **Use an interesting package** — the "hidden gem" from PyPI
- **Actually run** — `python main.py` should produce visible output
- **Have a docstring** — explain what it does and which package is the star
- **Include error handling** — try/except with helpful messages
- **Be under 100 lines** — these are mini-projects, not frameworks

## Example Pattern

```python
"""
Project NN: Project Name

Hidden Gem: `package_name` — what makes it special.

What it does: Brief description.
"""
from package_name import CoolThing

def main():
    try:
        result = CoolThing.do_something()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Submit

1. Fork the repo
2. Create a branch: `git checkout -b project-NN-name`
3. Write `main.py` and update `requirements.txt`
4. Test: `python -m py_compile main.py` (syntax) and `python main.py` (runtime)
5. Submit a PR

## Guidelines

- Pin all dependencies in `requirements.txt`
- No API keys required (use `.env.example` for optional config)
- Keep it educational — the goal is to showcase the package
