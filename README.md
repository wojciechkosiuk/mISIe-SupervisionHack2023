---
IF YOU'RE TRYING TO MAKE THE APP WORK YOU SHOULD CD TO FakeJobHunter_Dashboard DIRECTORY AND RUN THE SERVER FROM THERE.
---

Tworzenie modelu z danych wyscrappowanych połączonych z danymi dostarczonymi z labelami jest w pliku Model.ipynb


Pipeline bag_of_words:
Dane tabularyczne z opisem jako input -> Stworzenie kolumn bazujących na opisie -> Tokenizacja opisu -> Usunięcie stopwordsów -> Stemming -> Użycie TF-IDF (Term Frequency-Inverse Document Frequency - metoda w analizie tekstu, mierząca ważność słów w opisie w kontekście wszystkich opisów) -> Skorzystanie z Open Source dnaych o emocjach danych słów -> Wyliczenie sentymentu danego opisu


