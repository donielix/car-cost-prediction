import json
import os
import awswrangler as wr


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    INPUT_PATH = os.environ["INPUT_PATH"]
    OUTPUT_PATH = os.environ["OUTPUT_PATH"]
    ATHENA_DATABASE = os.environ["ATHENA_DATABASE"]
    ATHENA_TABLE = os.environ["ATHENA_TABLE"]
    ATHENA_WORKGROUP = os.environ["ATHENA_WORKGROUP"]
    print("Reading data...")
    df = wr.s3.read_parquet(INPUT_PATH, dataset=True)
    print("Done!")
    print("Removing duplicates...")
    df.drop_duplicates(inplace=True)
    print("Done!")
    print("Writing to parquet...")
    wr.s3.to_parquet(
        df,
        path=OUTPUT_PATH,
        dataset=True,
        partition_cols=["year", "month"],
        mode="overwrite",
        dtype={
            "fecha": "date",
            "hora_salida": "string",
            "hora_llegada": "string",
            "direccion_origen": "string",
            "direccion_destino": "string",
            "distancia": "double",
            "kilometraje": "int",
            "consumo_medio": "double",
            "precio_carburante": "double",
            "coste": "double",
            "year": "string",
            "month": "string",
        },
    )
    SQL = f"MSCK REPAIR TABLE {ATHENA_DATABASE}.{ATHENA_TABLE}"
    print(f"Repairing table with: {SQL}")
    result = wr.athena.start_query_execution(
        sql=SQL, workgroup=ATHENA_WORKGROUP, wait=True
    )
    print(f"Reparinig result: {result}")
    print("Done!")
    return {
        "status": 201,
    }
