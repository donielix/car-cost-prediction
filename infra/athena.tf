resource "aws_athena_workgroup" "citroen_workgroup" {
  name = var.athena_workgroup_name
  force_destroy = true

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.citroen-cost-prediction.bucket}/athena_output/"
    }
  }
}
