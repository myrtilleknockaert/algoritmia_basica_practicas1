import sys
import math


def insertion_sort(liste: list[list]) -> list[list]:
    """Tri par insertion basé sur la fréquence des caractères"""
    for i in range(1, len(liste)):
        x = liste[i]
        j = i - 1
        while j >= 0 and liste[j][0] > x[0]:
            liste[j + 1] = liste[j]
            j -= 1
        liste[j + 1] = x
    return liste


def step_1(liste: list[list], L: int) -> list[list]:
    """Assure que la longueur maximale des codes Huffman ne dépasse pas L"""
    for i in range(len(liste) - 1, -1, -1):
        if liste[i][0] > L:
            liste[i][0] = L
    return liste


def kraft(liste: list[list]) -> float:
    """Calcule la somme de Kraft pour vérifier si les longueurs de code sont valides"""
    return sum(2 ** (-element[0]) for element in liste)


def step_2(liste: list[list], kraft_sum: float, L: int) -> tuple[list[list], float]:
    """Ajuste les longueurs de code pour respecter la contrainte de Kraft"""
    for i in range(len(liste) - 1, 0, -1):
        while (kraft_sum - 2 ** (-liste[i][0]) + 2 ** (-liste[i][0] + 1) > 1) and (
            liste[i][0] < L
        ):
            liste[i][0] += 1
            kraft_sum += -(2 ** (-liste[i][0] + 1)) + 2 ** (-liste[i][0])
    return liste, kraft_sum


def step_3(liste: list[list], kraft_sum: float) -> tuple[list[list], float]:
    """Réajuste les longueurs pour optimiser la distribution"""
    for i in range(len(liste)):
        while (
            kraft_sum - 2 ** (-liste[i][0]) + 2 ** (-(liste[i][0] - 1)) <= 1
            and liste[i][0] > 1
        ):
            liste[i][0] -= 1
            kraft_sum += -(2 ** (-(liste[i][0] + 1))) + 2 ** (-liste[i][0])
    return liste, kraft_sum


def compression_L(input_path: str, L: int) -> None:
    """Effectue la compression avec une longueur de code maximale L"""
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Calcul des fréquences des caractères
    frequencies: dict[str, int] = {char: content.count(char) for char in set(content)}
    liste: list[list] = [[freq, char] for char, freq in frequencies.items()]

    # Tri des fréquences
    liste = insertion_sort(liste)

    # Limitation des longueurs maximales à L
    liste = step_1(liste, L)

    # Vérification et ajustement avec Kraft
    kraft_sum: float = kraft(liste)
    liste, kraft_sum = step_2(liste, kraft_sum, L)

    # Vérifier si la distribution est toujours correcte
    if kraft(liste) > 1:
        print("Impossible de respecter la contrainte L avec cette distribution")
    else:
        liste, kraft_sum = step_3(liste, kraft_sum, L)
        print("Compression optimisée avec une longueur max de", L)
        print("Longueurs finales des codes :", liste)

        # Enregistrer la compression dans un fichier temporaire
        output_file: str = input_path + ".huf"
        with open(output_file, "w", encoding="utf-8") as f:
            for char, length in liste:
                f.write(f"{char}:{length}\n")

        print(f"Résultats enregistrés dans {output_file}")


# Vérifier si le script est exécuté directement avec des arguments
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 lenght.py <file> <max_length>")
        sys.exit(1)

    input_file: str = sys.argv[1]
    max_length: int = int(sys.argv[2]) # on converti le L en entier

    print(f"Exécution de la compression avec L = {max_length} sur {input_file}")
    compression_L(input_file, max_length)
