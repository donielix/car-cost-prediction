import json
import os
import urllib.parse
import awswrangler as wr


def lambda_handler(event, context):
    """
    This function is a Lambda function that processes CSV data from S3 and writes
    it to Parquet format to another S3 path.

    Args
    ----
    * `event`: The event object from AWS Lambda.
    * `context`: The context object from AWS Lambda.

    It does the following:

    1. Loads the CSV data from S3.
    2. Renames the columns.
    3. Drops unneeded columns.
    4. Performs some transformations.
    5. Enforces the schema.
    6. Adds partition columns.
    7. Writes the data to Parquet format.

    Returns
    -------
    * A dictionary with a status code of 201
    """
    print("Received event: " + json.dumps(event))
    OUTPUT_PATH = os.environ["OUTPUT_PATH"]
    # Get the object from the event and show its content type
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )
    full_path = f"s3://{bucket}/{key}"
    print("Loading object...")
    df = wr.s3.read_csv(
        full_path,
        sep=";",
        decimal=",",
        thousands=".",
        parse_dates=["fecha"],
        dayfirst=True,
    )
    print("Done!")
    print("Renaming columns...")
    df.rename(
        columns={
            "hora de salida": "hora_salida",
            "hora de llegada": "hora_llegada",
            "duración": "duracion",
            "dirección de origen": "direccion_origen",
            "dirección de destino": "direccion_destino",
            "Kilometraje en el contador (km)": "kilometraje",
            "consumo medio (l/100km)": "consumo_medio",
            "precio del carburante (EUR/l)": "precio_carburante",
            "coste (EUR)": "coste",
            "categoría": "categoria",
        },
        inplace=True,
    )
    print("Done!")
    print("Droping unneeded columns...")
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df.drop(columns=["categoria", "duracion"], inplace=True)
    print("Done!")
    print("Performing some transformations...")
    df["consumo_medio"] = df["consumo_medio"] / 100
    print("Enforcing schema...")
    df = df.astype(
        {
            "fecha": "datetime64[ns]",
            "hora_salida": "string",
            "hora_llegada": "string",
            "direccion_origen": "string",
            "direccion_destino": "string",
            "kilometraje": "int32",
            "consumo_medio": "float64",
            "precio_carburante": "float64",
            "coste": "float64",
        }
    )
    print("Done!")
    print("Adding partition columns...")
    df["year"] = df.fecha.dt.year
    df["month"] = df.fecha.dt.month
    print("Done!")
    print("Writing to parquet...")
    wr.s3.to_parquet(
        df,
        path=OUTPUT_PATH,
        dataset=True,
        partition_cols=["year", "month"],
        mode="append",
    )
    print("Done!")
    return {"status": 201}
