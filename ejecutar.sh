#!/bin/bash

# give permission to execute the script
chmod 777 "$0"

# verify that the script is executed with the correct number of arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 -c <file>  (to compress)"
    echo "       $0 -d <file.huf>  (to decompress)"
    echo "       $0 -l <file> <max_length> (to compress with limited length)"
    exit 1
fi

# decraration of the variables
HUFFMAN_SCRIPT="huf.py"
LENGTH_SCRIPT="lenght.py"

# get the arguments (option and file)
OPTION=$1
FILE=$2

# verify that the file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found!"
    exit 1
fi

# do the compression, decompression or length-limited compression
if [ "$OPTION" == "-c" ]; then
    echo "Compressing '$FILE'..."
    python3 "$HUFFMAN_SCRIPT" -c "$FILE"
    echo "Compression complete: '$FILE.huf'"

elif [ "$OPTION" == "-d" ]; then
    echo "Decompressing '$FILE'..."
    python3 "$HUFFMAN_SCRIPT" -d "$FILE"
    echo "Decompression complete: '${FILE%.huf}.orig'"

elif [ "$OPTION" == "-l" ]; then
    if [ "$#" -lt 3 ]; then
        echo "Usage: $0 -l <file> <max_length> (to compress with limited length)"
        exit 1
    fi
    MAX_LENGTH=$3
    echo "Compressing '$FILE' with max length $MAX_LENGTH..."
    python3 "$LENGTH_SCRIPT" "$FILE" "$MAX_LENGTH"
    echo "Compression with limited length complete: '$FILE.huf'"

else
    echo "Invalid option: $OPTION"
    echo "Use -c to compress, -d to decompress, or -l for length-limited compression."
    exit 1
fi
