import argparse
import os
from ej import compress_file, decompress_file


def main():
    parser = argparse.ArgumentParser(
        description="Huffman Compression and Decompression Tool"
    )
    parser.add_argument("-c", "--compress", help="Compress a file", type=str)
    parser.add_argument("-d", "--decompress", help="Decompress a file", type=str)

    args = parser.parse_args()

    if args.compress:
        input_file = args.compress
        output_file = input_file + ".huf"

        print(f"Compressing {input_file} -> {output_file} ...")
        compress_file(input_file, output_file)
        print(f"Compression successful: {output_file}")

    elif args.decompress:
        input_file = args.decompress
        if not input_file.endswith(".huf"):
            print("❌ Error: Input file must have .huf extension for decompression.")
            return

        output_file = input_file.replace(".huf", ".orig")

        print(f"Decompressing {input_file} -> {output_file} ...")
        decompress_file(input_file, output_file)
        print(f"Decompression successful: {output_file}")

    else:
        print(
            "Error: You must specify either -c for compression or -d for decompression."
        )


if __name__ == "__main__":
    main()
