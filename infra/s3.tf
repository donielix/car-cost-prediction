# Create an S3 bucket for Citroen cost prediction
resource "aws_s3_bucket" "citroen-cost-prediction" {
  bucket        = var.app_bucket_name # The name of the bucket specified as a variable
  force_destroy = true                # Enable forceful deletion of the bucket

  tags = {
    Name = var.app_bucket_name # Add a tag to the bucket with the same name as the bucket
  }
}

# Create an S3 object for raw data
resource "aws_s3_object" "raw-data" {
  bucket       = aws_s3_bucket.citroen-cost-prediction.id # The ID of the S3 bucket created above
  key          = "${var.raw_data_name}/"                  # The key/path of the S3 object with a variable name for raw data
  content_type = "application/x-directory"                # Set the content type as a directory
}

# Create an S3 object for processed data
resource "aws_s3_object" "processed-data" {
  bucket       = aws_s3_bucket.citroen-cost-prediction.id # The ID of the S3 bucket created above
  key          = "${var.processed_data_name}/"            # The key/path of the S3 object with a variable name for processed data
  content_type = "application/x-directory"                # Set the content type as a directory
}

# Create an S3 object for deduped data
resource "aws_s3_object" "dedup-data" {
  bucket       = aws_s3_bucket.citroen-cost-prediction.id # The ID of the S3 bucket created above
  key          = "${var.dedup_data_name}/"                # The key/path of the S3 object with a variable name for deduped data
  content_type = "application/x-directory"                # Set the content type as a directory
}

# Create an S3 object for MLflow artifacts
resource "aws_s3_object" "mlflow-artifacts" {
  bucket       = aws_s3_bucket.citroen-cost-prediction.id # The ID of the S3 bucket created above
  key          = "${var.mlflow_artifacts}/"               # The key/path of the S3 object with a variable name for MLflow artifacts
  content_type = "application/x-directory"                # Set the content type as a directory
}

# Create an S3 object for DVC data
resource "aws_s3_object" "dvc-data" {
  bucket       = aws_s3_bucket.citroen-cost-prediction.id # The ID of the S3 bucket created above
  key          = "${var.dvc_data}/"                       # The key/path of the S3 object with a variable name for DVC data
  content_type = "application/x-directory"                # Set the content type as a directory
}

# Create an S3 bucket notification to trigger a Lambda function when an object is created in the bucket
resource "aws_s3_bucket_notification" "s3_trigger_lambda_processing" {
  bucket     = aws_s3_bucket.citroen-cost-prediction.id # The ID of the S3 bucket created above
  depends_on = [aws_lambda_permission.s3_trigger]       # Make sure to wait for the Lambda permission to be set

  lambda_function {
    lambda_function_arn = aws_lambda_function.processing_lambda_function.arn # The ARN of the Lambda function to be triggered
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".csv"
    filter_prefix       = var.raw_data_name
  }
}
