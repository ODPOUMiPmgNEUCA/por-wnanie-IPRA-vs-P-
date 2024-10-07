# -*- coding: utf-8 -*-
"""Soczyste rabaty.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1bfU5lwdNa2GOPWmQ9-URaf30VnlBzQC0
"""

#importowanie potrzebnych bibliotek
import os
import openpyxl
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
import io



st.set_page_config(page_title='Porównanie rabatów - IPRA vs P+', layout='wide')



tabs_font_css = """
<style>
div[class*="stTextInput"] label {
  font-size: 26px;
  color: black;
}
div[class*="stSelectbox"] label {
  font-size: 26px;
  color: black;
}
</style>
"""



df = st.file_uploader(
    label = "Wrzuć Raport promocyjny"
)
if df:
    df = pd.read_csv(df, sep=';')
    st.write(df.head())

# Wybieranie tylko określonych kolumn z DataFrame
kolumny = [
    'Nazwa Promocji', 'Nr producenta sprzedażowego', 'Nazwa producenta sprzedażowego', 'Skład (SPR,SGL)', 'Czy dopuszcza rabat kontraktowy', 'Id Materiału', 
    'Nazwa Materiału', 'Rabat Promocyjny','Cena z cennika głównego','identyfikator promocji','Data obowiązywania promocji od','Data obowiązywania promocji do','Rodzaj warunku płatności',
    'Ilość Klientów','Nazwa grupy promocyjnej','MPK','Grupa klientów','Czy KDW'

]

# Filtruj kolumny w DataFrame
df = df[kolumny]
df = df[(df['Nazwa Promocji'].str.contains('P\+') | df['Nazwa Promocji'].str.contains('PARTNER')) &  ~df['Nazwa Promocji'].str.contains('WTP\+')]


# Kolumna 'Skład (SPR,SGL)' - zostawiamy tylko 'SGL'
df = df[df['Skład (SPR,SGL)'] == 'SGL']

# Kolumna 'Czy dopuszcza rabat kontraktowy' - zostawiamy tylko '1'
df = df[df['Czy dopuszcza rabat kontraktowy'] == 1]

# Kolumna 'Rodzaj warunku płatności' - zostawiamy tylko 'Standard'
df = df[df['Rodzaj warunku płatności'] == 'Standard']

# Kolumna 'Grupa klientów' - zostawiamy tylko '1'
df = df[df['Grupa klientów'] == 1]

# Kolumna 'Czy KDW' - zostawiamy tylko '0'
df = df[df['Czy KDW'] == 0]

# Kolumna Rabat P+
# Oczyszczanie kolumny 'Rabat Promocyjny'
df['Rabat Promocyjny'] = df['Rabat Promocyjny'].str.replace(',', '.')  # Zastąp przecinki kropkami, jeśli są
df['Rabat Promocyjny'] = df['Rabat Promocyjny'].str.strip()  # Usuwanie białych znaków

# Sprawdzenie wartości po konwersji
st.write("Typ danych w kolumnie 'Rabat Promocyjny':", df['Rabat Promocyjny'].dtype)
df['Rabat Promocyjny1'] = pd.to_numeric(df['Rabat Promocyjny'], errors='coerce')
df['Rabat P+'] = np.where(df['Rabat Promocyjny1'].isna(), 0, df['Rabat Promocyjny1'] / -100)





################################### tero IPRA

# Umożliwienie użytkownikowi wgrania pliku
IPRA = st.file_uploader(
    label="Wrzuć ofertę IPRA", 
    type=["xlsx"]  # Ogranicz do plików xlsx
)

# Sprawdzenie, czy plik został załadowany
if IPRA:
    # Wczytanie arkuszy z pliku Excel
    xls = pd.ExcelFile(IPRA)
    
    # Wczytanie arkusza 'IPRA WHA'
    IPRA_WHA = pd.read_excel(xls, sheet_name='IPRA WHA')
    st.write("Zawartość arkusza 'IPRA WHA':")
    st.write(IPRA_WHA.head())

    # Filtracja arkuszy, które zawierają 'EO' w nazwie
    eo_sheets = [sheet for sheet in xls.sheet_names if 'EO' in sheet]

    # Sprawdzenie, czy jest arkusz zawierający 'EO'
    if eo_sheets:
        # Wczytanie arkusza, który zawiera 'EO'
        EO = pd.read_excel(IPRA, sheet_name=eo_sheets[0])
        
        # Wyświetlenie pierwszych kilku wierszy
        st.write(f"Zawartość arkusza '{eo_sheets[0]}':")
        st.write(EO.head())
    else:
        st.write("Nie znaleziono arkuszy zawierających 'EO'.")


################ PORÓWNANIE
IPRA_WHA = IPRA_WHA.sort_values(by = 'Rabat IPRA',ascending=False)
EO = EO.sort_values(by = 'Rabat IPRA', ascending = False)
df = df.sort_values(by='Rabat P+', ascending=False)

#duplikaty
df = df.drop_duplicates(subset='Id Materiału')
IPRA_WHA = IPRA_WHA.drop_duplicates(subset='Indeks')
EO = EO.drop_duplicates(subset='Indeks')
EO = EO.rename(columns={'Rabat IPRA': 'Rabat EO'})

df_merged = df.merge(IPRA_WHA[['Indeks', 'Rabat IPRA']], left_on='Id Materiału', right_on='Indeks', how='left')
df_merged2 = df_merged.merge(EO[['Indeks', 'Rabat EO']], left_on='Id Materiału', right_on='Indeks', how='left')
columns_to_keep = ['Nazwa Promocji', 'Nr producenta sprzedażowego', 'Nazwa producenta sprzedażowego', 'Skład (SPR,SGL)', 'Czy dopuszcza rabat kontraktowy', 'Id Materiału', 
    'Nazwa Materiału', 'Rabat P+','Rabat IPRA','Rabat EO','Cena z cennika głównego','identyfikator promocji','Data obowiązywania promocji od','Data obowiązywania promocji do','Rodzaj warunku płatności',
    'Ilość Klientów','Nazwa grupy promocyjnej','MPK','Grupa klientów','Czy KDW'
]
df_merged2 = df_merged2[columns_to_keep]

# Dodanie kolumny 'IPRA WHA vs P+' z uwzględnieniem NaN
df_merged2['IPRA WHA vs P+'] = np.where(
    df_merged2['Rabat P+'].isna() | df_merged2['Rabat IPRA'].isna(),  # Sprawdź, czy którakolwiek z kolumn ma NaN
    np.nan,  # Zwróć NaN, jeśli którakolwiek kolumna ma NaN
    np.where(df_merged2['Rabat P+'] >= df_merged2['Rabat IPRA'], 1, 0)  # W przeciwnym razie wykonaj porównanie
)
df_merged2['EO vs P+'] = np.where(
    df_merged2['Rabat P+'].isna() | df_merged2['Rabat EO'].isna(),  # Sprawdź, czy którakolwiek z kolumn ma NaN
    np.nan,  # Zwróć NaN, jeśli którakolwiek kolumna ma NaN
    np.where(df_merged2['Rabat P+'] >= df_merged2['Rabat EO'], 1, 0)  # W przeciwnym razie wykonaj porównanie
)

kolumny = ['Nazwa Promocji', 'Nr producenta sprzedażowego', 'Nazwa producenta sprzedażowego', 'Skład (SPR,SGL)', 'Czy dopuszcza rabat kontraktowy', 'Id Materiału', 
    'Nazwa Materiału', 'Rabat P+','Rabat IPRA','Rabat EO','IPRA WHA vs P+','EO vs P+','Cena z cennika głównego','identyfikator promocji','Data obowiązywania promocji od','Data obowiązywania promocji do','Rodzaj warunku płatności',
    'Ilość Klientów','Nazwa grupy promocyjnej','MPK','Grupa klientów','Czy KDW'
]
df_merged2 = df_merged2[kolumny]
df_merged2


##### IPRA
IPRA_WHA_m = IPRA_WHA.merge(df[['Id materiału','Rabat P+']], left_on='Indeks', right_on='Id materiału', how='left')
EO_m = EO.merge(df[['Id materiału','Rabat P+']], left_on='Indeks', right_on='Id materiału', how='left')
IPRA_WHA_m
EO_m






'''
IPRA = st.file_uploader(
    label = "Wrzuć ofertę IPRA"
)
if IPRA:
    IPRA_WHA = pd.read_excel(IPRA, sheet_name = 'IPRA WHA')
    st.write(IPRA_WHA.head())

IPRA_WHA







    poprzedni = poprzedni.rename(columns={'max_percent': 'old_percent'})
    # Wykonanie left join, dodanie 'old_percent' do pliku 'ostatecznie'
    result = ostatecznie.merge(poprzedni[['Kod klienta', 'old_percent']], on='Kod klienta', how='left')
    result['old_percent'] = result['old_percent'].fillna(0)
    result['Czy dodać'] = result.apply(lambda row: 'DODAJ' if row['max_percent'] > row['old_percent'] else '', axis=1)
    st.write('Kliknij aby pobrać plik z kodami, które kody należy dodać')

    excel_file1 = io.BytesIO()
    with pd.ExcelWriter(excel_file1, engine='xlsxwriter') as writer:
        result.to_excel(writer, index=False, sheet_name='Sheet1')
    excel_file1.seek(0)  # Resetowanie wskaźnika do początku pliku

    # Umożliwienie pobrania pliku Excel
    st.download_button(
        label='Pobierz',
        data=excel_file1,
        file_name='czy_dodac.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    result = result.drop(columns=['old_percent', 'Czy dodać'])


    st.write('Kliknij, aby pobrać plik z formułą max do następnego monitoringu')
    excel_file2 = io.BytesIO()
    with pd.ExcelWriter(excel_file2, engine='xlsxwriter') as writer:
        result.to_excel(writer, index=False, sheet_name='Sheet1')
    excel_file1.seek(0)  # Resetowanie wskaźnika do początku pliku

    # Umożliwienie pobrania pliku Excel
    st.download_button(
        label='Pobierz nowy plik FORMUŁA MAX',
        data=excel_file2,
        file_name='formula_max.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )



'''
