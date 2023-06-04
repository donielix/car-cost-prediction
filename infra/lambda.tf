data "archive_file" "processing_lambda_function" {
  type        = "zip"
  source_file = "./lambda/processing.py"
  output_path = "${var.lambda_processing_name}.zip"
}

data "archive_file" "dedup_lambda_function" {
  type        = "zip"
  source_file = "./lambda/dedup.py"
  output_path = "${var.lambda_dedup_name}.zip"
}

resource "aws_lambda_function" "processing_lambda_function" {
  filename         = data.archive_file.processing_lambda_function.output_path
  function_name    = var.lambda_processing_name
  handler          = "processing.lambda_handler"
  runtime          = var.lambda_runtime
  role             = aws_iam_role.iam_lambda_processing.arn
  source_code_hash = data.archive_file.processing_lambda_function.output_base64sha256
  memory_size      = 1024
  timeout          = var.lambda_timeout
  layers           = ["arn:aws:lambda:${var.region}:336392948345:layer:AWSSDKPandas-Python39:9"]
  environment {
    variables = {
      OUTPUT_PATH = "s3://${aws_s3_object.processed-data.bucket}/${aws_s3_object.processed-data.key}"
    }
  }
}

resource "aws_lambda_function" "dedup_lambda_function" {
  filename         = data.archive_file.dedup_lambda_function.output_path
  function_name    = var.lambda_dedup_name
  handler          = "dedup.lambda_handler"
  runtime          = var.lambda_runtime
  role             = aws_iam_role.iam_lambda_dedup.arn
  source_code_hash = data.archive_file.dedup_lambda_function.output_base64sha256
  memory_size      = 1024
  timeout          = var.lambda_timeout
  layers           = ["arn:aws:lambda:${var.region}:336392948345:layer:AWSSDKPandas-Python39:9"]
  environment {
    variables = {
      INPUT_PATH       = "s3://${aws_s3_object.processed-data.bucket}/${aws_s3_object.processed-data.key}"
      OUTPUT_PATH      = "s3://${aws_s3_object.dedup-data.bucket}/${aws_s3_object.dedup-data.key}"
      ATHENA_DATABASE  = var.glue_database
      ATHENA_TABLE     = var.glue_table
      ATHENA_WORKGROUP = var.athena_workgroup_name
    }
  }
}


resource "aws_lambda_permission" "s3_trigger" {
  statement_id  = "AllowS3Trigger"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.processing_lambda_function.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.citroen-cost-prediction.arn
  depends_on    = [aws_lambda_function.processing_lambda_function]
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.dedup_lambda_function.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_lambda_dedup.arn
  depends_on    = [aws_cloudwatch_event_rule.daily_lambda_dedup]
}
