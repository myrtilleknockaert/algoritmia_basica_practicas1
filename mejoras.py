import sys
import math


def insertion_sort(liste: list[list]) -> list[list]:
    """
    sort the list of lists by the first element of each list
    """
    for i in range(1, len(liste)):
        x = liste[i]
        j = i - 1
        while j >= 0 and liste[j][0] > x[0]:
            liste[j + 1] = liste[j]
            j -= 1
        liste[j + 1] = x
    return liste


def step_1(liste: list[list], L: int) -> list[list]:
    """
    Limit the maximum length of the code to L
    """
    for i in range(len(liste) - 1, -1, -1):
        if liste[i][0] > L:
            liste[i][0] = L
    return liste


def kraft(liste: list[list]) -> float:
    """
    Calculate the Kraft sum of the code
    """
    return sum(2 ** (-element[0]) for element in liste)


def step_2(liste: list[list], kraft_sum: float, L: int) -> tuple[list[list], float]:
    """
    Adjust the lengths to respect the Kraft inequality
    """
    for i in range(len(liste) - 1, 0, -1):
        while (kraft_sum - 2 ** (-liste[i][0]) + 2 ** (-liste[i][0] + 1) > 1) and (
            liste[i][0] < L
        ):
            liste[i][0] += 1
            kraft_sum += -(2 ** (-liste[i][0] + 1)) + 2 ** (-liste[i][0])
    return liste, kraft_sum


def step_3(liste: list[list], kraft_sum: float) -> tuple[list[list], float]:
    """Adjust the lengths to optimize the distribution"""
    for i in range(len(liste)):
        while (
            kraft_sum - 2 ** (-liste[i][0]) + 2 ** (-(liste[i][0] - 1)) <= 1
            and liste[i][0] > 1
        ):
            liste[i][0] -= 1
            kraft_sum += -(2 ** (-(liste[i][0] + 1))) + 2 ** (-liste[i][0])
    return liste, kraft_sum


def compression_L(input_path: str, L: int) -> bool:
    """do the compression with the given length L"""
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # count the frequency of each character
    frequencies: dict[str, int] = {char: content.count(char) for char in set(content)}
    liste: list[list] = [[freq, char] for char, freq in frequencies.items()]

    # sort the list by frequency
    liste = insertion_sort(liste)

    # limit the maximum length of the code to L
    liste = step_1(liste, L)

    # verification and correction of the Kraft inequality
    kraft_sum: float = kraft(liste)
    liste, kraft_sum = step_2(liste, kraft_sum, L)

    # verify is the distribution is still possible
    if kraft(liste) > 1:
        print("Impossible to compress with L =", L)
        return False
    else:
        liste, kraft_sum = step_3(liste, kraft_sum)
        print("Compression done with that lenght :", L)
        print("Final lenght :", liste)

        # save the results in a file
        output_file: str = input_path + ".huf"
        with open(output_file, "w", encoding="utf-8") as f:
            for char, length in liste:
                f.write(f"{char}:{length}\n")

        print(f"Résultats enregistrés dans {output_file}")
        return True


# Vérifier si le script est exécuté directement avec des arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 lenght.py <file> <max_length>")
        sys.exit(1)

    input_file: str = sys.argv[1]
    max_length: int = int(sys.argv[2])  # on converti le L en entier

    print(f"Exécution de la compression avec L = {max_length} sur {input_file}")
    compression_L(input_file, max_length)
