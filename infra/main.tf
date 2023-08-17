terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.1"
    }
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.42.1"
    }
    tls = {
      source = "hashicorp/tls"
      version = "~> 4.0.4"
    }
  }
}

provider "aws" {
  region = var.region
}

# Configure the Hetzner Cloud Provider
provider "hcloud" {
  token = var.HETZNER_API_KEY # You need to define an environment variable called TF_VAR_HETZNER_API_KEY
}

provider "tls" {
  // no config needed
}
