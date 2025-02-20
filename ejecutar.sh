#!/bin/bash


# Check if Python3 is installed, if not, install it
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Installing it now..."
    
    if [ -f /etc/debian_version ]; then
        sudo apt update && sudo apt install -y python3
    elif [ -f /etc/arch-release ]; then
        sudo pacman -Sy --noconfirm python
    elif [ -f /etc/fedora-release ]; then
        sudo dnf install -y python3
    elif command -v brew &> /dev/null; then
        brew install python
    else
        echo "Error: Could not determine package manager. Install Python3 manually."
        exit 1
    fi
fi

# Verify correct number of arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 -c <file>              (to compress)"
    echo "       $0 -d <file.huf>         (to decompress)"
    echo "       $0 -l <max_length> -c <file> (to compress with limited length)"
    exit 1
fi

# Declare script variables
HUFFMAN_SCRIPT="huf.py"
LENGTH_SCRIPT="length.py"
MAX_LENGTH=""
FILE=""
MODE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -c)  # Compression
            MODE="compress"
            FILE="$2"
            shift 2
            ;;
        -d)  # Decompression
            MODE="decompress"
            FILE="$2"
            shift 2
            ;;
        -l)  # Length-limited compression
            MAX_LENGTH="$2"
            shift 2
            ;;
        *)
            echo "Invalid option: $1"
            echo "Usage: $0 -c <file>              (to compress)"
            echo "       $0 -d <file.huf>         (to decompress)"
            echo "       $0 -l <max_length> -c <file> (to compress with limited length)"
            exit 1
            ;;
    esac
done

# Verify that a file is provided
if [ -z "$FILE" ]; then
    echo "Error: No file specified!"
    exit 1
fi

# Verify that the file exists
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found!"
    exit 1
fi

# Execute the requested action
if [ "$MODE" == "compress" ]; then
    if [ -n "$MAX_LENGTH" ]; then
        echo "Compressing '$FILE' with max length $MAX_LENGTH..."
        python3 "$LENGTH_SCRIPT" "$FILE" "$MAX_LENGTH"
        echo "Compression with limited length complete: '$FILE.huf'"
    else
        echo "Compressing '$FILE'..."
        python3 "$HUFFMAN_SCRIPT" -c "$FILE"
        echo "Compression complete: '$FILE.huf'"
    fi

elif [ "$MODE" == "decompress" ]; then
    echo "Decompressing '$FILE'..."
    python3 "$HUFFMAN_SCRIPT" -d "$FILE"
    echo "Decompression complete: '${FILE%.huf}'"

else
    echo "Error: No valid action specified."
    exit 1
fi
