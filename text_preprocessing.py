
import numpy as np
import pandas as pd
from stempel import StempelStemmer
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import copy
from sklearn.feature_extraction.text import CountVectorizer

stemmer = StempelStemmer.polimorf()

with open('data\stop_words_polish.txt', encoding="utf-8") as f:
    stopwords = f.readlines()

for i in range(len(stopwords)):
    stopwords[i] = stopwords[i].replace('\n', '')

grouped_emotions = pd.read_csv('data\grouped_emotions_dictionary.csv')
grouped_emotions.set_index('word', inplace=True)
grouped_emotions


def load_file(filepath):
    """
    Wczytuje plik tekstowy i zwraca jego zawartość jako string
    """
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    return text

def create_description_column(filepath, posting_delimiter='********'):
    """
    Potrzebne tylko kiedy wczytujemy dane z pliku tekstowego, w przypadku wczytywania z csv zamiast outputu tej funkcji podajemy df['description']
    """
    text = load_file(filepath)
    
    text_transformed = text.replace('\n', ' ').replace('\r', '')
    opisy_ofert = text_transformed.split(posting_delimiter)
    return opisy_ofert

def preprocess_text(description_column, stopwords, stemmer):
    """
    Usuwanie stopwordsów oraz stemming
    """
    
    opisy_ofert_bez_stopwords = []
    for opis in description_column:
        opis_bez_stopwords = opis
        for stopword in stopwords:
            opis_bez_stopwords = re.sub(r"\b%s\b" %stopword, '', opis_bez_stopwords)
        opisy_ofert_bez_stopwords.append(opis_bez_stopwords)

    opisy_po_stemmingu = []
    for opis in opisy_ofert_bez_stopwords:
        opisy_po_stemmingu.append([stemmer.stem(word.lower()) for word in opis.split()])

    return opisy_po_stemmingu


def create_tfidf_frame(opisy_ofert):
    """
    Tworzy ramkę danych ze słowami jako kolumnami i wartościami tfidf
    """
    vectorizer = TfidfVectorizer()
    cechy_tfidf = vectorizer.fit_transform(opisy_ofert)

    tfidf = cechy_tfidf.toarray()
    cechy_df = pd.DataFrame(tfidf, columns=vectorizer.get_feature_names_out())

    # Wyświetlanie ramki danych
    return cechy_df


def create_tfidf_columns(df_tfidf):
    tfidf_cols = pd.DataFrame([df_tfidf.iloc[:,:-1].sum(axis=1), df_tfidf.iloc[:,:-1].mean(axis=1)]).T
    tfidf_cols.columns=['tfidf_sum', 'tfidf_mean']
    return tfidf_cols

def create_emotions_columns(opisy_ofert, grouped_emotions):
    # Tworzenie wektora cech
    vectorizer = CountVectorizer()
    cechy = vectorizer.fit_transform(opisy_ofert)

    # Konwersja wektora cech do ramki danych
    df_emotions = pd.DataFrame(cechy.toarray(), columns=vectorizer.get_feature_names_out())

    for column in  list(df_emotions.columns):
        if column in list(grouped_emotions.index):
            df_emotions[column] *= grouped_emotions.loc[column,'emotions']

    emotion_cols = pd.DataFrame([df_emotions.sum(axis=1), df_emotions.mean(axis=1)]).T
    emotion_cols.columns=['emotions_sum', 'emotions_mean']
    return emotion_cols

def create_text_based_columns(df, text_column):
    df['text_length'] = df[text_column].apply(len)

    #liczba dużych liter
    df['capital_letters_count'] = df[text_column].apply(lambda x: sum(1 for c in x if c.isupper()))

    #zliczenia liczb
    df['numbers_count'] = df[text_column].apply(lambda x: sum(1 for c in x if c.isdigit()))

    #zliczenia znaków
    df['question_marks_count'] = df[text_column].apply(lambda x: x.count('!'))

    #zliczenia znaków walutowych
    df['currency_signs_count'] = df[text_column].apply(lambda x: x.count('$') + x.count('€') + x.count('£') + len(re.findall(r'\bzł\b|zł\b', x, re.IGNORECASE)))

        #liczba słów całych wielka litera
    df['capital_words_count'] = df[text_column].apply(lambda x: sum(1 for word in x.split() if word.isupper()))

    #możliwy adres email
    df['possible_email'] = df[text_column].apply(lambda x: ','.join([word for word in x.split() if '@' in word]))

    #możliwy adres rzeczywisty
    df['possible_address'] = df[text_column].apply(lambda x: ', '.join(re.findall(r'.{0,10}ul\..{0,10}', x)))

    #niepolskie słowa
    df['non_polish_char_count'] = df[text_column].apply(lambda x: sum(1 for char in ''.join(x) if char.strip() and (not char.isalpha() or char.lower() not in 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż')))

    #możliwy numer telefonu
    df['possible_phone_numbers'] = df[text_column].apply(lambda x: re.findall(r'\d+(?:[-\s]?\d+)+', x))
    df['possible_phone_numbers'] = df['possible_phone_numbers'].apply(lambda x: ', '.join(number for number in x if sum(1 for c in number if c.isdigit()) >= 9 and sum(1 for c in number if c.isdigit()) < 13))
    return df

def create_keywords_counter_column(df, keywords, output_column_name, ispreprocessed=False):
    # final_df = df_desc_preprocessed.merge(tfidf_cols, left_index=True, right_index=True)
    # final_df = final_df.merge(emotion_cols, left_index=True, right_index=True)
    # final_df = create_text_based_columns(final_df, 'description')


    # all_keywords = ["dowód" , "zawsze" , "nigdy" , "pesel" , "kryptowaluty" ,  "nic" , "wszystko" , "konto bankowe"]
    if ispreprocessed:
        text_column = 'preprocessed_description'
    else:  
        text_column = 'description'
    keywords_counter_col = [0]* len(df[text_column])

    for i in range(len(df['description'])):
        for keyword in keywords:
            keywords_counter_col[i] += len(re.findall(keyword, df[text_column][i].lower()))

    df[output_column_name] = keywords_counter_col
    return df

# %% [markdown]
# # Funkcja do tworzenia kolumn z pojedynczego tekstu

# %%
def process_single_row(single_posting_desc):
    df = pd.DataFrame([single_posting_desc], columns=["description"])
    other_cols = df.drop(columns=['description'])
    opisy = preprocess_text(df['description'].replace('\n', '').replace('\r', ''), stopwords, stemmer)
    opisy_full = []

    for opis in opisy:
        try:
            opisy_full.append(' '.join(opis))
        except:
            print(opis)
            opisy_full.append('INVALID_DATA')
            continue
    df_desc_preprocessed = pd.DataFrame([list(df['description']), opisy_full]).T
    df_desc_preprocessed.columns = ['description', 'preprocessed_description']
    df_desc_preprocessed['index'] = df_desc_preprocessed.index
    df_desc_preprocessed = df_desc_preprocessed[df_desc_preprocessed['preprocessed_description'] != 'INVALID_DATA'].reset_index(drop=True)

    df_tfidf = create_tfidf_frame(df_desc_preprocessed['preprocessed_description'])
    tfidf_cols = create_tfidf_columns(df_tfidf)
    emotion_cols = create_emotions_columns(df_desc_preprocessed['preprocessed_description'], grouped_emotions)


    final_df = df_desc_preprocessed.merge(tfidf_cols, left_index=True, right_index=True)
    final_df = final_df.merge(emotion_cols, left_index=True, right_index=True)
    final_df = create_text_based_columns(final_df, 'description')
    
    personal_info_keywords = ["dowód" , "pesel", "konto", "numer", "adres", "numer", "karty", "kredytowej"]
    inspiring_keywords = ["niepowtarzalna", "super", "dziś", "dzisiaj", "wyjątkowa", "ekstra", "zawsze", "nigdy", "nic", "wszystko"]
    money_related_keywords = ["gwarantowana", "zysk", "obrót", "zyski", "najlepsza", "gwarantowany", "najlepszy","kryptowaluty"]

    #all_keywords_stemmed = [stemmer.stem(word) for word in all_keywords]

    final_df = create_keywords_counter_column(final_df, personal_info_keywords, "personal_info_keywords_count")
    final_df = create_keywords_counter_column(final_df, inspiring_keywords, "inspiring_keywords_count")
    final_df = create_keywords_counter_column(final_df, money_related_keywords, "money_related_keywords_count")

    final_df = final_df.merge(other_cols, left_index=True, right_index=True)
    return final_df


def create_final_dataframe(df):

    df = pd.read_csv(df)
    other_cols = df.drop(columns=['description'])
    opisy = preprocess_text(df['description'].replace('\n', '').replace('\r', ''), stopwords, stemmer)
    opisy_full = []

    for opis in opisy:
        try:
            opisy_full.append(' '.join(opis))
        except:
            print(opis)
            opisy_full.append('INVALID_DATA')
            continue
    df_desc_preprocessed = pd.DataFrame([list(df['description']), opisy_full]).T
    df_desc_preprocessed.columns = ['description', 'preprocessed_description']
    df_desc_preprocessed['index'] = df_desc_preprocessed.index
    df_desc_preprocessed = df_desc_preprocessed[df_desc_preprocessed['preprocessed_description'] != 'INVALID_DATA'].reset_index(drop=True)

    df_tfidf = create_tfidf_frame(df_desc_preprocessed['preprocessed_description'])
    tfidf_cols = create_tfidf_columns(df_tfidf)
    emotion_cols = create_emotions_columns(df_desc_preprocessed['preprocessed_description'], grouped_emotions)

    final_df = df_desc_preprocessed.merge(tfidf_cols, left_index=True, right_index=True)
    final_df = final_df.merge(emotion_cols, left_index=True, right_index=True)
    final_df = create_text_based_columns(final_df, 'description')


    personal_info_keywords = ["dowód" , "pesel", "konto", "numer", "adres", "numer", "karty", "kredytowej"]
    inspiring_keywords = ["niepowtarzalna", "super", "dziś", "dzisiaj", "wyjątkowa", "ekstra", "zawsze", "nigdy", "nic", "wszystko"]
    money_related_keywords = ["gwarantowana", "zysk", "obrót", "zyski", "najlepsza", "gwarantowany", "najlepszy","kryptowaluty"]

    #all_keywords_stemmed = [stemmer.stem(word) for word in all_keywords]

    final_df = create_keywords_counter_column(final_df, personal_info_keywords, "personal_info_keywords_count")
    final_df = create_keywords_counter_column(final_df, inspiring_keywords, "inspiring_keywords_count")
    final_df = create_keywords_counter_column(final_df, money_related_keywords, "money_related_keywords_count")

    final_df = final_df.merge(other_cols, left_index=True, right_index=True)
    return final_df

