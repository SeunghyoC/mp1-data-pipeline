# MP1 Data Pipeline

This pipeline loads a data file, validates it, cleans it, and saves the result as a CSV. The data moves in this order: load, validate, process, then save. `pipeline.py` runs each step, and the settings come from `config/config.yaml`. The modules are in `src/`: `data_loaders.py` loads files, `data_validator.py` checks the data, `data_processor.py` cleans it, `data_output.py` saves it, and `utils.py` sets up logging and checks file paths. `src/__init__.py` lets `pipeline.py` import all of these in one line. Sample data is in `fixtures/`, and the cleaned file goes to `output/`.

## Example

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

```text
01:53:25 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
01:53:25 INFO     src.utils — Input file validated: fixtures/sample_data.csv
01:53:25 INFO     src.utils — Input file validated: config/config.yaml
01:53:25 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
01:53:25 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
01:53:25 WARNING  src.data_validator — Invalid numeric value in rating at row 94: not_available
01:53:25 WARNING  src.data_validator — Invalid numeric value in rating at row 95: error
01:53:25 DEBUG    src.data_validator — Validation: 100 -> 98 rows (removed 2)
01:53:25 INFO     __main__ — Validation complete: 100 -> 98 rows
01:53:25 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows (removed 2)
01:53:25 DEBUG    src.data_processor — handle_missing: 96 → 94 rows (removed 2)
01:53:25 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
01:53:25 INFO     __main__ — Processing complete: 98 → 92 rows
01:53:25 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
01:53:25 INFO     __main__ — Saved cleaned data to output/clean.csv
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```