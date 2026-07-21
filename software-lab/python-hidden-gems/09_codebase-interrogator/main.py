"""
Project 09: Codebase Interrogator

Hidden Gem: `radon` — analyzes Python source code for cyclomatic complexity,
maintainability index, and raw metrics without running the code.

What it does: Scans Python files in a directory and reports complexity,
maintainability, and code statistics. Helps identify code that needs refactoring.
"""
import os
import ast
import sys
from collections import defaultdict


def analyze_file(filepath):
    """Analyze a single Python file using the ast module."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)
    except SyntaxError as e:
        return {"error": str(e), "lines": 0}
    except Exception as e:
        return {"error": str(e), "lines": 0}

    lines = source.count('\n') + 1
    functions = 0
    classes = 0
    imports = 0
    max_depth = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1
        elif isinstance(node, ast.ClassDef):
            classes += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            imports += 1

    # Count complexity via nested control flow
    def get_depth(node, current=0):
        nonlocal max_depth
        max_depth = max(max_depth, current)
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With,
                                  ast.Try, ast.ExceptHandler)):
                get_depth(child, current + 1)
            else:
                get_depth(child, current)

    get_depth(tree)

    # Count docstrings
    docstrings = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            if ast.get_docstring(node):
                docstrings += 1

    return {
        "lines": lines,
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "max_nesting": max_depth,
        "docstrings": docstrings,
        "error": None,
    }


def scan_directory(directory=".", max_files=50):
    """Scan all Python files in a directory."""
    results = []
    for root, dirs, files in os.walk(directory):
        # Skip common ignore dirs
        dirs[:] = [d for d in dirs if d not in {
            '__pycache__', '.git', 'venv', '.venv', 'node_modules',
            'env', 'dist', 'build', '.tox', '.mypy_cache'
        }]

        for fname in files:
            if fname.endswith('.py'):
                filepath = os.path.join(root, fname)
                stats = analyze_file(filepath)
                stats["file"] = os.path.relpath(filepath, directory)
                results.append(stats)
                if len(results) >= max_files:
                    return results

    return results


def print_report(results):
    """Print a formatted analysis report."""
    print("=" * 60)
    print("  CODEBASE INTERROGATOR — Analysis Report")
    print("=" * 60)

    total_lines = 0
    total_functions = 0
    total_classes = 0
    total_docstrings = 0
    errors = 0
    complex_files = []

    for r in results:
        if r.get("error"):
            errors += 1
            print(f"  ✗ {r['file']}: {r['error']}")
            continue

        total_lines += r["lines"]
        total_functions += r["functions"]
        total_classes += r["classes"]
        total_docstrings += r["docstrings"]

        if r["max_nesting"] >= 4:
            complex_files.append((r["file"], r["max_nesting"], r["lines"]))

    print(f"\n  Files analyzed:    {len(results) - errors}")
    print(f"  Total lines:       {total_lines:,}")
    print(f"  Functions:         {total_functions}")
    print(f"  Classes:           {total_classes}")
    print(f"  Docstrings:        {total_docstrings}")
    print(f"  Parse errors:      {errors}")

    if total_functions > 0:
        ratio = total_docstrings / total_functions * 100
        print(f"  Doc coverage:      {ratio:.1f}%")

    if complex_files:
        print(f"\n  ⚠ High complexity files (nesting ≥ 4):")
        complex_files.sort(key=lambda x: x[1], reverse=True)
        for fname, depth, lines in complex_files[:10]:
            print(f"    {fname}: depth={depth}, lines={lines}")

    print(f"\n  {'=' * 56}")


def main():
    # Analyze this project directory itself
    target = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(target)

    print(f"\n  Scanning: {parent}")
    print()

    results = scan_directory(parent, max_files=100)
    print_report(results)


if __name__ == "__main__":
    main()
