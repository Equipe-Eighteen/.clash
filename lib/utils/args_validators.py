import os
import argparse

def clash_file(filename: str) -> str:
    if not filename.endswith(".clash"):
        raise argparse.ArgumentTypeError("The file must have a .clash extension.")
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(f"The file '{filename}' was not found.")
    return filename
