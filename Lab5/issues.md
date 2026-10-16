# Lab 5 : Static Code Analysis: Issue Log

The line numbers below refer to the **original assigned file** in `baseline/hospital_patient_system.py`. Severity is a practical prioritisation for this lab; exact tool wording and severity should be copied from the real local Pylint/Bandit/Flake8 reports after running `run_analysis.sh`.

| Issue | Type / tool | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Dynamic `eval()` | Security : Bandit (medium-priority) | 37–40 | Evaluating a caller-provided expression can execute arbitrary Python code. | Replaced the expression string with a numeric multiplier and calculate the cost directly. |
| Shell command built from a filename | Security : Bandit | 51–55 | `os.system()` invokes a shell and concatenates the supplied filename into a command. | Removed shell execution and printed the export result directly. |
| Hard-coded nurse key exposed in output | Security review / Bandit-style finding | 66–76 | A credential-like value is committed in source and printed to the terminal. | Removed the unused credential and its print statement; secrets should not be embedded in source or logged. |
| Weak MD5 digest | Security : Bandit | 43–44 | MD5 is not suitable where a modern cryptographic digest is expected. | Switched the deterministic digest to SHA-256. This digest is not encryption or anonymisation for predictable IDs. |
| Non-cryptographic token generator | Security review | 47–48 | `random` is not designed for security-sensitive tokens. | Switched to `secrets.randbelow()` for a four-digit token. |
| Mutable default argument | Correctness : Pylint | 12 | `intake_log=[]` creates one list shared between calls that omit the argument. | Changed the default to `None` and initialise a fresh list inside the function. |
| Bare `except` silently ignores errors | Correctness : Pylint | 20–25 | The handler catches every exception and hides failures, making defects difficult to diagnose. | Replaced it with an explicit lookup and a boolean result for unknown IDs. |
| Unused import and local variable | Quality : Pylint / Flake8 | 4, 28 | `math` and `bed_charge` are unused. | Removed the unused import and local variable. |
| `== None` comparison and redundant branch | Quality : Pylint | 27–35 | The code uses a non-idiomatic `None` comparison and an unnecessary `else` after a return. | Used a single lookup and a direct boolean return. |
| File opened without a context manager | Quality : Pylint | 51–54 | If writing fails, explicit close may be skipped; output is also Python's `repr` rather than a data format. | Used `Path.open()` with a context manager and exported JSON. |
| Naming and formatting issues | Style : Pylint / Flake8 | 12, 13, 16, 37, 43, 47, 58–63 | `admitPatient`, short names, long lines, and inconsistent style make the code harder to maintain. | Used snake_case names, descriptive variables, annotations, docstrings, and consistent formatting. |
| Script executes on import | Maintainability : Pylint/code review | 79–80 | Importing the module runs the demo and writes a ledger as a side effect. | Put the demo behind `if __name__ == "__main__":`. |

## Verification status

The fixed source was checked for Python syntax and exercised with smoke tests in this environment. Pylint, Bandit, and Flake8 could not be installed here because package-server DNS/network access was unavailable. Therefore, this file does **not** claim an actual final Pylint score or that the three tools returned zero findings. Run `./run_analysis.sh` in an environment with package access to generate the genuine reports in `reports/before/` and `reports/after/`.
