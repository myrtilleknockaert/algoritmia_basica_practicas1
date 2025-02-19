#!/bin/bash

# Vérifier que l'argument est fourni
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 -c <file>  (to compress)"
    echo "       $0 -d <file.huf>  (to decompress)"
    exit 1
fi

# Définition du fichier Python contenant les fonctions Huffman
HUFFMAN_SCRIPT="huf.py"

# Récupérer l'option (-c pour compression, -d pour décompression)
OPTION=$1
FILE=$2

# Vérifier que le fichier existe
if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found!"
    exit 1
fi

# Exécuter la compression ou la décompression
if [ "$OPTION" == "-c" ]; then
    echo "Compressing '$FILE'..."
    python3 "$HUFFMAN_SCRIPT" -c "$FILE"
    echo "Compression complete: '$FILE.huf'"

elif [ "$OPTION" == "-d" ]; then
    echo "Decompressing '$FILE'..."
    python3 "$HUFFMAN_SCRIPT" -d "$FILE"
    echo "Decompression complete: '${FILE%.huf}.orig'"

else
    echo "Invalid option: $OPTION"
    echo "Use -c to compress or -d to decompress."
    exit 1
fi
