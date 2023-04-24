#!/usr/bin/env bash
# Starts a local MLFlow server, with remote storage for artifacts on S3
# An instance of PostgreSQL must be running on port 5432
set -e

mlflow server --backend-store-uri postgresql://mlflow:mlflow@localhost:5432/mlflowdb --default-artifact-root s3://citroen-cost-prediction/artifacts