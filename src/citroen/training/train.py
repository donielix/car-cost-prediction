#!/usr/bin/env python3

import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Training script",
        description="Fits the model according to the data passed",
        epilog="End of help",
    )
    parser.add_argument(
        "--training-data", type=str, required=True, help="Source path for training data"
    )
    parser.add_argument(
        "--hyperparams-file",
        type=str,
        required=True,
        help="Source path for hyperparameters file",
    )
    parser.add_argument(
        "--artifacts-data",
        type=str,
        required=True,
        help="Path where to store output artifacts",
    )
