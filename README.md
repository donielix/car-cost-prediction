# Pulling Script

The `pull.py` script pulls data from AWS Athena, saves it as train and test sets in parquet format, and stores them in a specified path.

## Installation

To run the script, you'll need Python 3 and the following packages:

- `awswrangler`
- `pandas`
- `scikit-learn`

To install the required packages, run:

```bash
pip install awswrangler pandas scikit-learn
```

## Usage

To use the script, run the following command in your terminal:

```bash
python pull.py [-h] [-d DATA] [--database DATABASE]
```

The script takes the following arguments:

- `-h` or `--help`: shows a help message and exits.
- `-d DATA` or `--data DATA`: specifies the path where the pulled data will be stored. Default: `<current working directory>/data`.
- `--database DATABASE`: specifies the AWS Glue database to pull data from. Default: `citroen-database`.

## Behaviour

The `pull.py` script performs the following steps:

1. Reads an SQL query from the `data.sql` file located in the same directory as the script.
2. Executes the SQL query in AWS Athena using the `awswrangler` package.
3. Splits the resulting data into train and test sets using the `train_test_split` function from the `scikit-learn` package.
4. Saves the train and test sets as parquet files in the specified path (`<path>/train.parquet` and `<path>/test.parquet`, respectively), using the `to_parquet` method from the `pandas` package.

Note that the SQL query used in the script selects columns `distancia`, `kilometraje`, `consumo_medio`, `precio_carburante`, and `coste` from the `citroen_processed` table in the specified AWS Glue database where `distancia` is greater than 1.
