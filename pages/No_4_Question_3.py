import streamlit as st
import pandas as pd
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

# セッション状態の初期化
if "start_button_clicked" not in st.session_state:
    st.session_state.start_button_clicked = False

# ボタンが押されたらセッション状態を更新
if st.button('問題1 スタート！'):
    st.session_state.start = time.time()
    st.session_state.start_button_clicked = True


if st.session_state.start_button_clicked:

    st.markdown("以下のプロフィール情報をもとに、生徒の成績を予想してください。", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("・生徒のプロフィール", unsafe_allow_html=True)

    # ダミーデータの作成
    df = pd.DataFrame({
        '項目': ['家族の人数', '親の同居状況', '母親の仕事', '父親の仕事', 
               'この学校を選んだ理由', '家から学校までの通学時間', '毎週の勉強時間', '学校以外での教育サポート有無', 
               '課外活動(部活)の有無', 'レベルの高い授業を受けたいか', '家族関係', '放課後の自由時間', '友人と出かける頻度', '学校を休んだ回数'],
        #'内容': [0, 0, 0, 4, 0, 2, 2, 1, 0, 1, 4, 3, 4, 6],
        '内容': ['3人より多い', '別居', '主婦', '先生', '授業コース', '15-30分', '2-5時間', 'あり', 'なし', '受けたい', '良い', '普通', '多い', '6日']
    })
    # DataFrameを表示
    st.markdown(df.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    form = st.form(key="ai1")

    with form:
        text1 = st.selectbox("生徒の成績はどちらだと思いますか？", [None, "平均より優れている", "平均よりも劣っている"], format_func=lambda x: "選択してください" if x is None else x)
        submitted = st.form_submit_button(label="回答を提出")

    if submitted:
        st.markdown("続いて、AIの予測を提示します。", unsafe_allow_html=True)
        st.markdown("", unsafe_allow_html=True)
        st.markdown("#### AIの予想：成績は平均より優れている", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("", unsafe_allow_html=True)
        

        form = st.form(key="q1")

        with form:
            text1 = st.selectbox("最終的に、生徒の成績はどちらだと思いますか？", [None, "平均より優れている", "平均よりも劣っている"], format_func=lambda x: "選択してください" if x is None else x)
            submitted_q = st.form_submit_button(label="回答を提出")

        if submitted_q:

            scopes = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']

            json_keyfile_dict = st.secrets["service_account"]

            credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                json_keyfile_dict, 
                scopes
            )

            # gspread用に認証
            gc = gspread.authorize(credentials)

            # スプレッドシートのIDを指定してワークブックを選択
            workbook = gc.open_by_key(st.session_state.file['id'])
            worksheet = workbook.sheet1

            st.session_state.end = time.time()

            elapsed_time = st.session_state.end - st.session_state.start

            # A1のセルに入力
            worksheet.update_acell('A1', text1)
            worksheet.update_acell('A2', str(elapsed_time))

            st.session_state.question_1_finished = True

            st.success("回答を提出しました！次の問題に進んでください。")