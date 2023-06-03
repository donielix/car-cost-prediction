# Create AWS Glue database
resource "aws_glue_catalog_database" "citroen_database" {
  name = var.glue_database
}

# Create AWS Glue table within the citroen-database
resource "aws_glue_catalog_table" "citroen_table" {
  database_name = aws_glue_catalog_database.citroen_database.name
  name          = var.glue_table
  description   = "Table for Citroen data"
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  # Specify the storage descriptor for the table
  storage_descriptor {
    location      = "s3://${aws_s3_object.dedup-data.bucket}/${aws_s3_object.dedup-data.key}"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    ser_de_info {
      name                  = "ParquetHiveSerDe"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
      parameters = {
        "serialization.format" = 1
      }
    }
  }

  # Specify the table columns and partition keys
  partition_keys {
    name = "year"
    type = "string"
  }

  partition_keys {
    name = "month"
    type = "string"
  }

  # Specify the table schema
  columns {
    name = "fecha"
    type = "date"
  }

  columns {
    name = "hora_salida"
    type = "string"
  }

  columns {
    name = "hora_llegada"
    type = "string"
  }

  columns {
    name = "direccion_origen"
    type = "string"
  }

  columns {
    name = "direccion_destino"
    type = "string"
  }

  columns {
    name = "distancia"
    type = "double"
  }

  columns {
    name = "kilometraje"
    type = "int"
  }

  columns {
    name = "consumo_medio"
    type = "double"
  }

  columns {
    name = "precio_carburante"
    type = "double"
  }

  columns {
    name = "coste"
    type = "double"
  }
}
