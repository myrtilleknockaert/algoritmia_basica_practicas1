import json
import collections


def read_file(path: str) -> str:
    """
    Reads a file and returns its content as a string.
    Replaces non-breaking spaces and newlines with spaces.
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        # Replace non-breaking spaces (\xa0) and newlines (\n)
        content = content.replace("\xa0", " ").replace("\n", " ")
    return content


def count_letters(content: str) -> dict:
    """
    Counts the frequency of each letter in the content and returns a dictionary with the letter as the key
    """
    letter_counts = collections.Counter(content)
    return letter_counts


def dictionary_to_list(letter_counts: dict) -> list:
    """
    Converts a dictionary of letter frequencies to a list of lists with the format [frequency, letter, "f"].
    """
    lst = [[freq, letter, "f"] for letter, freq in letter_counts.items()]
    lst.sort()
    return lst


def build_tree(lst: list) -> list:
    """
    buid a huffman tree from a list of lists
    """
    while len(lst) > 1:
        first = lst.pop(0)
        second = lst.pop(0)
        lst.append([first[0] + second[0], first, second])
        lst.sort(key=lambda x: x[0])
    return lst


def generate_huffman_codes(tree, final_dict, code):
    """
    Fixes infinite recursion by ensuring proper termination.
    """
    stack = [(tree, code)]
    while stack:
        node, code = stack.pop()
        if len(node) == 3 and node[2] == "f":
            final_dict[node[1]] = code
        else:
            stack.append((node[1], code + "0"))
            stack.append((node[2], code + "1"))
    return final_dict


def write_compressed(content, final_dict):
    with open("test2.txt", "w", encoding="utf-8") as f:
        for letter, code in final_dict.items():
            if letter == " ":
                letter = "<SPACE>"
            elif letter == "\n":
                letter = "<NEWLINE>"
            f.write(f"{letter} {code} ")
        f.write("\n")

        for letter in content:
            encoded_char = final_dict.get(letter, "")
            f.write(encoded_char)


def compress_file(input_path, output_path):
    """
    read the file, count the frequency of each letter, build the huffman tree, generate the huffman codes and compress the text
    """
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    frequencies = count_letters(content)  # step 1: count the frequency of each letter
    sorted_list = dictionary_to_list(
        frequencies
    )  # step 2: convert the dictionary to a list and sort it
    huffman_tree = build_tree(sorted_list)  # step 3: build the huffman tree
    huffman_codes = generate_huffman_codes(
        huffman_tree[0], {}, ""
    )  # step 4: generate the huffman codes

    compressed_text = "".join(
        huffman_codes[c] for c in content
    )  # step 5: compress the text

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(huffman_codes, f)  # save the huffman tree in the header
        f.write("\n")  # separate the header from the compressed text
        f.write(compressed_text)


def reverse_dictionary(dictionary: dict) -> dict:
    return {code: letter for letter, code in dictionary.items()}


def decode_text(reverse_dict, encoded_text):
    decoded_text = ""
    buffer = ""
    for bit in encoded_text:
        buffer += bit
        if buffer in reverse_dict:
            decoded_text += reverse_dict[buffer]
            buffer = ""
    return decoded_text


def write_decompressed(text, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def decompress_file(input_path, output_path):
    """read a compressed file (.huf), get the huffmantree et decode the text"""
    with open(input_path, "r", encoding="utf-8") as f:
        # read the huffman tree from the header
        huffman_tree = json.loads(f.readline().strip())

        compressed_text = f.read()

    # inverse the huffman tree to decode the text
    reverse_tree = {code: char for char, code in huffman_tree.items()}

    # decode the text
    buffer = ""
    decompressed_text = ""
    for bit in compressed_text:
        buffer += bit
        if buffer in reverse_tree:
            decompressed_text += reverse_tree[buffer]
            buffer = ""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decompressed_text)
