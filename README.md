This project uses **Taskipy** to automate boring tasks.
Below are the installation instructions and available commands.

## Installation

1. Clone the repository:
   ```bash
   git clone <REPOSITORY_URL>
   cd <PROJECT_FOLDER>
   ```
2. Install Poetry:
   ```bash
   pip install poetry
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

5. Run the command:
   ```bash
   poetry run python3 ./src/extraction/spider.py
   ```

6. Check the available data in ./src/extraction/data/analysis.ipynb

## Available Commands

### `task lint`
Runs style checks with `ruff`:
```bash
task lint
```
- **`ruff check .`**: Checks for style issues.
- **`ruff format . --diff`**: Displays suggested changes.

### `task format`
Applies automatic fixes:
```bash
task format
```
- **`ruff check . --fix`**: Fixes style issues.
- **`ruff format .`**: Formats the code.

### `task del_cache`
Removes cache files:
```bash
task del_cache
```
- Deletes `__pycache__`, `.pyc`, `.pyo`, `.mypy`, and `.ruff` files.
