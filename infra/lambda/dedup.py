import json
import awswrangler as wr


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    INPUT_PATH = "s3://citroen-cost-prediction/proccesed-data"
    OUTPUT_PATH = "s3://citroen-cost-prediction/dedup-data"
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
    print("Done!")
    return {
        "status": 201,
    }
