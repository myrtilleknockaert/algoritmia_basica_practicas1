# 📌 Practica 1: Algoritmos Voraces

## 📌 1. Presentación del practica
Este proyecto implementa un **compresor y descompresor de archivos basado en el algoritmo Huffman**.
El objetivo es reducir el tamaño de los archivos mediante el uso de una **codificación óptima sin pérdida**.

## 📌 2. Características
* Compresión de archivos de texto o binarios
* Descomprimir archivos comprimidos (`.huf`)
* Gestión de caracteres especiales (acentos, espacios, etc.)
* Opción de codificación Huffman con longitud limitada (`-l <L>`)
* Automatización de compilación y pruebas (`ejecutar.sh`)

---

## 📌 3. Organización de archivos
### 📂 `practica1_NIA1_NIA2/`
El archivo contiene:
- **📜 `README.md`** → Explicación del proyecto (este archivo).
- **📜 `huf.py`** → Script principal para comprimir/descomprimir.
- **📜 `lenght.py`** → Implementa Huffman con longitud limitada.
- **📜 `ejecutar.sh`** → Automatización de compilación y pruebas.
- **📜 `my_text.txt`** → Archivo de ejemplo para probar.
- **📜 `report.pdf`** → Análisis de rendimiento y resultados.

---
## 📌 4. Instrucciones de uso
### Compresión
```sh
./ejecutar.sh -c <nombre de fichero>
```
Produce `nombre de fichero.huf` (archivo comprimido).

###  Descompresión
```sh
./ejecutar.sh -d <nombre de fichero>
```
Produce `nombre de fichero.orig` (archivo restaurado).

### Compresión con longitud limitada
```sh
./ejecutar.sh -l <longitud máxima> -c <nombre de fichero>
```
Produce `nombre de fichero.huf`

## 📌 5. Comprobación de integridad 
Comparar archivos:
```sh
diff test.txt test.txt.orig
```
 **Si no aparece ningún mensaje, ¡la compresión y descompresión funcionan correctamente!**

 ### Verificar el tamaño de un archivo:
```sh
ls -lh test.txt
ls -lh test.txt.huf
```
Esto muestra el tamaño del archivo original y el archivo comprimido en un formato legible.

 
