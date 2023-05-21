

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

`save_url_to_html(url, filename)` służy do zapisania zawartości HTML strony internetowej do pliku o rozszerzeniu html. Plik można nastpępnie otworzyć w przeglądarce w takiej samej formie w jakiej został pobrany.

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





    

## Requirements
Pakiety, których używaliśmy znajdują się w pliku *requirements.txt*.


