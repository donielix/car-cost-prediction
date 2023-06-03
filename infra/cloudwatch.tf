resource "aws_cloudwatch_log_group" "lambda_processing_logs" {
  name              = "/aws/lambda/${aws_lambda_function.processing_lambda_function.function_name}"
  retention_in_days = 10
}

resource "aws_cloudwatch_log_group" "lambda_dedup_logs" {
  name              = "/aws/lambda/${aws_lambda_function.dedup_lambda_function.function_name}"
  retention_in_days = 10
}

resource "aws_cloudwatch_event_rule" "daily_lambda_dedup" {
  name        = var.eventbridge_name
  description = "Event rule for daily lambda deduplication"
  schedule_expression = "cron(0 12 * * ? *)"

  tags = {
    Name = "daily-lambda-dedup"
  }
}

resource "aws_cloudwatch_event_target" "lambda_dedup_target" {
  rule      = aws_cloudwatch_event_rule.daily_lambda_dedup.name
  target_id = "lambda-dedup"
  arn       = aws_lambda_function.dedup_lambda_function.arn
}
