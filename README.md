# TableKit — Python Table Manipulation Package

A lightweight, pure-Python library for loading, transforming, and saving tabular data — built on top of `csv`, `pickle`, and native file I/O. No external dependencies.

```python
table = load_table("data.csv")
set_column_types({0: int, 1: float, 2: str})
filtered = filter_rows(gr(get_values(1), 3.5))
save_table(filtered, "output.csv")
```

---

## Features

### I/O
| Function | Description |
|----------|-------------|
| `load_table(file1, ...)` | Load from one or multiple CSV / pickle files; validates column structure across files |
| `save_table(table, file, max_rows=None)` | Save to one file or split across multiple files by row limit |

### Row & Column Access
| Function | Description |
|----------|-------------|
| `get_rows_by_number(start, stop, copy_table)` | Slice rows by index; returns a view or a deep copy |
| `get_rows_by_index(val1, ..., copy_table)` | Filter rows by first-column value; view or copy |
| `get_values(column)` | Get a typed list of values from a column (by index or name) |
| `get_value(column)` | Single-row variant — returns one typed value |
| `set_values(values, column)` | Write a list of values to a column |
| `set_value(value, column)` | Single-row variant — write one value |
| `print_table()` | Pretty-print the table to stdout |

### Type System
| Function | Description |
|----------|-------------|
| `get_column_types(by_number)` | Returns `{column: type}` dict; supports `int`, `float`, `bool`, `str`, `datetime` |
| `set_column_types(types_dict, by_number)` | Set types manually |
| `detect_types()` | Auto-detect column types from stored values; also available as `load_table(..., detect_types=True)` |

### Arithmetic (numeric columns)
```python
add(table, col_a, col_b)   # col_a + col_b
sub(table, col_a, col_b)   # col_a - col_b
mul(table, col_a, col_b)   # col_a * col_b
div(table, col_a, col_b)   # col_a / col_b  (raises on division by zero)
```

### Comparison & Filtering
```python
eq(col, value)   # ==       gr(col, value)   # >
ls(col, value)   # <        ge(col, value)   # >=
le(col, value)   # <=       ne(col, value)   # !=

filter_rows(bool_list, copy_table=False)   # keep rows where True
```

### Table Operations
| Function | Description |
|----------|-------------|
| `concat(table1, table2)` | Stack two tables vertically |
| `split(row_number)` | Split one table into two at a given row |
| `merge_tables(table1, table2, by_number=True)` | Join tables by row number or index column; conflict resolution via parameters |

### Extra
- **`None` support** — empty cells load as `None`; all get/set/arithmetic operations handle `None` gracefully
- **`datetime` column type** — full support via Python's `datetime` module
- **Exception handling** — every function raises descriptive errors on bad input, type mismatches, or structural conflicts

---

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/tablekit.git
cd tablekit
python main.py
```

No dependencies beyond the Python standard library.

---

## Quick Example

```python
from tablekit import load_table, get_rows_by_index, set_column_types, filter_rows, gr, save_table

# Load and merge two CSV shards
table = load_table("test.csv", "test2.csv")

# Set types
set_column_types({0: int, 1: str, 2: float}, by_number=True)

# Filter rows where column 2 > 3.5
result = filter_rows(gr(2, 3.5))

# Save split across files of max 100 rows each
save_table(result, "output.csv", max_rows=100)
```

---

## Project Structure

```
tablekit/
├── main.py          # Demo script covering all features
├── tablekit/
│   ├── __init__.py
│   ├── io.py        # load_table, save_table (CSV, pickle, multi-file)
│   ├── access.py    # get/set rows, columns, values
│   ├── types.py     # get/set column types, auto-detection, datetime support
│   ├── ops.py       # add, sub, mul, div, eq, gr, ls, ge, le, ne, filter_rows
│   └── table.py     # concat, split, merge_tables, None handling
├── test.csv         # Sample dataset
└── test.dump        # Sample pickle file (same data as test.csv)
```

---

## Author

**Manaeva Daria** 


