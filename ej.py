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
                letter = "<SPACE>"  # Indicateur spécial pour l'espace
            elif letter == "\n":
                letter = "<NEWLINE>"  # Indicateur pour les sauts de ligne

            print(f"Writing to file: {letter} -> {code}")  # Debugging
            f.write(f"{letter} {code} ")
        f.write("\n")

        for letter in content:
            encoded_char = final_dict.get(letter, "")
            f.write(encoded_char)


def compress_file(path: str):
    content = read_file(path)
    letter_counts = count_letters(content)
    lst = dictionary_to_list(letter_counts)
    tree = build_tree(lst)
    final_dict = generate_huffman_codes(tree[0], {}, "")
    write_compressed(content, path, final_dict)


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


def decompress_file(path):
    with open("test2.txt", "r", encoding="utf-8") as f:
        line = f.readline()
        elements = line.strip().split()
        print(f"Elements list from file: {elements}")  # Debugging

        # Vérifier que la liste a bien un nombre pair d'éléments
        if len(elements) % 2 != 0:
            raise ValueError("Error: Huffman table in test2.txt is malformed.")

        dictionary = {}
        i = 0
        while i < len(elements):
            char = elements[i]
            code = elements[i + 1]

            # Correction : Remplacer "<SPACE>" par un vrai espace
            if char == "<SPACE>":
                char = " "
            elif char == "<NEWLINE>":
                char = "\n"

            dictionary[char] = code
            i += 2  # Avancer de 2 pour éviter les erreurs d'index

        encoded_text = f.read()
        reverse_dict = reverse_dictionary(dictionary)
        decoded_text = decode_text(reverse_dict, encoded_text)

        # Affichage pour vérifier le texte final
        print(f"Decoded text: {repr(decoded_text)}")

        write_decompressed(decoded_text, path)


def test_huffman():
    test_input = "test_input.txt"
    test_output = "test_output.txt"
    test_text = "hello huffman compression"
    
    with open(test_input, 'w', encoding='utf-8') as f:
        f.write(test_text)
    
    compress_file(test_input)
    decompress_file(test_output)
    
    with open(test_output, 'r', encoding='utf-8') as f:
        decompressed_text = f.read()
    
    assert decompressed_text == test_text, "Decompression did not match original text!"
    print("Test passed: Huffman compression and decompression work correctly.")

test_huffman()

test_huffman()
