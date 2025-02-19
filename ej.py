import json
import unicodedata
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


def build_tree(lst):
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


def write_compressed(content, path, final_dict):
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
    """Lit un fichier, compresse son contenu avec Huffman et stocke l’arbre en en-tête"""
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    frequencies = count_letters(content)  # Étape 1 : Compter la fréquence des lettres
    sorted_list = dictionary_to_list(frequencies)  # Étape 2 : Générer la liste triée
    huffman_tree = build_tree(sorted_list)  # Étape 3 : Construire l'arbre Huffman
    huffman_codes = generate_huffman_codes(huffman_tree[0], {}, "")  # Étape 4 : Générer les codes

    compressed_text = "".join(huffman_codes[c] for c in content)  # Étape 5 : Encoder le texte

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(huffman_codes, f)  # Sauvegarde de la table de codage en en-tête
        f.write("\n")  # Séparation entre l'en-tête et le texte compressé
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


# def decompress_file(path):
#     with open("test2.txt", "r", encoding="utf-8") as f:
#         line = f.readline()
#         elements = line.strip().split()

#         # verify that the list har a pair number of elements
#         if len(elements) % 2 != 0:
#             raise ValueError("Error: Huffman table in test2.txt is malformed.")

#         dictionary = {}
#         i = 0
#         while i < len(elements):
#             char = elements[i]
#             code = elements[i + 1]

#             # replace special indicators
#             if char == "<SPACE>":
#                 char = " "
#             elif char == "<NEWLINE>":
#                 char = "\n"

#             dictionary[char] = code
#             i += 2  # jump to the next pair

#         encoded_text = f.read()
#         reverse_dict = reverse_dictionary(dictionary)
#         decoded_text = decode_text(reverse_dict, encoded_text)

#         # verify that the decoded text is the same as the original text
#         print(f"Decoded text: {repr(decoded_text)}")

#         write_decompressed(decoded_text, path)


def decompress_file(input_path, output_path):
    """Lit un fichier compressé (.huf), récupère l’arbre Huffman et décompresse le texte"""
    with open(input_path, "r", encoding="utf-8") as f:
        # Lire l'arbre Huffman depuis l'en-tête
        huffman_tree = json.loads(f.readline().strip())

        compressed_text = f.read()

    # Inverser la table de Huffman pour décoder
    reverse_tree = {code: char for char, code in huffman_tree.items()}

    # Décoder le texte
    buffer = ""
    decompressed_text = ""
    for bit in compressed_text:
        buffer += bit
        if buffer in reverse_tree:
            decompressed_text += reverse_tree[buffer]
            buffer = ""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decompressed_text)


# def test_huffman():
#     test_input = "test_input.txt"
#     test_output = "test_output.txt"
#     test_text = "hello huffman compression"

#     with open(test_input, "w", encoding="utf-8") as f:
#         f.write(test_text)

#     compress_file(test_input, test_output)
#     decompress_file(test_output)

#     with open(test_output, "r", encoding="utf-8") as f:
#         decompressed_text = f.read()

#     assert decompressed_text == test_text, "Decompression did not match original text!"
#     print("Test passed: Huffman compression and decompression work correctly.")
