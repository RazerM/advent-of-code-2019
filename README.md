# Installation

```bash
git clone https://github.com/RazerM/advent-of-code-2019
cd advent-of-code-2019
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

# Download input

Set the `AOC_SESSION` environment variable to the value of your
https://adventofcode.com `session` cookie.

```bash
./aoc.py download 1 input/1.txt
```

# Running

```bash
./aoc.py run 1 input/1.txt
```

# Tests

```bash
pip install -e .[test]
pytest tests/
```
