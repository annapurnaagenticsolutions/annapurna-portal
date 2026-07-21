"""
Project 10: The Aggressive Linter AI

Hidden Gem: `ruff` — a blazing-fast Python linter written in Rust.
10-100x faster than flake8, with 700+ rules and auto-fix capabilities.

What it does: Runs ruff on Python files, shows violations, and demonstrates
auto-fixing. Falls back to a simple built-in checker if ruff isn't installed.
"""
import os
import subprocess
import sys


def run_ruff(target=".", fix=False):
    """Run ruff linter on the target directory."""
    cmd = ["ruff", "check", target]
    if fix:
        cmd.append("--fix")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return None, "ruff not installed", -1
    except subprocess.TimeoutExpired:
        return None, "Timed out", -1


def simple_lint(filepath):
    """A simple built-in linter for when ruff isn't available."""
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return [(0, f"Cannot read file: {e}")]

    for i, line in enumerate(lines, 1):
        stripped = line.rstrip('\n')

        # Trailing whitespace
        if stripped != stripped.rstrip():
            issues.append((i, "Trailing whitespace"))

        # Line too long (>100 chars)
        if len(stripped) > 100:
            issues.append((i, f"Line too long ({len(stripped)} chars)"))

        # Tab indentation (should be spaces)
        if '\t' in line[:10]:
            issues.append((i, "Tab indentation (use spaces)"))

        # Bare except
        if 'except:' in stripped and 'except Exception' not in stripped:
            issues.append((i, "Bare except clause"))

        # Print statement (should use logging)
        if stripped.strip().startswith('print(') and 'def ' not in stripped:
            issues.append((i, "Print statement (consider logging)"))

        # Unused import (very basic check)
        if stripped.startswith('import ') and ', ' not in stripped:
            mod = stripped.split('import ')[1].strip()
            # Check if module name appears elsewhere in file
            content = ''.join(lines)
            if content.count(mod) < 2:
                issues.append((i, f"Possibly unused import: {mod}"))

    return issues


def scan_with_simple_linter(directory="."):
    """Scan Python files with the built-in linter."""
    total_issues = 0
    files_checked = 0

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in {
            '__pycache__', '.git', 'venv', '.venv', 'node_modules', 'env'
        }]

        for fname in files:
            if not fname.endswith('.py'):
                continue

            filepath = os.path.join(root, fname)
            issues = simple_lint(filepath)
            files_checked += 1

            if issues:
                print(f"\n  {os.path.relpath(filepath, directory)}:")
                for line_no, msg in issues:
                    print(f"    Line {line_no:3d}: {msg}")
                    total_issues += 1

    return files_checked, total_issues


def main():
    print("--- Aggressive Linter AI ---")
    print("Checking Python code quality...\n")

    target = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Try ruff first
    stdout, stderr, rc = run_ruff(target, fix=False)

    if stdout is not None:
        print("Using: ruff (Rust-powered, 700+ rules)\n")
        if stdout.strip():
            print(stdout)
        else:
            print("  ✓ No issues found! Code is clean.")
        print(f"\n  Exit code: {rc}")
    else:
        print("ruff not installed. Using built-in simple linter.\n")
        print("Install ruff for full power: pip install ruff\n")

        files, issues = scan_with_simple_linter(target)
        print(f"\n  {'=' * 50}")
        print(f"  Files checked: {files}")
        print(f"  Issues found:  {issues}")
        print(f"  {'=' * 50}")


if __name__ == "__main__":
    main()
