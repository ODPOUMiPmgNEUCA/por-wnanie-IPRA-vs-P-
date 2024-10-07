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


# File uploader dla CSV lub Excel
uploaded_file = st.file_uploader("Wrzuć Raport promocyjny", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Sprawdzenie, jaki typ pliku został załadowany
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.write(df.head())  # Wyświetlanie danych, jeśli są dostępne
    except Exception as e:
        st.error(f"Wystąpił błąd podczas wczytywania pliku: {e}")
else:
    st.warning("Proszę załadować plik przed próbą jego przetwarzania.")

'''
df = st.file_uploader(
    label = "Wrzuć Raport promocyjny"
)
if df:
    df = pd.read_csv(df)
    st.write(df.head())
'''

# Wybieranie tylko określonych kolumn z DataFrame
kolumny = [
    'Nazwa Promocji', 'Nr producenta sprzedażowego', 'Nazwa producenta sprzedażowego',
    'Skład (SPR,SGL)', 'Czy dopuszcza rabat kontraktowy', 'Id Materiału', 
    'Nazwa Materiału', 'Rabat P+'
]
df
'''

# Filtruj kolumny w DataFrame
df = df[kolumny]
df = df[(df['Nazwa promocji'].str.contains('P\+') | df['Nazwa promocji'].str.contains('PARTNER')) &  ~df['Nazwa promocji'].str.contains('WTP\+')]
df

'''






'''
    

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
