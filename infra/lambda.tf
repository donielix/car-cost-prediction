data "archive_file" "processing_lambda_function" {
  type        = "zip"
  source_file = "../lambda/processing.py"
  output_path = "${var.lambda_processing_name}.zip"
}

resource "aws_lambda_function" "processing_lambda_function" {
  filename         = data.archive_file.processing_lambda_function.output_path
  function_name    = var.lambda_processing_name
  handler          = "processing.lambda_handler"
  runtime          = "python3.10"
  role             = aws_iam_role.iam_lambda_processing.arn
  source_code_hash = data.archive_file.lambda_function_file.output_base64sha256
  memory_size      = 1024
  timeout          = 3
  layers           = ["arn:aws:lambda:${var.region}:336392948345:layer:AWSSDKPandas-Python39:9"]
}
