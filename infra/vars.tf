variable "region" {
  default     = "eu-west-3"
  description = "The AWS region to use"
  type        = string
}

variable "app_bucket_name" {
  default     = "citroen-cost-prediction"
  description = "The name of the bucket for the app"
  type        = string
}

variable "raw_data_name" {
  default     = "raw-data"
  description = "The name for the raw data folder"
  type        = string
}

variable "processed_data_name" {
  default     = "processed-data"
  description = "The name for the processed data folder"
  type        = string
}

variable "dedup_data_name" {
  default     = "dedup-data"
  description = "The name for the deduplicated data folder"
  type        = string
}

variable "mlflow_artifacts" {
  default     = "artifacts"
  description = "The name for the mlflow artifacts folder"
  type        = string
}

variable "dvc_data" {
  default     = "dvc-data"
  description = "The name for the dvc data folder"
  type        = string
}
variable "glue_database" {
  default     = "citroen_database"
  description = "The name of the AWS Glue Catalog Database"
  type        = string
}

variable "glue_table" {
  default     = "citroen_table"
  description = "The name of the AWS Glue Catalog Table"
  type        = string
}

variable "lambda_runtime" {
  default     = "python3.9"
  description = "The runtime for AWS Lambda"
  type        = string

}

variable "lambda_processing_name" {
  default     = "citroen-s3-processing"
  description = "The name of the AWS Lambda processing function"
  type        = string
}

variable "lambda_dedup_name" {
  default     = "citroen-s3-deduplication"
  description = "The name of the AWS Lambda deduplicating function"
  type        = string
}

variable "eventbridge_name" {
  default     = "daily-lambda-dedup"
  description = "The name of the EventBridge resource"
  type        = string
}

variable "lambda_timeout" {
  default     = 180
  description = "Number of seconds for Lambda timeout"
  type        = number
}

variable "athena_workgroup_name" {
  default     = "citroen_workgroup"
  description = "The name for the workgroup for Athena"
  type        = string
}

variable "HETZNER_API_KEY" {
  description = "API key for Hetzner cloud provider"
  type        = string
  sensitive   = true
}

variable "AWS_ACCESS_KEY_ID" {
  type      = string
  sensitive = true
}

variable "AWS_SECRET_ACCESS_KEY" {
  type      = string
  sensitive = true
}


variable "AWS_DEFAULT_REGION" {
  type      = string
  sensitive = true
}
