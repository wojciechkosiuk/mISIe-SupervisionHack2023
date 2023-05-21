

## Web scraping
Szukaliśmy danych dotyczących ogłoszeń o pracę na dwóch portalach:
- *www.olx.pl*
- *sprzedajemy.pl*

Funkcje związane ze scrapingiem przechowujemy w 3 plikach:

- *scraping_functions.py* - funkcje, które można wykorzystać ogólnie przy pracy ze stronami
- *olx_functions.py* - przygotowane funkcje do zbierania interesujących nas danych dotyczących ofert pracy z portalu olx.
- *sprzedajemy_functions.py* - przygotowane funkcje to zbierania danych z potalu sprzedajemy.


### *scraping_functions.py*
Dokumentacja funkcji:

-  `return_soup(url)` służy do pobrania zawartości HTML ze wskazanego URL i przeparsowania jej za pomocą BeautifulSoup. Zwraca obiekt BeautifulSoup:
    - argumenty:
        - `url` (str): Adres URL strony do pobrania.
    - zwraca:
        - `BeautifulSoup`: Obiekt BeautifulSoup zawierający sparsowaną zawartość HTML.

- `save_url_to_html(url, filename)` służy do zapisania zawartości HTML strony internetowej do pliku o rozszerzeniu html. Plik można nastpępnie otworzyć w przeglądarce w takiej samej formie w jakiej został pobrany.

    - argumenty:
        - `url` (str): Adres URL strony do zapisania.
        - `filename` (str): Nazwa pliku, do którego ma być zapisana zawartość HTML. Do nazwy pliku dodawany jest prefix z datą stworzenia zapisu. Plik zapisywany jest w folderze htmls. 

### *olx_functions.py*
Dokumentacja funkcji:






## Requirements
Pakiety, których używaliśmy znajdują się w pliku *requirements.txt*.


