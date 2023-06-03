variable "app_bucket_name" {
  default = "citroen-cost-prediction"
  description = "The name of the bucket for the app"
  type = string
}

variable "raw_data_name" {
  default = "raw-data"
  description = "The name for the raw data folder"
  type = string
}

variable "processed_data_name" {
  default = "processed-data"
  description = "The name for the processed data folder"
  type = string
}

variable "dedup_data_name" {
  default = "dedup-data"
  description = "The name for the deduplicated data folder"
  type = string
}