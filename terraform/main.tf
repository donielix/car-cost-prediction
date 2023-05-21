provider "aws" {
  region = "eu-west-3"
}

resource "aws_s3_bucket" "citroen-cost-prediction" {
  bucket = "citroen-cost-prediction"

  tags = {
    Name = "citroen-cost-prediction"
  }
}

resource "aws_s3_bucket_acl" "citroen-cost-prediction" {
  bucket = aws_s3_bucket.citroen-cost-prediction.id
  acl = "private"
}

resource "aws_s3_object" "raw-data" {
  bucket = aws_s3_bucket.citroen-cost-prediction.id
  key = "raw-data"
  content = "This is the raw data folder"
}

resource "aws_s3_object" "proccesed-data" {
  bucket = aws_s3_bucket.citroen-cost-prediction.id
  key = "proccesed-data"
  content = "This is the proccesed data folder"
}

resource "aws_s3_object" "dedup-data" {
  bucket = aws_s3_bucket.citroen-cost-prediction.id
  key = "dedup-data"
  content = "This is the dedup data folder"
}
