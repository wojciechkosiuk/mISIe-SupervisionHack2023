
Spis treści:
 -web scraping (informacje, co uzyskujemy)
 -model (dlaczego taki, jak działa, wyjaśnienia)
 -strona użytkownika - django

## Web scraping
Szukaliśmy danych dotyczących ogłoszeń o pracę na dwóch portalach:
- *www.olx.pl*
- *sprzedajemy.pl*

Funkcje związane ze scrapingiem przechowujemy w 3 plikach:

- *scraping_functions.py* - funkcje, które można wykorzystać ogólnie przy pracy ze stronami
- *olx_functions.py* - przygotowane funkcje do zbierania interesujących nas danych dotyczących ofert pracy z portalu olx.
- *sprzedajemy_functions.py* - przygotowane funkcje to zbierania danych z potalu sprzedajemy.

Do scrapingu posługiwaliśmy się w dużej mierze tagami z CSS. Podobny scraping można wykonać na innych stronach z niedużym problemem. Kod powinien nie mieć problemów z działaniem dopóki nie zmieni się struktura strony.


### Oferty
Udało nam się znaleźć ponad 28 tysięcy linków do unikalnych ofert prac z portalu *olx* i ponad 5 tysięcy linków do ofert na portalu *sprzedajemy*. Łącznie mamy więc około 32-33 tys. linków.


#### Dane z linkami
Linki przechowujemy w folderze data odpowiednio w plikach:

- *links_olx.txt*
- *links_sprzedajemy.txt*

  przy czym przy obu trzeba dokleić ich domenowe prefixy.

#### Dane ze webscrapingu

Przykładowe dane otrzymane z webscrapingu z obu stron znajdują się odpowiednio w plikach:

- *olx_1000.csv*
- *sprzedajemy_1000.csv*


#### Opis kolumn:

- link - pełny URL do oferty pracy
- dodane-data - data dodania oferty na serwis (format YYYY-mm-dd)
- title - tytuł oferty
- category-tree-item - kategorie poodzielane "/"
- user-profile-link - pełny URL do profilu użytkownika wystawiającego ofertę 
- filters - w olx - filtry przy wyszukiwaniu, w sprzedajemy nie ma odpowiednika
- description - pełny opis oferty
- pay_low - jeśli na stronie zarobki są w podane jako przedział to jest to dolna granica, jeśli jest podana konkretna wartość to przyjmuje ją
- pay_high - jeśli na stronie zarobki są w podane jako przedział to jest to górna granica, jeśli jest podana konkretna wartość to przyjmuje ją
- pay_currency - waluta w jakiej podane są zarobki
- pay_period - typ płacanie (np. godz. brutto, albo mies. brutto)
- Lokalizacja - lokalizacja pracy
- Wymiar pracy - wymiar pracy (pełen etat, pół etatu itd.)
- Typ umowy - np. umowa o pracę
- user-profile-link-hash - jest w pliku *olx_1000.csv*, ale ogólnie nigdzie nie jest używany. Nie usunęliśmy tej kolumny, bo już w kolejnych plikach usuwamy ją w kodzie.

### *scraping_functions.py*
Dokumentacja funkcji:

`return_soup(url)` służy do pobrania zawartości HTML ze wskazanego URL i przeparsowania jej za pomocą BeautifulSoup. Zwraca obiekt BeautifulSoup:
- argumenty:
    - `url (str)`: Adres URL strony do pobrania.
- zwraca:
    - `BeautifulSoup`: Obiekt BeautifulSoup zawierający sparsowaną zawartość HTML.

`save_url_to_html(url, filename)` służy do zapisania zawartości HTML strony internetowej do pliku o rozszerzeniu html. Plik można następnie otworzyć w przeglądarce w takiej samej formie w jakiej został pobrany. Po uzyskaniu listy użytkowników u których model wykrył fałszywe ogłoszenie za pomocą tej funkcji zapisujemy **dowody**, czyli plik html profilu użytkownika. Są one w  /FakeJobHunter_Dashboard/suspicious_users

- argumenty:
    - `url (str)`: Adres URL strony do zapisania.
    - `filename` (str): Nazwa pliku, do którego ma być zapisana zawartość HTML. Do nazwy pliku dodawany jest prefix z datą stworzenia zapisu. Plik zapisywany jest w folderze htmls. 

### *olx_functions.py*
Dokumentacja funkcji:


`get_info_about_job_olx(url)` pobiera informacje o ofercie pracy z witryny OLX. Funkcja znajduje po tagach CSS interesujące nas fragmenty strony. Każde wyszukanie jest zawarte w bloku `try-except`.

- argumenty:
    - `url (str)` - adres URL strony z ofertą pracy na OLX.
- zwracane:
    - `pandas.DataFrame` - Ramka danych zawierająca surowe informacje o ofercie pracy.


`adjust_olx_df(df)` służy do dostosowania ramki otrzymanej z funkcji `get_info_about_job_olx(url).

- argumenty:
    - df (pandas.DataFrame) - ramka danych otrzymana z funkcji `get_info_about_job_olx(url)`
- zwracane:
    - pandas.DataFrame - Dostosowana ramka danych zawierająca informacje o ofertach pracy, którą można wykorzystać do dalszej analizy. 

Towarzyszą jej funkcje pomocnicze:

- `remove_dodane(str: x)` - usuwająca przedrostek "Dodane " z daty
- `convert_to_datetime(str: x)` - zamieniająca datę na objekt `datetime`
- `remove_id(str: x)` - usuwająca przedrostek "ID:" z id ogłoszenia
- `remove_opis(str: x)` - usuwająca przedrostek "OPIS: " z opisu ogłoszenia
- `add_olx(str: x)` - dodająca przedrostek domeny olx do reszty linku, który jest niepełny
- `replace_commas(str: x)` - zamieniająca "," na "."
- `convert_str_to_float(str: x)` - zamieniająca zarobki na floaty jeśli są w formie ułamka


`scrape_olx_links()` służy do pobierania linków ofert pracy z witryny OLX. Zapisuje je w niepełnej formie (bez przedrostka domeny olx) w pliku *linki_olx*.txt.

### *sprzedajemy_functions.py*
Ogólnie podobne funkcje jak w przypadku OLX. Jest też podobne nazewnictwo. Do uzupełnienia.....


## Tworzenie modelu
Do stworzenia modelu użyliśmy plików:
 - Create_dictionary.ipynb
 - bag_of_words.ipynb
 - model_research.ipynb
 - Models.ipynb

### Create_dictionary.ipynb
Korzystając ze słownika ogólnie dostępnego (nawet dla commercial use) Słowosieci w wersji 4.2 tworzymy własne mapowanie słów do wskaźnika emocjonalnego wydźwięku i zapisujemy

### bag_of_words.ipynb
Nasz preprocessing danych polegał głównie na wyszukiwaniu kluczowych informacji z tekstu, ale także na analizie NLP danego tekstu
Word Tokenization -> Stemming -> TF-IDF (Term Frequency-Inverse Document Frequency) to metoda stosowana w analizie tekstu, która mierzy ważność słów w dokumencie w kontekście całej kolekcji dokumentów. Przyznaje ona wyższe wagi słowom, które występują często w danym dokumencie, ale rzadziej w innych dokumentach, co pozwala identyfikować istotne słowa charakterystyczne dla danego tekstu. Analiza tekstu i tworzenie nowych kolum.
Między innymi:
- budowanie metryki do określenia emocjonalnego zbarwienia ogłoszenia, 
- uzyskiwanie kolumn potencjalny number telefonu, adres mailowy, adres fizyczny z tekstu
- wyszukiwanie słów z danego tematu
- kolumny określające stylistyczny i fizyczny format tekstu
- liczność znaków niealfabetycznych w tekście

'Dodatkowe kolumny jakie można dodać to liczba błędów ortograficznych, informacje o nicku autora' - nie używamy z powodu podejścia do tuningowania zbioru. 


### model_research.ipynb
Stworzono tu alternatywne podejście używające klastrowania, nie wykorzystaliśmy go finalnie, ale zostawiamy poglądowo kod.

### Models.ipynb
Trenujemy model, zapisujemy go, tworzymy finalne csv z wyscrappowanych danych do zapisu - gotowe do robienia z nich raportów oraz otrzymujemy listę użytkowników z potencjalnymi fałszywymi ogłoszeniami.
**WYJAŚNIENIE PODEJŚCIA** - Zastosowaliśmy Anomaly Detection, model Isolation Forest po tuningu parametrów. Używamy takiego podejścia, ponieważ jest skuteczny w podejściach fraud detection. Z powodu braku datasetu z labelami uczenie przeprowadziliśmy w taki sposób. Dane tekstowe od organizatorów miały informacje czy są fałszywe czy nie, więc dołączyliśmy je do wyscrappowanych przez nas danych. Mogliśmy tak zrobić, ponieważ używamy tylko tekstu ogłoszenia do tworzenia kolumn do modelu. Trenowaliśmy Isolation Forest ustawiając parametry tak aby zmaksymalizować liczbę wykrytych reklam z datasetu z labelami od organizatorów, jednocześnie minimalizując liczbę wykrytych jako potencjalne reklamy z danych gdzie label wskazywał o prawdziwości ogłoszenia.
Otrzymaliśmy 15/24 wykryte reklamy ze wszystkich oraz 1/13 wykrytą reklamę ze zbioru prawdziwych. **Te statystyki służyły tylko do odpowiedniego tuningu isoforest, nie do ewaluacji. ** Ustawiając parametr contamination=0.033 gwarantujemy że przy trenowaniu naszych plików otrzymujemy 3.3% zaklasyfikowanych jako outliery - u nas fakejob. 
**Testy**
Testując otrzymaliśmy około 3% zakwalifikowania ze zbioru jako potencjalne fałszywe oferty (66 ofert).  Z nich sprawdziliśmy ręcznie ich tekst klasyfikując czy faktycznie są fałszywe. Z naszych 66 wykrytych uznajemy, że 75% z błędem statystycznym 5% zostało wykrytych fałszywych ofert. 

**Ulepszenie**
Dodanie o labelowanych danych motywujemy tym, że musieliśmy dodać fałszywe oferty aby być pewnym że są tam takowe. Przy lepszym, większym zbiorze, np z naszych wyscrapowanych danych (zostało tam utowrzonych wiele kolumn, z których nie skorzystaliśmy) jest możliwe otrzymanie pewniejszych wyników.

**Wyjaśnialność**
Dodaliśmy wyjaśnialność do naszego modelu poprzez użycie Shap for Forest, dzięki temu tworzyła się wizualizacja dla konkretnej obserwacji (oferty) i otrzymaliśmy z tego metrykę służącą jako wychylenie od standardowej obserwacji (uzyskanie z shap_values). Potrzebne było przeskalowanie tych wartości aby otrzymać z tego prawdopodobieństwo.

Z wyjaśnialności shapa, czyli wpływu konkretnej kolumny na decyzje wygenerowaliśmy komunikat tłumaczący model, więc ekspert działający na stronie dostaje prawdopodobieństwo modelu oraz tłumaczenie dlaczego ma ono konkretną wartość. Uważamy, że łatwy dostęp do wyjaśnialności, pomoże określić ekspertowi poprzez zwrócenie jego uwagi na pewne aspekty.

**Dodatkowe kolumny**
Otrzymujemy kolumny o potencjalnym adresie fizycznym, adresie email, telefonie z ogłoszenia
Wykrywamy użytkowników z ogłoszeniem uznanym ponad danego thresholdu jako fałszywe i zapisujemy je jako BlackList  w:
/FakeJobHunter_Dashboard/suspicious_users/fake_users.csv oraz mamy możliwość zapisania tego profilu do pliku w formacie html jako dowód (nie jest to podłączone do django, ale mamy zaimplementowane funkcje, które wywołaliśmy z poziomu notebooka).

## Django
Django zostało zaprezentowane wizualnie za pomocą nagrania, które dodaliśmy do platformy. Przetrzymujemy tam skrypty do potrzebnych funkcji, mamy baze danych z ogłoszeniami. Można rozwinąć o dodatkowe wykresy w oparciu o stworzoną tam bazę danych.

## Requirements
Pakiety, których używaliśmy znajdują się w pliku *requirements.txt*.


