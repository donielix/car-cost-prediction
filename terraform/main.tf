provider "aws" {
  region = "eu-west-3"
}

module "s3_module" {
  source = "./s3"
}
