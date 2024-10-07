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
df['Rabat P+'] = df['Rabat Promocyjny'] / -100
df


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
