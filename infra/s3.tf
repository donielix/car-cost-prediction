resource "aws_s3_bucket" "citroen-cost-prediction" {
  bucket = var.app_bucket_name

  tags = {
    Name = var.app_bucket_name
  }
}

resource "aws_s3_bucket_acl" "citroen-cost-prediction-acl" {
  bucket = aws_s3_bucket.citroen-cost-prediction.id
  acl    = "private"
}

resource "aws_s3_object" "raw-data" {
  bucket  = aws_s3_bucket.citroen-cost-prediction.id
  key     = var.raw_data_name
  content = "This is the raw data folder"
}

resource "aws_s3_object" "processed-data" {
  bucket  = aws_s3_bucket.citroen-cost-prediction.id
  key     = var.processed_data_name
  content = "This is the proccesed data folder"
}

resource "aws_s3_object" "dedup-data" {
  bucket  = aws_s3_bucket.citroen-cost-prediction.id
  key     = var.dedup_data_name
  content = "This is the dedup data folder"
}

resource "aws_s3_object" "mlflow-artifacts" {
  bucket  = aws_s3_bucket.citroen-cost-prediction.id
  key     = var.mlflow_artifacts
  content = "This is the mlflow artifacts folder"
}

resource "aws_s3_object" "dvc-data" {
  bucket  = aws_s3_bucket.citroen-cost-prediction.id
  key     = var.dvc_data
  content = "This is the dvc data folder"
}
