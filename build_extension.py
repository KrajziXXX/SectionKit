#!/usr/bin/env python3
"""
INF04 Snippets Extension Builder
Buduje wtyczkę VS Code z snippetami do egzaminu INF04
"""
import json, os, shutil

BASE   = "/home/claude/inf04-snippets"
SNIP   = os.path.join(BASE, "snippets")
os.makedirs(SNIP, exist_ok=True)

def body(code):
    """Multiline string → VS Code body array z poprawnym escaping $."""
    lines = code.split("\n")
    while lines and not lines[0].strip():  lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()
    return [l.replace("$", "\\$") for l in lines]

# ═══════════════════════════════════════════════════════
#   PYTHON – czytamy istniejący plik i dodajemy nowe
# ═══════════════════════════════════════════════════════
with open("/mnt/user-data/uploads/1778151403283_algorytmy.json", encoding="utf-8") as f:
    PY = json.load(f)

# Nowe snippety Python
PY["Python OOP – klasa abstrakcyjna, getter/setter, dziedziczenie"] = {
    "prefix": "4Qpython!",
    "description": "Pełny szablon OOP: ABC, getter, setter, konstruktor, dziedziczenie, polimorfizm",
    "body": body(r"""
from abc import ABC, abstractmethod

# ════════════════════════════════════════
#   KLASA ABSTRAKCYJNA (ABC)
#   – nie można jej bezpośrednio instancjonować
# ════════════════════════════════════════
class Pojazd(ABC):

    # KONSTRUKTOR – wywoływany przy tworzeniu obiektu
    def __init__(self, marka: str, rok: int):
        self.__marka = marka   # atrybut PRYWATNY (__ = name mangling → _Pojazd__marka)
        self.__rok   = rok

    # ── GETTER (właściwość tylko do odczytu) ──
    @property
    def marka(self) -> str:
        return self.__marka

    # ── SETTER z walidacją ──
    @marka.setter
    def marka(self, val: str):
        if len(str(val).strip()) < 2:
            raise ValueError("Marka musi mieć ≥ 2 znaki!")
        self.__marka = str(val).strip()

    @property
    def rok(self) -> int:
        return self.__rok

    @rok.setter
    def rok(self, val: int):
        if not isinstance(val, int) or val < 1886 or val > 2100:
            raise ValueError(f"Nieprawidłowy rok: {val}")
        self.__rok = val

    # ── METODA ABSTRAKCYJNA – podklasy MUSZĄ zaimplementować ──
    @abstractmethod
    def info(self) -> str:
        pass

    # Wywoływana przez print(obj)
    def __str__(self) -> str:
        return f"{self.__marka} ({self.__rok})"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.__marka!r}, {self.__rok})"


# ════════════════════════════════════════
#   KLASA POTOMNA (dziedziczenie jednopozio mowe)
# ════════════════════════════════════════
class Samochod(Pojazd):

    def __init__(self, marka: str, rok: int, drzwi: int = 4):
        super().__init__(marka, rok)   # wywołaj __init__ rodzica (OBOWIĄZKOWE)
        self.drzwi = drzwi             # własny atrybut (publiczny)

    def info(self) -> str:             # implementacja metody abstrakcyjnej
        return f"Samochód: {self.marka}, {self.rok} r., {self.drzwi} drzwi"


class Motocykl(Pojazd):

    def __init__(self, marka: str, rok: int, typ: str = "turystyczny"):
        super().__init__(marka, rok)
        self.typ = typ

    def info(self) -> str:
        return f"Motocykl: {self.marka}, {self.rok} r., typ: {self.typ}"


# ════════════════════════════════════════
#   UŻYCIE
# ════════════════════════════════════════
if __name__ == "__main__":
    s = Samochod("Toyota", 2020, 4)
    print(s)            # __str__  →  Toyota (2020)
    print(s.info())
    print(repr(s))      # __repr__

    s.marka = "Honda"   # setter z walidacją
    # s.marka = "X"     # ValueError – za krótka

    m = Motocykl("Yamaha", 2019, "sportowy")
    print(m.info())

    # POLIMORFIZM – ta sama metoda info(), różne zachowanie
    pojazdy: list = [s, m]
    for p in pojazdy:
        print(p.info())

    # Sprawdzanie typów
    print(isinstance(s, Pojazd))    # True
    print(isinstance(s, Samochod))  # True
    print(type(s).__name__)         # "Samochod"

    # v = Pojazd("X", 2020)  # TypeError! – nie można tworzyć instancji ABC
""")
}

PY["Python – sortowania: bąbelkowe, wstawianie, wybieranie, quick"] = {
    "prefix": "4QSort",
    "description": "4 sortowania z komentarzami – INF04",
    "body": body(r"""
# ════════════════════════════════════════
#   SORTOWANIA – INF04
#   Każde zwraca NOWĄ listę (kopia przez [:])
# ════════════════════════════════════════

# 1. BĄBELKOWE – porównuj sąsiednie, zamieniaj większy z mniejszym
def babelkowe(arr):
    a = arr[:]
    n = len(a)
    for i in range(n - 1):            # n-1 przejść
        for j in range(n - i - 1):   # ostatnie i elementów już posortowane
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

# 2. PRZEZ WSTAWIANIE – jak układanie kart: wstaw i-ty w odpowiednie miejsce
def przez_wstawianie(arr):
    a = arr[:]
    for i in range(1, len(a)):
        klucz = a[i]
        j = i - 1
        while j >= 0 and a[j] > klucz:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = klucz
    return a

# 3. PRZEZ WYBIERANIE – znajdź minimum, wstaw na przód
def przez_wybieranie(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

# 4. QUICKSORT – rekurencyjnie dziel na pivot / mniejsze / większe
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot  = arr[len(arr) // 2]
    lewe   = [x for x in arr if x < pivot]
    srodek = [x for x in arr if x == pivot]
    prawe  = [x for x in arr if x > pivot]
    return quicksort(lewe) + srodek + quicksort(prawe)

# ════════════════════════════════════════
#   TEST
# ════════════════════════════════════════
lista = [64, 34, 25, 12, 22, 11, 90]
print("Bąbelkowe:    ", babelkowe(lista))
print("Wstawianie:   ", przez_wstawianie(lista))
print("Wybieranie:   ", przez_wybieranie(lista))
print("Quicksort:    ", quicksort(lista))
print("Python sorted:", sorted(lista))
print("Malejąco:     ", sorted(lista, reverse=True))
print("Wg klucza:    ", sorted(["banan","jabłko","ananas"], key=len))
""")
}

PY["Python – pliki TXT i CSV"] = {
    "prefix": "4QPyFiles",
    "description": "Zapis/odczyt TXT i CSV z obsługą wyjątków – INF04",
    "body": body(r"""
import csv, os

# ═══ PLIKI TXT ═══════════════════════════

# Zapis (nadpisuje)
with open("plik.txt", "w", encoding="utf-8") as f:
    f.write("Linia 1\n")
    f.writelines(["Linia 2\n", "Linia 3\n"])

# Odczyt całości
with open("plik.txt", "r", encoding="utf-8") as f:
    tekst = f.read()
    print(tekst)

# Odczyt linia po linii
with open("plik.txt", "r", encoding="utf-8") as f:
    linie = [l.strip() for l in f]   # strip() usuwa \n i spacje
    print(linie)

# Dopisanie
with open("plik.txt", "a", encoding="utf-8") as f:
    f.write("Nowa linia\n")

# Sprawdzenie czy istnieje
if os.path.exists("plik.txt"):
    print("Rozmiar:", os.path.getsize("plik.txt"), "B")

# ═══ PLIKI CSV ═══════════════════════════

naglowki = ["Imię", "Wiek", "Miasto"]
dane     = [["Jan", 25, "Gdańsk"], ["Anna", 30, "Kraków"]]

# Zapis CSV
with open("dane.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(naglowki)
    w.writerows(dane)

# Odczyt CSV – jako lista
with open("dane.csv", "r", encoding="utf-8") as f:
    r = csv.reader(f)
    nagl = next(r)              # pomiń nagłówek
    for row in r:
        print(row[0], row[1])  # row to lista stringów

# Odczyt CSV – jako słownik (wygodniejsze)
with open("dane.csv", "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["Imię"], row["Wiek"])

# Zapis słowników do CSV
osoby = [{"Imię":"Piotr","Wiek":22,"Miasto":"Poznań"}]
with open("osoby.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["Imię","Wiek","Miasto"])
    w.writeheader()
    w.writerows(osoby)

# ═══ OBSŁUGA WYJĄTKÓW ════════════════════
try:
    with open("brak.txt", "r", encoding="utf-8") as f:
        data = f.read()
except FileNotFoundError:
    print("Plik nie istnieje!")
except PermissionError:
    print("Brak uprawnień!")
except Exception as e:
    print(f"Błąd: {e}")
""")
}

PY["Python – wyjątki i własne klasy wyjątków"] = {
    "prefix": "4QPyExc",
    "description": "try/except/else/finally, raise, własny wyjątek – INF04",
    "body": body(r"""
# ═══ PODSTAWOWE WYJĄTKI ══════════════════
try:
    x = int(input("Podaj liczbę: "))
    wynik = 10 / x
except ValueError:
    print("To nie jest liczba!")
except ZeroDivisionError:
    print("Nie dziel przez zero!")
except (TypeError, AttributeError) as e:
    print(f"Błąd typu: {e}")
except Exception as e:
    print(f"Nieoczekiwany: {e}")
else:
    print(f"Wynik: {wynik}")  # tylko gdy BRAK wyjątku
finally:
    print("Zawsze się wykonuje")  # sprzątanie, zamknięcie pliku itp.

# ═══ WŁASNY WYJĄTEK ══════════════════════
class BladWalidacji(Exception):
    def __init__(self, pole, wartosc):
        super().__init__(f"Błąd '{pole}': {wartosc!r}")
        self.pole    = pole
        self.wartosc = wartosc

class NieprawidlowyWiekError(BladWalidacji):
    def __init__(self, wiek):
        super().__init__("wiek", wiek)

# ═══ RAISE ═══════════════════════════════
def sprawdz_wiek(wiek: int):
    if not isinstance(wiek, int):
        raise TypeError(f"Wiek musi być int, nie {type(wiek).__name__}")
    if wiek < 0 or wiek > 150:
        raise NieprawidlowyWiekError(wiek)
    return wiek

try:
    sprawdz_wiek(-5)
except NieprawidlowyWiekError as e:
    print(e)          # "Błąd 'wiek': -5"
    print(e.pole)     # "wiek"
    print(e.wartosc)  # -5
""")
}

PY["Python – lambda, map, filter, sorted, comprehension"] = {
    "prefix": "4QPyLambda",
    "description": "Programowanie funkcyjne: lambda, map, filter, sorted, enumerate, zip",
    "body": body(r"""
# ═══ LAMBDA ══════════════════════════════
kwadrat   = lambda x: x ** 2
sumuj     = lambda a, b: a + b
czy_parzy = lambda x: x % 2 == 0
print(kwadrat(5))    # 25

# ═══ MAP – zastosuj funkcję do każdego ═══
liczby   = [1, 2, 3, 4, 5]
kwadraty = list(map(lambda x: x**2, liczby))
ints     = list(map(int, ["1", "2", "3"]))

# ═══ FILTER – filtruj elementy ═══════════
parzyste = list(filter(lambda x: x % 2 == 0, liczby))
dorosli  = list(filter(lambda o: o["wiek"] >= 18, [
    {"imie": "Jan", "wiek": 15},
    {"imie": "Anna","wiek": 25},
]))

# ═══ SORTED z kluczem ════════════════════
slowa = ["banan", "jabłko", "gruszka", "ananas"]
print(sorted(slowa))                           # alfabetycznie
print(sorted(slowa, key=len))                 # wg długości
print(sorted(slowa, key=len, reverse=True))   # malejąco wg długości

osoby = [{"imie":"Jan","wiek":30},{"imie":"Anna","wiek":25}]
print(sorted(osoby, key=lambda o: (o["wiek"], o["imie"])))

# ═══ LIST COMPREHENSION ══════════════════
kwadraty  = [x**2 for x in range(10)]
parzyste  = [x for x in range(20) if x % 2 == 0]
tabliczka = [[i*j for j in range(1,6)] for i in range(1,6)]  # zagnieżdżone

# DICT COMPREHENSION
d = {x: x**2 for x in range(5)}
odw = {v: k for k, v in d.items()}   # zamień klucze ↔ wartości

# ═══ ZIP i ENUMERATE ══════════════════════
imiona = ["Jan", "Anna", "Piotr"]
wieki  = [25,    30,     22    ]
for imie, wiek in zip(imiona, wieki):
    print(f"{imie}: {wiek}")

for i, imie in enumerate(imiona, start=1):   # start=1 → indeks od 1
    print(f"{i}. {imie}")
""")
}

PY["Python – rekurencja: silnia, Fibonacci, suma"] = {
    "prefix": "4QPyRec",
    "description": "Rekurencja z warunkiem stopu: silnia, Fibonacci, suma, potęga",
    "body": body(r"""
# ═══ SILNIA: n! = n * (n-1)! ══════════════
def silnia(n: int) -> int:
    if n <= 1:             # warunek stopu
        return 1
    return n * silnia(n - 1)

print(silnia(5))   # 120

# ═══ FIBONACCI ════════════════════════════
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print([fibonacci(i) for i in range(10)])  # [0,1,1,2,3,5,8,13,21,34]

# ═══ SUMA LISTY REKURENCYJNIE ═════════════
def suma(lista: list) -> int:
    if not lista:          # pusta lista = 0 (warunek stopu)
        return 0
    return lista[0] + suma(lista[1:])

print(suma([1,2,3,4,5]))  # 15

# ═══ POTĘGA ═══════════════════════════════
def potega(p, w):
    if w == 0: return 1
    return p * potega(p, w-1)

print(potega(2, 8))   # 256

# ═══ ODWRÓCENIE STRINGA ═══════════════════
def odwroc(s: str) -> str:
    if len(s) <= 1: return s
    return odwroc(s[1:]) + s[0]

print(odwroc("Python"))   # "nohtyP"
""")
}

PY["Python – słowniki i listy (operacje egzaminowe)"] = {
    "prefix": "4QPyCollections",
    "description": "Listy, słowniki, krotki – typowe operacje na egzaminie INF04",
    "body": body(r"""
# ═══ LISTY ═══════════════════════════════
lista = [3, 1, 4, 1, 5, 9, 2, 6]

lista.append(7)          # dodaj na koniec
lista.insert(0, 0)       # wstaw 0 na indeks 0
lista.remove(1)          # usuń PIERWSZE wystąpienie 1
lista.pop()              # usuń i zwróć ostatni
lista.pop(0)             # usuń i zwróć element o indeksie 0
lista.sort()             # sortuj in-place rosnąco
lista.sort(reverse=True) # malejąco
lista.reverse()          # odwróć in-place
kopia = lista.copy()     # płytka kopia (lub lista[:])
lista.clear()            # wyczyść

liczby = [3, 1, 4, 1, 5, 9]
print(min(liczby), max(liczby), sum(liczby), len(liczby))
print(sorted(liczby))          # nowa lista, oryginał bez zmian
print(liczby.count(1))         # 2  – ile razy 1
print(liczby.index(5))         # 4  – indeks pierwszego 5
print(liczby[1:4])             # [1, 4, 1]  – wycinek
print(liczby[::-1])            # odwrócona lista

for i, el in enumerate(["a","b","c"]):
    print(i, el)               # 0 a, 1 b, 2 c

# ═══ SŁOWNIKI ════════════════════════════
osoba = {"imie": "Jan", "wiek": 25, "miasto": "Gdańsk"}

print(osoba["imie"])                 # Jan
print(osoba.get("email", "Brak"))    # "Brak" – bezpieczny dostęp (brak wyjątku)

osoba["email"] = "jan@mail.com"     # dodaj klucz
osoba["wiek"]  = 26                 # zmień wartość
del osoba["miasto"]                 # usuń klucz
val = osoba.pop("email", None)      # usuń i zwróć, None gdy brak klucza

for klucz, wartosc in osoba.items():
    print(f"{klucz} = {wartosc}")

print("imie" in osoba)        # True
print("email" not in osoba)   # True

# Scalanie (Python 3.9+)
d1 = {"a": 1};  d2 = {"b": 2}
d3 = d1 | d2    # {"a": 1, "b": 2}

# ═══ KROTKI ══════════════════════════════
punkt = (10, 20)
x, y  = punkt     # rozpakowanie
# Krotka jako klucz słownika (nie można modyfikować krotki)
pozycje = {(0,0): "Start", (1,1): "Meta"}
""")
}

# ═══════════════════════════════════════════════════════
#   REACT – czytamy istniejący + dodajemy nowe
# ═══════════════════════════════════════════════════════
with open("/mnt/user-data/uploads/1778151403283_react.json", encoding="utf-8-sig") as f:
    REACT = json.load(f)

REACT["React – pełny szablon komponentu INF04"] = {
    "prefix": "4Qreact!",
    "description": "Pełny szablon: useState, useEffect, fetch, map, filter, formularz",
    "body": body(r"""
import { useState, useEffect, useRef } from "react";

// ════════════════════════════════════════
//   PEŁNY SZABLON REACT – INF04
// ════════════════════════════════════════
export default function App() {

  // ── STATE ─────────────────────────────
  const [lista,     setLista]     = useState([]);
  const [filtr,     setFiltr]     = useState("");
  const [ladowanie, setLadowanie] = useState(true);
  const [blad,      setBlad]      = useState(null);

  // Stan formularza – jeden obiekt zamiast wielu useState
  const [form, setForm] = useState({ imie: "", wiek: "", email: "" });

  const inputRef = useRef(null);   // bezpośredni dostęp do DOM

  // ── EFEKTY ────────────────────────────
  useEffect(() => {
    pobierzDane();
  }, []);  // [] = uruchom raz po zamontowaniu

  // ── FETCH ─────────────────────────────
  async function pobierzDane() {
    try {
      setLadowanie(true);
      const res = await fetch("https://jsonplaceholder.typicode.com/users");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setLista(data);
    } catch (err) {
      setBlad(err.message);
    } finally {
      setLadowanie(false);
    }
  }

  // ── FORMULARZ ─────────────────────────
  // Jeden handler dla wszystkich pól formularza
  function handleChange(e) {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  }

  function handleSubmit(e) {
    e.preventDefault();    // blokuj domyślny reload strony
    if (!form.imie.trim()) { alert("Imię wymagane!"); return; }
    const nowy = { id: Date.now(), name: form.imie, email: form.email };
    setLista(prev => [...prev, nowy]);   // spread – NIE mutuj oryginalnego state
    setForm({ imie: "", wiek: "", email: "" });
    inputRef.current?.focus();
  }

  // ── OPERACJE NA LIŚCIE ─────────────────
  function usun(id) {
    setLista(prev => prev.filter(el => el.id !== id));
  }

  // FILTROWANIE – pochodna stanu, bez nowego useState
  const listaFiltr = lista.filter(el =>
    el.name?.toLowerCase().includes(filtr.toLowerCase())
  );

  // ── RENDER ────────────────────────────
  if (ladowanie) return <p>Ładowanie...</p>;
  if (blad)      return <p style={{ color: "red" }}>Błąd: {blad}</p>;

  return (
    <div>
      <h1>Lista – INF04</h1>

      {/* Wyszukiwarka */}
      <input
        type="text"
        placeholder="Szukaj..."
        value={filtr}
        onChange={e => setFiltr(e.target.value)}
      />

      {/* Formularz */}
      <form onSubmit={handleSubmit}>
        <input ref={inputRef} name="imie"  value={form.imie}  onChange={handleChange} placeholder="Imię" />
        <input                name="wiek"  value={form.wiek}  onChange={handleChange} placeholder="Wiek" type="number" />
        <input                name="email" value={form.email} onChange={handleChange} placeholder="Email" type="email" />
        <button type="submit">Dodaj</button>
      </form>

      {/* Mapowanie listy */}
      {listaFiltr.length === 0
        ? <p>Brak wyników</p>
        : <ul>
            {listaFiltr.map(el => (
              <li key={el.id}>
                <strong>{el.name}</strong> – {el.email}
                <button onClick={() => usun(el.id)}>Usuń</button>
              </li>
            ))}
          </ul>
      }

      <p>Wyniki: {listaFiltr.length} / {lista.length}</p>
    </div>
  );
}
""")
}

REACT["React – useState: licznik, toggle, lista z CRUD"] = {
    "prefix": "4QUseState",
    "description": "useState: licznik, przełącznik, lista z dodawaniem i usuwaniem",
    "body": body(r"""
import { useState } from "react";

// ── LICZNIK ───────────────────────────────
function Licznik() {
  const [n, setN] = useState(0);
  return (
    <div>
      <button onClick={() => setN(n => n - 1)}>–</button>
      <span> {n} </span>
      <button onClick={() => setN(n => n + 1)}>+</button>
      <button onClick={() => setN(0)}>Reset</button>
    </div>
  );
}

// ── TOGGLE (przełącznik) ──────────────────
function Przelacznik() {
  const [widoczny, setWidoczny] = useState(false);
  return (
    <div>
      <button onClick={() => setWidoczny(v => !v)}>
        {widoczny ? "Ukryj" : "Pokaż"}
      </button>
      {widoczny && <p>Treść widoczna!</p>}
    </div>
  );
}

// ── LISTA – dodawanie i usuwanie ──────────
function Lista() {
  const [elementy, setElementy] = useState(["jabłko", "banan"]);
  const [nowy,     setNowy]     = useState("");

  function dodaj() {
    if (!nowy.trim()) return;
    setElementy(prev => [...prev, nowy.trim()]); // spread – nie mutuj stanu!
    setNowy("");
  }

  function usun(index) {
    setElementy(prev => prev.filter((_, i) => i !== index));
  }

  return (
    <div>
      <input
        value={nowy}
        onChange={e => setNowy(e.target.value)}
        onKeyDown={e => e.key === "Enter" && dodaj()}
        placeholder="Nowy element"
      />
      <button onClick={dodaj}>Dodaj</button>
      <ul>
        {elementy.map((el, i) => (
          <li key={i}>
            {el} <button onClick={() => usun(i)}>✕</button>
          </li>
        ))}
      </ul>
      <p>Łącznie: {elementy.length}</p>
    </div>
  );
}
""")
}

REACT["React – useEffect + fetch (pobieranie danych z API)"] = {
    "prefix": "4QFetch",
    "description": "useEffect z fetch: loading state, błędy, cleanup, ponowne pobieranie",
    "body": body(r"""
import { useState, useEffect } from "react";

// ════════════════════════════════════════
//   FETCH Z API – wzorzec INF04
// ════════════════════════════════════════
function DaneZApi({ userId }) {
  const [dane,      setDane]      = useState(null);
  const [ladowanie, setLadowanie] = useState(true);
  const [blad,      setBlad]      = useState(null);

  useEffect(() => {
    let aktywny = true;   // cleanup – zapobiega ustawieniu stanu po odmontowaniu

    async function pobierz() {
      try {
        setLadowanie(true);
        setBlad(null);
        const res = await fetch(`https://jsonplaceholder.typicode.com/users/${userId}`);
        if (!res.ok) throw new Error(`Błąd ${res.status}`);
        const json = await res.json();
        if (aktywny) setDane(json);
      } catch (err) {
        if (aktywny) setBlad(err.message);
      } finally {
        if (aktywny) setLadowanie(false);
      }
    }

    pobierz();
    return () => { aktywny = false; };  // cleanup przed kolejnym efektem
  }, [userId]);  // zależności – uruchom ponownie gdy userId się zmieni

  if (ladowanie) return <p>Ładowanie...</p>;
  if (blad)      return <p style={{ color: "red" }}>Błąd: {blad}</p>;
  if (!dane)     return null;

  return (
    <div>
      <h2>{dane.name}</h2>
      <p>Email: {dane.email}</p>
      <p>Miasto: {dane.address?.city}</p>   {/* optional chaining */}
    </div>
  );
}

// ════════════════════════════════════════
//   POST – wysyłanie danych
// ════════════════════════════════════════
async function wyslijDane(dane) {
  const res = await fetch("https://api.example.com/items", {
    method:  "POST",
    headers: { "Content-Type": "application/json" },
    body:    JSON.stringify(dane),
  });
  if (!res.ok) throw new Error("Błąd zapisu");
  return res.json();
}

// ════════════════════════════════════════
//   DELETE
// ════════════════════════════════════════
async function usunElement(id) {
  const res = await fetch(`https://api.example.com/items/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Błąd usunięcia");
}
""")
}

REACT["React – mapowanie i filtrowanie listy z sortowaniem"] = {
    "prefix": "4QMapFilter",
    "description": "Mapowanie, filtrowanie, sortowanie, unikalne kategorie – INF04",
    "body": body(r"""
import { useState } from "react";

const PRODUKTY = [
  { id: 1, nazwa: "Laptop",  cena: 3500, kat: "Elektronika" },
  { id: 2, nazwa: "Książka", cena:   59, kat: "Edukacja"    },
  { id: 3, nazwa: "Telefon", cena: 2200, kat: "Elektronika" },
  { id: 4, nazwa: "Notes",   cena:   15, kat: "Edukacja"    },
];

export default function ListaProdukow() {
  const [szukaj, setSzukaj]   = useState("");
  const [kat,    setKat]      = useState("Wszystkie");
  const [sort,   setSort]     = useState("nazwa");   // "nazwa" | "cena"

  // Unikalne kategorie (bez duplikatów)
  const kategorie = ["Wszystkie", ...new Set(PRODUKTY.map(p => p.kat))];

  // PIPELINE: filter → sort → map  (kolejność ważna!)
  const wyswietlane = PRODUKTY
    .filter(p => kat === "Wszystkie" || p.kat === kat)
    .filter(p => p.nazwa.toLowerCase().includes(szukaj.toLowerCase()))
    .sort((a, b) =>
      sort === "cena"
        ? a.cena - b.cena
        : a.nazwa.localeCompare(b.nazwa, "pl")
    );

  return (
    <div>
      <input
        type="search"
        value={szukaj}
        onChange={e => setSzukaj(e.target.value)}
        placeholder="Szukaj produktu..."
      />

      <select value={kat} onChange={e => setKat(e.target.value)}>
        {kategorie.map(k => <option key={k}>{k}</option>)}
      </select>

      <select value={sort} onChange={e => setSort(e.target.value)}>
        <option value="nazwa">Sortuj: A–Z</option>
        <option value="cena">Sortuj: cena rosnąco</option>
      </select>

      {wyswietlane.length === 0
        ? <p>Brak wyników</p>
        : <ul>
            {wyswietlane.map(p => (
              <li key={p.id}>
                <strong>{p.nazwa}</strong> – {p.cena} zł
                <em> [{p.kat}]</em>
              </li>
            ))}
          </ul>
      }
      <p>Wyników: {wyswietlane.length} / {PRODUKTY.length}</p>
    </div>
  );
}
""")
}

REACT["React – useReducer (zaawansowany state)"] = {
    "prefix": "4QReducer",
    "description": "useReducer zamiast wielu useState – zarządzanie złożonym stanem",
    "body": body(r"""
import { useReducer } from "react";

// ════════════════════════════════════════
//   useReducer – gdy stan jest złożony
//   lub wiele akcji modyfikuje ten sam stan
// ════════════════════════════════════════

const poczatkowyStan = {
  elementy: [],
  filtr:    "",
  licznik:  0,
};

// REDUCER – czysta funkcja: (stan, akcja) => nowyStan
function reducer(stan, akcja) {
  switch (akcja.type) {
    case "DODAJ":
      return {
        ...stan,
        elementy: [...stan.elementy, { id: Date.now(), tekst: akcja.payload }],
        licznik:  stan.licznik + 1,
      };
    case "USUN":
      return {
        ...stan,
        elementy: stan.elementy.filter(el => el.id !== akcja.payload),
      };
    case "USTAW_FILTR":
      return { ...stan, filtr: akcja.payload };
    case "RESET":
      return poczatkowyStan;
    default:
      return stan;   // nieznana akcja – zwróć stan bez zmian
  }
}

export default function App() {
  const [stan, dispatch] = useReducer(reducer, poczatkowyStan);
  const [input, setInput] = require("react").useState("");

  function dodaj() {
    if (!input.trim()) return;
    dispatch({ type: "DODAJ", payload: input });
    setInput("");
  }

  const widoczne = stan.elementy.filter(el =>
    el.tekst.toLowerCase().includes(stan.filtr.toLowerCase())
  );

  return (
    <div>
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={dodaj}>Dodaj</button>
      <input
        placeholder="Filtruj..."
        value={stan.filtr}
        onChange={e => dispatch({ type: "USTAW_FILTR", payload: e.target.value })}
      />
      <button onClick={() => dispatch({ type: "RESET" })}>Reset</button>
      <p>Dodano łącznie: {stan.licznik}</p>
      <ul>
        {widoczne.map(el => (
          <li key={el.id}>
            {el.tekst}
            <button onClick={() => dispatch({ type: "USUN", payload: el.id })}>✕</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
""")
}

# ═══════════════════════════════════════════════════════
#   KOTLIN (ANDROID) – nowe snippety (Kotlin + XML Views)
# ═══════════════════════════════════════════════════════
KOTLIN = {}

KOTLIN["Android Kotlin – MainActivity pełny szablon (XML Views)"] = {
    "prefix": "4Qkotlin!",
    "description": "Pełny szablon: Button, EditText, ListView, AlertDialog, Toast, Intent",
    "body": body(r"""
package com.example.aplikacja

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity

// ════════════════════════════════════════
//   MAIN ACTIVITY – szablon INF04
//   (Empty Activity + Views / XML)
// ════════════════════════════════════════
//
//  W activity_main.xml dodaj:
//   <EditText  android:id="@+id/etNazwa"   ... />
//   <Button    android:id="@+id/btnDodaj"  android:text="Dodaj" ... />
//   <ListView  android:id="@+id/listView"  ... />
//   <TextView  android:id="@+id/tvInfo"    ... />

class MainActivity : AppCompatActivity() {

    private lateinit var etNazwa:  EditText
    private lateinit var btnDodaj: Button
    private lateinit var listView: ListView
    private lateinit var tvInfo:   TextView

    private val lista   = mutableListOf<String>()
    private lateinit var adapter: ArrayAdapter<String>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // ── Powiązanie widoków ──────────────
        etNazwa  = findViewById(R.id.etNazwa)
        btnDodaj = findViewById(R.id.btnDodaj)
        listView = findViewById(R.id.listView)
        tvInfo   = findViewById(R.id.tvInfo)

        // ── Adapter ────────────────────────
        adapter  = ArrayAdapter(this, android.R.layout.simple_list_item_1, lista)
        listView.adapter = adapter

        // ── Kliknięcie przycisku ────────────
        btnDodaj.setOnClickListener {
            val tekst = etNazwa.text.toString().trim()
            if (tekst.isEmpty()) {
                Toast.makeText(this, "Pole nie może być puste!", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            lista.add(tekst)
            adapter.notifyDataSetChanged()
            etNazwa.text.clear()
            tvInfo.text = "Elementów: ${lista.size}"
        }

        // ── Długie kliknięcie → usuń ────────
        listView.setOnItemLongClickListener { _, _, position, _ ->
            pokazDialogUsuwania(position)
            true
        }

        // ── Krótkie kliknięcie → nowa aktywność ──
        listView.setOnItemClickListener { _, _, position, _ ->
            val intent = Intent(this, SzczegolyActivity::class.java)
            intent.putExtra("ELEMENT",  lista[position])
            intent.putExtra("POZYCJA",  position)
            startActivity(intent)
        }
    }

    private fun pokazDialogUsuwania(position: Int) {
        AlertDialog.Builder(this)
            .setTitle("Usuń element")
            .setMessage("Usunąć '${lista[position]}'?")
            .setPositiveButton("Tak") { _, _ ->
                lista.removeAt(position)
                adapter.notifyDataSetChanged()
                Toast.makeText(this, "Usunięto!", Toast.LENGTH_SHORT).show()
            }
            .setNegativeButton("Anuluj", null)
            .show()
    }
}
""")
}

KOTLIN["Android Kotlin – RecyclerView + Adapter + ViewHolder"] = {
    "prefix": "4QRecyclerView",
    "description": "RecyclerView z Adapterem, ViewHolder, onclick i long click – INF04",
    "body": body(r"""
package com.example.aplikacja

// ════════════════════════════════════════
//   MODEL DANYCH
// ════════════════════════════════════════
data class Produkt(val id: Int, val nazwa: String, val cena: Double)

// ════════════════════════════════════════
//   ADAPTER
// ════════════════════════════════════════
//
//  W build.gradle (app) dodaj zależność:
//   implementation "androidx.recyclerview:recyclerview:1.3.2"
//
//  W activity_main.xml:
//   <androidx.recyclerview.widget.RecyclerView
//       android:id="@+id/recyclerView"
//       android:layout_width="match_parent"
//       android:layout_height="match_parent"/>
//
//  Utwórz res/layout/item_produkt.xml:
//   <LinearLayout ...>
//     <TextView android:id="@+id/tvNazwa" />
//     <TextView android:id="@+id/tvCena"  />
//   </LinearLayout>

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ProduktAdapter(
    private val lista:       MutableList<Produkt>,
    private val onClick:     (Produkt) -> Unit,
    private val onLongClick: (Int)     -> Unit
) : RecyclerView.Adapter<ProduktAdapter.ViewHolder>() {

    inner class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val tvNazwa: TextView = view.findViewById(R.id.tvNazwa)
        val tvCena:  TextView = view.findViewById(R.id.tvCena)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_produkt, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val p = lista[position]
        holder.tvNazwa.text = p.nazwa
        holder.tvCena.text  = "%.2f zł".format(p.cena)

        holder.itemView.setOnClickListener     { onClick(p)       }
        holder.itemView.setOnLongClickListener { onLongClick(position); true }
    }

    override fun getItemCount() = lista.size

    fun updateData(nowa: List<Produkt>) {
        lista.clear(); lista.addAll(nowa); notifyDataSetChanged()
    }
}

// ════════════════════════════════════════
//   UŻYCIE W ACTIVITY (w onCreate):
// ════════════════════════════════════════
//
//   val rv = findViewById<RecyclerView>(R.id.recyclerView)
//   rv.layoutManager = LinearLayoutManager(this)
//
//   val produkty = mutableListOf(Produkt(1,"Laptop",3500.0))
//   val adapter  = ProduktAdapter(
//       produkty,
//       onClick     = { p   -> Toast.makeText(this, p.nazwa, Toast.LENGTH_SHORT).show() },
//       onLongClick = { pos -> produkty.removeAt(pos); adapter.notifyItemRemoved(pos)   }
//   )
//   rv.adapter = adapter
""")
}

KOTLIN["Android Kotlin – Intent, przekazywanie danych między aktywnościami"] = {
    "prefix": "4QIntent",
    "description": "Explicit intent + putExtra/getExtra, implicit intent (URL, tel, mail)",
    "body": body(r"""
// ════════════════════════════════════════
//   WYSYŁANIE (Activity A → Activity B)
// ════════════════════════════════════════
val intent = Intent(this, SzczegolyActivity::class.java).apply {
    putExtra("KLUCZ_STRING",  "wartość tekstowa")
    putExtra("KLUCZ_INT",     42)
    putExtra("KLUCZ_BOOL",    true)
    putExtra("KLUCZ_DOUBLE",  3.14)
}
startActivity(intent)

// ════════════════════════════════════════
//   ODBIERANIE (SzczegolyActivity – onCreate)
// ════════════════════════════════════════
val tekst   = intent.getStringExtra("KLUCZ_STRING")  ?: "domyślna"
val liczba  = intent.getIntExtra("KLUCZ_INT",    0)
val flaga   = intent.getBooleanExtra("KLUCZ_BOOL", false)
val decimal = intent.getDoubleExtra("KLUCZ_DOUBLE", 0.0)

// ════════════════════════════════════════
//   INTENT NIEJAWNY
// ════════════════════════════════════════
// Otwórz przeglądarkę
startActivity(Intent(Intent.ACTION_VIEW,
    android.net.Uri.parse("https://google.com")))

// Zadzwoń
startActivity(Intent(Intent.ACTION_DIAL,
    android.net.Uri.parse("tel:123456789")))

// Wyślij e-mail
val mail = Intent(Intent.ACTION_SEND).apply {
    type = "text/plain"
    putExtra(Intent.EXTRA_EMAIL,   arrayOf("mail@example.com"))
    putExtra(Intent.EXTRA_SUBJECT, "Temat")
    putExtra(Intent.EXTRA_TEXT,    "Treść")
}
startActivity(Intent.createChooser(mail, "Wyślij e-mail"))
""")
}

KOTLIN["Android Kotlin – SharedPreferences"] = {
    "prefix": "4QSharedPrefs",
    "description": "Zapis i odczyt danych lokalnych w SharedPreferences",
    "body": body(r"""
import android.content.Context

// ════════════════════════════════════════
//   SHARED PREFERENCES – małe dane lokalne
//   (ustawienia, token, wyniki użytkownika)
// ════════════════════════════════════════

val prefs = getSharedPreferences("MOJE_USTAWIENIA", Context.MODE_PRIVATE)

// ZAPIS
prefs.edit()
    .putString("nazwa",  "Jan Kowalski")
    .putInt("wiek",      25)
    .putBoolean("dark",  true)
    .putFloat("wynik",   9.5f)
    .apply()          // apply() = asynchroniczny (zalecany)
    // commit()       -- synchroniczny, zwraca Boolean

// ODCZYT
val nazwa = prefs.getString("nazwa",  "Nieznany")  // 2. arg = domyślna
val wiek  = prefs.getInt("wiek",      0)
val dark  = prefs.getBoolean("dark",  false)
val wynik = prefs.getFloat("wynik",   0f)

println("$nazwa, wiek: $wiek, dark: $dark")

// USUWANIE jednego klucza
prefs.edit().remove("wiek").apply()

// WYCZYŚĆ WSZYSTKO
prefs.edit().clear().apply()

// Sprawdzenie czy klucz istnieje
if (prefs.contains("nazwa")) println("Klucz 'nazwa' istnieje")
""")
}

KOTLIN["Android Kotlin – pętle, kolekcje, null safety, wyjątki"] = {
    "prefix": "4QKotlinBasics",
    "description": "Pętle, listy, mapy, null safety, wyjątki w Kotlinie – INF04",
    "body": body(r"""
// ════════════════════════════════════════
//   PĘTLE
// ════════════════════════════════════════
for (i in 1..10)            print("$i ")   // 1..10 (włącznie)
for (i in 1 until 10)       print("$i ")   // 1..9  (bez 10)
for (i in 10 downTo 1 step 2) print("$i ") // 10 8 6 4 2

val owoce = listOf("jabłko", "banan", "gruszka")
for (owoc in owoce) println(owoc)
owoce.forEachIndexed { i, owoc -> println("$i: $owoc") }

var n = 0
while (n < 5) { print("$n "); n++ }

// ════════════════════════════════════════
//   KOLEKCJE
// ════════════════════════════════════════
val niemut = listOf("a", "b", "c")                     // niezmienalna
val mut    = mutableListOf(1, 2, 3)                    // zmienalna
mut.add(4); mut.removeAt(0); mut.set(0, 99)

val mapa   = mapOf("pl" to "Polska", "de" to "Niemcy")
val mutMap = mutableMapOf<String, Int>()
mutMap["Jan"] = 25
println(mutMap.getOrDefault("X", -1))  // -1 gdy brak klucza

// Operacje funkcyjne
val liczby = listOf(1, 2, 3, 4, 5, 6)
val parzyste    = liczby.filter { it % 2 == 0 }
val kwadraty    = liczby.map    { it * it       }
val posortowane = liczby.sortedDescending()
val suma        = liczby.sum()
val pierwsze    = liczby.first { it > 3 }  // 4

// ════════════════════════════════════════
//   NULL SAFETY
// ════════════════════════════════════════
var tekst: String? = null         // ? = może być null

val dlugosc = tekst?.length       // null gdy tekst == null (safe call)
val bezNull = tekst ?: "domyślna" // elvis – użyj "domyślna" gdy null
// tekst!!.length                 // NPE jeśli null (unikaj!)

val liczba: Int? = "123".toIntOrNull()  // null gdy błąd konwersji
val safe   = liczba ?: 0

// ════════════════════════════════════════
//   WYJĄTKI
// ════════════════════════════════════════
try {
    val x = "abc".toInt()    // NumberFormatException
    val y = 10 / 0           // ArithmeticException
} catch (e: NumberFormatException) {
    println("Zły format: ${e.message}")
} catch (e: ArithmeticException) {
    println("Dzielenie przez 0")
} catch (e: Exception) {
    println("Błąd: ${e.message}")
} finally {
    println("Zawsze się wykona")
}
""")
}

KOTLIN["Android Kotlin – AlertDialog, Toast, Snackbar, ProgressBar"] = {
    "prefix": "4QKotlinDialogs",
    "description": "AlertDialog (z listą, z EditText), Toast, Snackbar – INF04",
    "body": body(r"""
import androidx.appcompat.app.AlertDialog
import android.widget.Toast
import android.widget.EditText

// ════ TOAST ════════════════════════════
Toast.makeText(this, "Operacja udana!",    Toast.LENGTH_SHORT).show()
Toast.makeText(this, "Błąd połączenia",    Toast.LENGTH_LONG).show()

// ════ ALERTDIALOG – Tak/Nie ════════════
AlertDialog.Builder(this)
    .setTitle("Usuń element")
    .setMessage("Czy na pewno chcesz usunąć ten element?")
    .setPositiveButton("Tak") { _, _ ->
        // akcja potwierdzenia
        Toast.makeText(this, "Usunięto", Toast.LENGTH_SHORT).show()
    }
    .setNegativeButton("Anuluj", null)  // null = po prostu zamknij
    .setNeutralButton("Więcej info")    { _, _ -> /* opcjonalny 3. przycisk */ }
    .setCancelable(false)               // nie zamykaj przez klik poza dialogiem
    .show()

// ════ ALERTDIALOG – lista wyboru ═══════
val opcje = arrayOf("Opcja A", "Opcja B", "Opcja C")
AlertDialog.Builder(this)
    .setTitle("Wybierz opcję")
    .setItems(opcje) { _, ktora ->
        Toast.makeText(this, "Wybrałeś: ${opcje[ktora]}", Toast.LENGTH_SHORT).show()
    }
    .show()

// ════ ALERTDIALOG – z polem tekstowym ═══
val et = EditText(this)
et.hint = "Wpisz wartość"
AlertDialog.Builder(this)
    .setTitle("Wpisz dane")
    .setView(et)
    .setPositiveButton("OK") { _, _ ->
        val wartosc = et.text.toString().trim()
        if (wartosc.isNotEmpty())
            Toast.makeText(this, "Wpisano: $wartosc", Toast.LENGTH_SHORT).show()
    }
    .setNegativeButton("Anuluj", null)
    .show()
""")
}

KOTLIN["Android Kotlin – ListView z drawable i customowym adapterem"] = {
    "prefix": "4QListDrawable",
    "description": "ListView z ikoną (drawable), niestandardowy adapter – INF04",
    "body": body(r"""
package com.example.aplikacja

// ════════════════════════════════════════
//   LISTA Z IKONAMI – drawable[] + ListView
// ════════════════════════════════════════
//
//  1. Dodaj ikony do res/drawable/ (np. ic_laptop.png, ic_phone.png)
//  2. Utwórz res/layout/item_row.xml:
//     <LinearLayout android:orientation="horizontal" ...>
//       <ImageView android:id="@+id/ivIcon"   android:layout_width="48dp"
//                  android:layout_height="48dp" android:padding="4dp"/>
//       <TextView  android:id="@+id/tvNazwa"  android:layout_gravity="center_vertical"
//                  android:textSize="18sp"/>
//     </LinearLayout>

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle

data class Element(val nazwa: String, val iconRes: Int)

class ElementAdapter(
    context: Context,
    private val lista: List<Element>
) : ArrayAdapter<Element>(context, 0, lista) {

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val view = convertView ?: LayoutInflater.from(context)
            .inflate(R.layout.item_row, parent, false)

        val el      = lista[position]
        val ivIcon  = view.findViewById<ImageView>(R.id.ivIcon)
        val tvNazwa = view.findViewById<TextView>(R.id.tvNazwa)

        ivIcon.setImageResource(el.iconRes)
        tvNazwa.text = el.nazwa

        return view
    }
}

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Tablica z obrazkami – ikony muszą być w res/drawable/
        val elementy = listOf(
            Element("Laptop",  R.drawable.ic_launcher_foreground),
            Element("Telefon", R.drawable.ic_launcher_foreground),
            // Zamień ic_launcher_foreground na własne ikony
        )

        val listView = findViewById<ListView>(R.id.listView)
        val adapter  = ElementAdapter(this, elementy)
        listView.adapter = adapter

        listView.setOnItemClickListener { _, _, pos, _ ->
            Toast.makeText(this, "Kliknięto: ${elementy[pos].nazwa}", Toast.LENGTH_SHORT).show()
        }
    }
}
""")
}

KOTLIN["Android Kotlin – Spinner (dropdown)"] = {
    "prefix": "4QSpinner",
    "description": "Spinner z ArrayAdapter i obsługą wyboru – INF04",
    "body": body(r"""
// W XML dodaj:
// <Spinner android:id="@+id/spinner" android:layout_width="match_parent"
//          android:layout_height="wrap_content"/>

val spinner = findViewById<Spinner>(R.id.spinner)

// Dane
val opcje = listOf("Wybierz...", "Opcja A", "Opcja B", "Opcja C")

// Adapter
val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, opcje)
adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
spinner.adapter = adapter

// Obsługa wyboru
spinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
    override fun onItemSelected(parent: AdapterView<*>, view: View?, position: Int, id: Long) {
        if (position == 0) return     // pomiń "Wybierz..."
        val wybrana = opcje[position]
        Toast.makeText(this@MainActivity, "Wybrano: $wybrana", Toast.LENGTH_SHORT).show()
    }
    override fun onNothingSelected(parent: AdapterView<*>) {}
}

// Programowe ustawienie wartości
spinner.setSelection(2)   // indeks 2 → "Opcja B"

// Pobranie aktualnej wartości
val aktualna = spinner.selectedItem.toString()
""")
}

# ═══════════════════════════════════════════════════════
#   C# WPF – nowe snippety (WPF, nie WinForms)
# ═══════════════════════════════════════════════════════
CSHARP = {}

CSHARP["WPF C# – pełny szablon aplikacji CRUD"] = {
    "prefix": "4Qwpf!",
    "description": "Pełny szablon WPF: ObservableCollection, CRUD, walidacja, MessageBox",
    "body": body(r"""
// ════════════════════════════════════════
//   WPF – PEŁNY SZABLON INF04
//   MainWindow.xaml.cs
// ════════════════════════════════════════
//
//  XAML (MainWindow.xaml) – wklej wewnątrz <Grid>:
//
//  <StackPanel Margin="10">
//    <TextBox   x:Name="txtNazwa" PlaceholderText="Nazwa" Margin="0,0,0,5"/>
//    <TextBox   x:Name="txtCena"  PlaceholderText="Cena"  Margin="0,0,0,5"/>
//    <StackPanel Orientation="Horizontal" Margin="0,0,0,5">
//      <Button Content="Dodaj"  Click="BtnDodaj_Click"  Margin="0,0,5,0"/>
//      <Button Content="Usuń"   Click="BtnUsun_Click"   Margin="0,0,5,0"/>
//      <Button Content="Edytuj" Click="BtnEdytuj_Click" Margin="0,0,5,0"/>
//    </StackPanel>
//    <ListBox   x:Name="listBox" Height="200"
//               DisplayMemberPath="NazwaICena" Margin="0,0,0,5"/>
//    <TextBlock x:Name="txtBlad" Foreground="Red"/>
//  </StackPanel>

using System;
using System.Collections.ObjectModel;
using System.Windows;

namespace Aplikacja
{
    // ── Model danych ──────────────────────
    public class Produkt
    {
        public int    Id    { get; set; }
        public string Nazwa { get; set; } = "";
        public double Cena  { get; set; }

        // Pomocnicze pole do wyświetlania w ListBox
        public string NazwaICena => $"{Nazwa} – {Cena:F2} zł";

        public override string ToString() => NazwaICena;
    }

    public partial class MainWindow : Window
    {
        // ObservableCollection – auto-odświeża ListBox/DataGrid
        private readonly ObservableCollection<Produkt> produkty = new();
        private int nextId = 1;

        public MainWindow()
        {
            InitializeComponent();
            listBox.ItemsSource = produkty;

            // Przykładowe dane startowe
            produkty.Add(new Produkt { Id = nextId++, Nazwa = "Laptop",  Cena = 3500 });
            produkty.Add(new Produkt { Id = nextId++, Nazwa = "Telefon", Cena = 1200 });
        }

        // ── DODAJ ─────────────────────────
        private void BtnDodaj_Click(object sender, RoutedEventArgs e)
        {
            txtBlad.Text = "";
            if (!WalidujFormularz(out string nazwa, out double cena)) return;

            produkty.Add(new Produkt { Id = nextId++, Nazwa = nazwa, Cena = cena });
            ClearForm();
            MessageBox.Show("Dodano produkt!", "OK",
                MessageBoxButton.OK, MessageBoxImage.Information);
        }

        // ── USUŃ ──────────────────────────
        private void BtnUsun_Click(object sender, RoutedEventArgs e)
        {
            if (listBox.SelectedItem is not Produkt wybrany)
            {
                MessageBox.Show("Zaznacz element!", "Uwaga",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            var res = MessageBox.Show($"Usunąć '{wybrany.Nazwa}'?", "Potwierdzenie",
                MessageBoxButton.YesNo, MessageBoxImage.Question);
            if (res == MessageBoxResult.Yes)
                produkty.Remove(wybrany);
        }

        // ── EDYTUJ ────────────────────────
        private void BtnEdytuj_Click(object sender, RoutedEventArgs e)
        {
            if (listBox.SelectedItem is not Produkt wybrany) return;

            txtNazwa.Text = wybrany.Nazwa;
            txtCena.Text  = wybrany.Cena.ToString();
            produkty.Remove(wybrany);  // usuń stary, dodaj poprawiony przez "Dodaj"
        }

        // ── WALIDACJA ─────────────────────
        private bool WalidujFormularz(out string nazwa, out double cena)
        {
            nazwa = txtNazwa.Text.Trim();
            cena  = 0;

            if (string.IsNullOrEmpty(nazwa) || nazwa.Length < 2)
            {
                txtBlad.Text = "Nazwa musi mieć co najmniej 2 znaki!";
                return false;
            }
            if (!double.TryParse(txtCena.Text.Replace(",", "."),
                    System.Globalization.NumberStyles.Any,
                    System.Globalization.CultureInfo.InvariantCulture, out cena) || cena < 0)
            {
                txtBlad.Text = "Nieprawidłowa cena (musi być liczbą ≥ 0)!";
                return false;
            }
            return true;
        }

        private void ClearForm()
        {
            txtNazwa.Text = "";
            txtCena.Text  = "";
            txtBlad.Text  = "";
        }
    }
}
""")
}

CSHARP["WPF C# – LINQ: Where, OrderBy, Select, GroupBy, agregacje"] = {
    "prefix": "4QLINQ",
    "description": "LINQ – zapytania: Where, OrderBy, Select, GroupBy, First, Any, Sum – INF04",
    "body": body(r"""
using System;
using System.Collections.Generic;
using System.Linq;

// ════════════════════════════════════════
//   LINQ – Language Integrated Query
//   Działa na List<T>, Array, ObservableCollection itd.
// ════════════════════════════════════════

var produkty = new List<Produkt>
{
    new() { Id=1, Nazwa="Laptop",   Cena=3500, Kat="Elektronika" },
    new() { Id=2, Nazwa="Książka",  Cena=  59, Kat="Edukacja"    },
    new() { Id=3, Nazwa="Telefon",  Cena=2200, Kat="Elektronika" },
    new() { Id=4, Nazwa="Długopis", Cena=   5, Kat="Edukacja"    },
};

// WHERE – filtrowanie
var drogie     = produkty.Where(p => p.Cena > 1000).ToList();
var elektronika = produkty.Where(p => p.Kat == "Elektronika").ToList();

// ORDER BY – sortowanie
var alfabet    = produkty.OrderBy(p => p.Nazwa).ToList();
var poKolejno  = produkty.OrderBy(p => p.Kat).ThenBy(p => p.Cena).ToList();
var najtanszy  = produkty.MinBy(p => p.Cena);
var najdrozszy = produkty.MaxBy(p => p.Cena);

// SELECT – projekcja
var nazwy    = produkty.Select(p => p.Nazwa).ToList();
var opisy    = produkty.Select(p => $"{p.Nazwa}: {p.Cena:F2} zł").ToList();
var skrocone = produkty.Select(p => new { p.Nazwa, p.Cena }).ToList();

// Łańcuchowanie
var wynik = produkty
    .Where(p => p.Kat == "Elektronika")
    .OrderByDescending(p => p.Cena)
    .Select(p => $"{p.Nazwa} ({p.Cena:F2} zł)")
    .ToList();
wynik.ForEach(Console.WriteLine);

// GROUP BY – grupowanie
var grupy = produkty
    .GroupBy(p => p.Kat)
    .ToDictionary(g => g.Key, g => g.ToList());
foreach (var (kat, lista) in grupy)
    Console.WriteLine($"{kat}: {lista.Count} szt., razem {lista.Sum(p => p.Cena):F2} zł");

// AGREGACJE
double suma    = produkty.Sum(p => p.Cena);
double srednia = produkty.Average(p => p.Cena);
int    ile     = produkty.Count(p => p.Cena > 100);

// SPRAWDZENIE
bool czyJest  = produkty.Any(p => p.Nazwa == "Laptop");
bool wszyskie = produkty.All(p => p.Cena > 0);

// ZNAJDŹ JEDEN (nie rzuca wyjątku gdy brak – zwraca null)
var znaleziony = produkty.FirstOrDefault(p => p.Id == 2);
var jedyny     = produkty.SingleOrDefault(p => p.Id == 3); // tylko gdy 1 wynik

// DISTINCT, SKIP, TAKE
var unikalne = produkty.Select(p => p.Kat).Distinct().ToList();
var strona   = produkty.Skip(1).Take(2).ToList();  // paginacja: pomiń 1, weź 2
""")
}

CSHARP["WPF C# – operacje na plikach TXT i CSV"] = {
    "prefix": "4QCsFiles",
    "description": "File.ReadAllText/Lines/WriteAll, StreamReader CSV, wyjątki – INF04",
    "body": body(r"""
using System;
using System.IO;
using System.Collections.Generic;
using System.Text;

// ════ PLIKI TXT ════════════════════════

// Zapis (nadpisuje)
File.WriteAllText("plik.txt", "Linia 1\nLinia 2\n", Encoding.UTF8);

// Dopisanie
File.AppendAllText("plik.txt", "Nowa linia\n", Encoding.UTF8);

// Odczyt całości
string zawartosc = File.ReadAllText("plik.txt", Encoding.UTF8);
Console.WriteLine(zawartosc);

// Odczyt jako tablica linii
string[] linie = File.ReadAllLines("plik.txt", Encoding.UTF8);
foreach (var l in linie) Console.WriteLine(l.Trim());

// Sprawdzenie istnienia
if (File.Exists("plik.txt"))
    Console.WriteLine("Rozmiar: " + new FileInfo("plik.txt").Length + " B");

// Usunięcie
// File.Delete("plik.txt");

// ════ PLIKI CSV ════════════════════════

// Zapis CSV
var wiersze = new List<string[]>
{
    new[] { "Imię",  "Wiek", "Miasto" },
    new[] { "Jan",   "25",   "Gdańsk" },
    new[] { "Anna",  "30",   "Kraków" },
};
using (var sw = new StreamWriter("dane.csv", false, Encoding.UTF8))
    foreach (var w in wiersze)
        sw.WriteLine(string.Join(",", w));

// Odczyt CSV
using (var sr = new StreamReader("dane.csv", Encoding.UTF8))
{
    var nagl = sr.ReadLine()?.Split(',');  // pierwsza linia = nagłówki
    while (!sr.EndOfStream)
    {
        var pola = sr.ReadLine()?.Split(',');
        if (pola is { Length: >= 2 })
            Console.WriteLine($"Imię: {pola[0]}, Wiek: {pola[1]}");
    }
}

// ════ OBSŁUGA WYJĄTKÓW ══════════════════
try
{
    string data = File.ReadAllText("brak.txt");
}
catch (FileNotFoundException)    { Console.WriteLine("Plik nie istnieje!"); }
catch (UnauthorizedAccessException) { Console.WriteLine("Brak dostępu!"); }
catch (IOException ex)           { Console.WriteLine($"Błąd I/O: {ex.Message}"); }
finally                          { Console.WriteLine("Gotowe"); }
""")
}

CSHARP["WPF C# – DataGrid z ObservableCollection i INotifyPropertyChanged"] = {
    "prefix": "4QDataGrid",
    "description": "DataGrid binding, INotifyPropertyChanged, DataContext – INF04",
    "body": body(r"""
// ════════════════════════════════════════
//   MODEL z powiadamianiem UI o zmianach
// ════════════════════════════════════════
//
//  XAML – DataGrid (wklej do Window):
//  <DataGrid x:Name="dg"
//            AutoGenerateColumns="False"
//            ItemsSource="{Binding Produkty}"
//            SelectedItem="{Binding WybranyProdukt, Mode=TwoWay}"
//            CanUserAddRows="False" Margin="5" Height="200">
//    <DataGrid.Columns>
//      <DataGridTextColumn Header="ID"    Binding="{Binding Id}"    IsReadOnly="True" Width="50"/>
//      <DataGridTextColumn Header="Nazwa" Binding="{Binding Nazwa}" Width="*"/>
//      <DataGridTextColumn Header="Cena"  Binding="{Binding Cena}"  Width="80"/>
//    </DataGrid.Columns>
//  </DataGrid>

using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Collections.ObjectModel;
using System.Windows;

// Model z INotifyPropertyChanged – konieczne aby UI reagowało na zmiany
public class Produkt : INotifyPropertyChanged
{
    private string _nazwa = "";
    private double _cena;

    public int    Id    { get; set; }

    public string Nazwa
    {
        get => _nazwa;
        set { _nazwa = value; OnPropertyChanged(); }
    }

    public double Cena
    {
        get => _cena;
        set { _cena = value; OnPropertyChanged(); OnPropertyChanged(nameof(CenaStr)); }
    }

    public string CenaStr => $"{_cena:F2} zł";  // tylko do wyświetlania

    public event PropertyChangedEventHandler? PropertyChanged;
    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}

// ════════════════════════════════════════
//   MAINWINDOW – DataContext = this
// ════════════════════════════════════════
public partial class MainWindow : Window, INotifyPropertyChanged
{
    public ObservableCollection<Produkt> Produkty { get; } = new();

    private Produkt? _wybrany;
    public Produkt? WybranyProdukt
    {
        get => _wybrany;
        set { _wybrany = value; OnPropertyChanged(); }
    }

    public MainWindow()
    {
        InitializeComponent();
        DataContext = this;   // potrzebne dla {Binding}

        Produkty.Add(new Produkt { Id=1, Nazwa="Laptop",  Cena=3500 });
        Produkty.Add(new Produkt { Id=2, Nazwa="Telefon", Cena=1200 });
    }

    public event PropertyChangedEventHandler? PropertyChanged;
    protected void OnPropertyChanged([CallerMemberName] string? name = null)
        => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
}
""")
}

CSHARP["WPF C# – MessageBox, walidacja, konwersje typów"] = {
    "prefix": "4QWpfUtils",
    "description": "MessageBox, TryParse, string/int/double konwersje, DateTime – INF04",
    "body": body(r"""
using System;
using System.Windows;

// ════ MESSAGEBOX ═══════════════════════
// Informacja
MessageBox.Show("Zapisano!", "Sukces",
    MessageBoxButton.OK, MessageBoxImage.Information);

// Pytanie – Tak/Nie
var odp = MessageBox.Show("Usunąć rekord?", "Potwierdzenie",
    MessageBoxButton.YesNo, MessageBoxImage.Question);
if (odp == MessageBoxResult.Yes) Console.WriteLine("Usuwam...");

// Błąd
MessageBox.Show("Coś poszło nie tak!", "Błąd",
    MessageBoxButton.OK, MessageBoxImage.Error);

// Ostrzeżenie z OK/Anuluj
var res = MessageBox.Show("Dane niekompletne, kontynuować?", "Uwaga",
    MessageBoxButton.OKCancel, MessageBoxImage.Warning);

// ════ KONWERSJE TYPÓW ════════════════════

// String → liczba (bezpieczne, bez wyjątku)
if (double.TryParse(txtCena.Text, out double cena))
    Console.WriteLine($"Cena: {cena:F2}");
else
    txtBlad.Text = "Nieprawidłowa cena!";

if (int.TryParse(txtWiek.Text, out int wiek))
    Console.WriteLine($"Wiek: {wiek}");

// Liczba → string
string s1 = 42.ToString();
string s2 = 3.14.ToString("F2");       // "3.14"
string s3 = 1234567.ToString("N0");    // "1 234 567" (z separatorem)

// DateTime
DateTime teraz = DateTime.Now;
string data = teraz.ToString("dd.MM.yyyy");        // "07.05.2024"
string czas = teraz.ToString("HH:mm:ss");          // "15:30:00"
string pelna = teraz.ToString("dd.MM.yyyy HH:mm"); // "07.05.2024 15:30"

// ════ WALIDACJA (funkcja pomocnicza) ════
private bool WalidujPole(string tekst, string nazwaPolaUI, int minDl = 1)
{
    if (string.IsNullOrWhiteSpace(tekst))
    {
        txtBlad.Text = $"{nazwaPolaUI} nie może być puste!";
        return false;
    }
    if (tekst.Length < minDl)
    {
        txtBlad.Text = $"{nazwaPolaUI} musi mieć co najmniej {minDl} znaki!";
        return false;
    }
    txtBlad.Text = "";
    return true;
}
""")
}

CSHARP["WPF C# – ComboBox, RadioButton, CheckBox"] = {
    "prefix": "4QWpfControls",
    "description": "ComboBox, RadioButton, CheckBox – obsługa w code-behind – INF04",
    "body": body(r"""
// ════════════════════════════════════════
//   XAML – wklej do <StackPanel>:
//
//  <ComboBox x:Name="cbKategoria" Margin="5">
//    <ComboBoxItem Content="Elektronika"/>
//    <ComboBoxItem Content="Edukacja"/>
//    <ComboBoxItem Content="Sport"/>
//  </ComboBox>
//
//  <RadioButton x:Name="rbMaly"   Content="Mały"   GroupName="rozmiar" Margin="5"/>
//  <RadioButton x:Name="rbSredni" Content="Średni" GroupName="rozmiar" Margin="5" IsChecked="True"/>
//  <RadioButton x:Name="rbDuzy"   Content="Duży"   GroupName="rozmiar" Margin="5"/>
//
//  <CheckBox x:Name="chkDostawa" Content="Dostawa gratis" Margin="5"/>
//  <Button Content="Zatwierdź" Click="BtnZatwierdz_Click" Margin="5"/>
// ════════════════════════════════════════

// ── ComboBox – wypełnianie z kodu ───────
cbKategoria.Items.Clear();
foreach (var kat in new[] { "Elektronika", "Edukacja", "Sport" })
    cbKategoria.Items.Add(kat);
cbKategoria.SelectedIndex = 0;

// Odczyt wybranego elementu
string wybrana = cbKategoria.SelectedItem?.ToString() ?? "";

// Zdarzenie zmiany
cbKategoria.SelectionChanged += (s, e) =>
{
    string sel = cbKategoria.SelectedItem?.ToString() ?? "";
    Console.WriteLine($"Wybrano: {sel}");
};

// ── RadioButton ──────────────────────────
private void BtnZatwierdz_Click(object sender, RoutedEventArgs e)
{
    // Sprawdź który RadioButton jest zaznaczony
    string rozmiar = rbMaly.IsChecked   == true ? "Mały"
                   : rbSredni.IsChecked == true ? "Średni"
                   :                              "Duży";

    // CheckBox
    bool darmowaDostawa = chkDostawa.IsChecked == true;

    MessageBox.Show($"Rozmiar: {rozmiar}, Dostawa: {(darmowaDostawa ? "gratis" : "płatna")}");
}
""")
}

CSHARP["WPF C# – obsługa wyjątków, try/catch/finally"] = {
    "prefix": "4QCsExceptions",
    "description": "try/catch/finally, własny wyjątek, walidacja w WPF – INF04",
    "body": body(r"""
using System;
using System.Windows;

// ════ PODSTAWOWE WYJĄTKI ════════════════
try
{
    int x = int.Parse(txtWiek.Text);    // FormatException gdy nie liczba
    int y = 10 / x;                     // DivideByZeroException
    Console.WriteLine($"Wynik: {y}");
}
catch (FormatException)
{
    MessageBox.Show("To nie jest liczba!", "Błąd", MessageBoxButton.OK, MessageBoxImage.Error);
}
catch (DivideByZeroException)
{
    MessageBox.Show("Nie dziel przez zero!", "Błąd", MessageBoxButton.OK, MessageBoxImage.Error);
}
catch (Exception ex)  // złap wszystko inne
{
    MessageBox.Show($"Nieoczekiwany błąd: {ex.Message}", "Błąd");
}
finally
{
    // Zawsze się wykona – np. zamknij plik, połączenie
    Console.WriteLine("Blok finally");
}

// ════ WŁASNY WYJĄTEK ════════════════════
public class BladWalidacjiException : Exception
{
    public string Pole { get; }
    public BladWalidacjiException(string pole, string message)
        : base(message)
    {
        Pole = pole;
    }
}

public class WiekNieprawidlowyException : BladWalidacjiException
{
    public WiekNieprawidlowyException(int wiek)
        : base("Wiek", $"Nieprawidłowy wiek: {wiek}. Musi być 0–150.") { }
}

// Rzucanie
private static void SprawdzWiek(int wiek)
{
    if (wiek < 0 || wiek > 150)
        throw new WiekNieprawidlowyException(wiek);
}

// Użycie
try
{
    SprawdzWiek(-5);
}
catch (WiekNieprawidlowyException ex)
{
    MessageBox.Show(ex.Message);  // "Nieprawidłowy wiek: -5. Musi być 0–150."
    Console.WriteLine($"Pole: {ex.Pole}");  // "Wiek"
}
""")
}

# ═══════════════════════════════════════════════════════
#   ZAPIS WSZYSTKICH PLIKÓW JSON
# ═══════════════════════════════════════════════════════
pliki = {
    "python.json":  PY,
    "react.json":   REACT,
    "kotlin.json":  KOTLIN,
    "csharp.json":  CSHARP,
}
for nazwa, dane in pliki.items():
    sciezka = os.path.join(SNIP, nazwa)
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(dane, f, ensure_ascii=False, indent=2)
    print(f"✓ Zapisano: {sciezka}")

# Kopiuj express.json
shutil.copy(
    "/mnt/user-data/uploads/1778151403282_express.json",
    os.path.join(SNIP, "express.json")
)
print("✓ Skopiowano: express.json")

print("\n✅ Wszystkie pliki snippetów gotowe!")
