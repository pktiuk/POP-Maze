# Przeszukiwanie i Optymalizacja - Labirynt

## Tematyka

Wykorzystanie algorytmów ewolucyjnych / genetycznych do znajdowania optymalnej drogi w losowo generowanym labiryncie.  
Zadanie polega na znalezieniu optymalnej drogi w losowo generowanym labiryncie. Należy zdefiniować obszar poruszania się oraz zaprezentować w formie wizualizacji efekt działania.  
Należy wykorzystać algorytm ewolucyjny / genetyczny, który będzie potrafił zoptymalizować przejście przez labirynt.

## Uruchomienie

Instalacja zależności

```bash
pip3 install -r requirements.txt
```

Uruchomienie programu

```bash
python3 ./main.py
```

Argumenty

```bash
./main.py -h
usage: main.py [-h] [-v] [-e {ABS,SQRT,MAX,NONE}] [width] [height]

Labitynth solver

positional arguments:
  width
  height

optional arguments:
  -h, --help            show this help message and exit
  -v, --visualize
  -e {ABS,SQRT,MAX,NONE}, --heuristic {ABS,SQRT,MAX,NONE}
                        Heuristic function used with A*
```
