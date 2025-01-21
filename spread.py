from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import gspread
import random
import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

#file_name = 'GC_test_by_gspread'

#scopes = [
#    "https://www.googleapis.com/auth/spreadsheets",
#    "https://spreadsheets.google.com/feeds",
#    "https://www.googleapis.com/auth/drive.file",
#    "https://www.googleapis.com/auth/drive"
#]

scopes = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#'../service_account.json',

# Credentials 情報を取得
#credentials = ServiceAccountCredentials.from_json_keyfile_name(
#    service_account,
#    scopes=scopes
#)
#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["service_account"],
#    scopes=scopes
#)

json_keyfile_dict = st.secrets["service_account"]

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json_keyfile_dict, 
    scopes
)


#json_keyfile_path = '../service_account.json'

# サービスアカウントキーを読み込む
#credentials = ServiceAccountCredentials.from_json_keyfile_name(
#    json_keyfile_path, scopes)

# PyDrive2 の認証設定
gauth = GoogleAuth()
gauth.credentials = credentials
drive = GoogleDrive(gauth)

st.markdown('# ユーザアンケート トップページ')

st.markdown('この度は、調査にご協力いただき誠にありがとうございます。 <br> 以下の指示に従って、順番にタスクを行ってください。', unsafe_allow_html=True)

st.markdown('1. 以下のgoogleフォームから同意書をお読みになり、同フォームに必要事項を記入して提出をお願いします。')

st.markdown(
    '<a href="https://forms.gle/nMGGdrnrMhnfrezx5" target="_blank">研究へのご協力のお願いと参加同意書</a>',
    unsafe_allow_html=True
)

st.markdown('2. 以下の空欄にユーザIDを入力して、提出ボタンを押してください。')

st.session_state.user_random_id = 0

form = st.form(key="test")

with form:
    text1 = st.text_input("user ID")
    #text2 = st.text_input("second")
    submitted = st.form_submit_button(label="Submit")

st.session_state.folder_id = st.secrets["folder_id"]
st.session_state.file_name = text1

if submitted:
    f = drive.CreateFile({
        'title': st.session_state.file_name,
        'mimeType': 'application/vnd.google-apps.spreadsheet',
        "parents": [{"id": st.secrets["folder_id"]}]
    })
    f.Upload()

    st.session_state.file = f

    st.session_state.user_random_id = random.randrange(1,6)

    st.success("File created successfully!")

st.markdown('3. ボタンを押してから数秒お待ちください。上にFile created successfully!と表示されます。<br>表示されなかった場合は、画面をリロードしてもう一度やり直してください。<br>それでも動作しない場合は、お手数をおかけしますがytsuchi28054@g.ecc.u-tokyo.ac.jpまでご連絡ください。',
    unsafe_allow_html=True
)

st.markdown('4. 無事に3を終えたらタスクスタートです。左のサイドバー(表示されない場合は、左上の「>」ボタンを押してください)の上から順番にクリックして、指示に従ってタスクを行ってください。<br>タスクは大きく2種類、それぞれ10問ずつ行います。また、最後に自由記述を含むアンケートへの回答もお願いします。所用時間は30分程度を見込んでいます。',
    unsafe_allow_html=True)


###ランダムに番号を表示して、それに沿ってURLを叩いてもらって問題を解いてもらう


