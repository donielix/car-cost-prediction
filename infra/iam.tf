resource "aws_iam_role" "iam_lambda_processing" {
  name = "iam_lambda_processing"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role" "iam_lambda_dedup" {
  name = "iam_lambda_dedup"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

data "aws_iam_policy_document" "lambda_processing_policy" {
  # IAM Policy data for processing Lambda
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "s3:PutObject",
      "s3:GetObject",
      "s3:ListBucket"
    ]

    resources = [
      "arn:aws:logs:*:*:*",
      aws_s3_bucket.citroen-cost-prediction.arn,
      "${aws_s3_bucket.citroen-cost-prediction.arn}/*"
    ]
  }
}

data "aws_iam_policy_document" "lambda_dedup_policy" {
  # IAM Policy data for dedup Lambda
  statement {
    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "arn:aws:logs:*:*:*"
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:*",
      "athena:*",
      "glue:*"
    ]

    resources = [
      "*"
    ]
  }
}

resource "aws_iam_policy" "lambda_processing_policy" {
  name        = "lambda_processing_policy"
  path        = "/"
  description = "IAM policy for lambda processing"
  policy      = data.aws_iam_policy_document.lambda_processing_policy.json
}

resource "aws_iam_policy" "lambda_dedup_policy" {
  name        = "lambda_dedup_policy"
  path        = "/"
  description = "IAM policy for lambda dedup"
  policy      = data.aws_iam_policy_document.lambda_dedup_policy.json
}

resource "aws_iam_role_policy_attachment" "lambda_processing_logs" {
  # Attach the processing Lambda policy to the processing Lambda role
  role       = aws_iam_role.iam_lambda_processing.name
  policy_arn = aws_iam_policy.lambda_processing_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_dedup_logs" {
  role       = aws_iam_role.iam_lambda_dedup.name
  policy_arn = aws_iam_policy.lambda_dedup_policy.arn
}
