from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import gspread
import random
import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


scopes = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


json_keyfile_dict = st.secrets["service_account"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json_keyfile_dict, 
    scopes
)

# PyDrive2 の認証設定
gauth = GoogleAuth()
gauth.credentials = credentials
drive = GoogleDrive(gauth)

st.markdown('# ユーザアンケート 終了ページ')

st.markdown('この度は、調査にご協力いただき誠にありがとうございました。', unsafe_allow_html=True)

st.markdown('最後に、以下のgoogleフォームに評価アンケートを記入して提出をお願いします。')

st.markdown(
    '<a href="https://forms.gle/5XUYnMaCmubZfLg78" target="_blank">評価アンケート</a>',
    unsafe_allow_html=True
)