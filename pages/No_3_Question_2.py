import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# セッション状態の初期化
if "start_button_clicked" not in st.session_state:
    st.session_state.start_button_clicked = False

# ボタンが押されたらセッション状態を更新
if st.button('問題1 スタート！'):
    st.session_state.select_count = 0
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

    st.write("")

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("まずは、生徒の成績を予想するためにあなたが重要だと思うプロフィール情報を3つ選びましょう。選んだ特徴に基づいたAIの意見を聞くことができます。", unsafe_allow_html=True)

    # 選択肢リスト
    options = ['家族の人数', '親の同居状況', '母親の仕事', '父親の仕事', 
               'この学校を選んだ理由', '家から学校までの通学時間', '毎週の勉強時間', '学校以外での教育サポート有無', 
               '課外活動(部活)の有無', 'レベルの高い授業を受けたいか', '家族関係', '放課後の自由時間', '友人と出かける頻度', '学校を休んだ回数']

    data = [
        ('友人と出かける頻度', '放課後の自由時間', '母親の仕事'),
        ('家族の人数', 'レベルの高い授業を受けたいか', '母親の仕事'),
        ('学校を休んだ回数', '学校以外での教育サポート有無', '母親の仕事'),
        ('レベルの高い授業を受けたいか', '母親の仕事', '学校以外での教育サポート有無'),
        ('母親の仕事', '学校以外での教育サポート有無', '学校を休んだ回数'),
        ('母親の仕事', 'レベルの高い授業を受けたいか', '学校以外での教育サポート有無'),
        ('母親の仕事', 'レベルの高い授業を受けたいか', '毎週の勉強時間'),
        ('レベルの高い授業を受けたいか', '友人と出かける頻度', '学校以外での教育サポート有無'),
        ('母親の仕事', '放課後の自由時間', 'レベルの高い授業を受けたいか'),
        ('友人と出かける頻度', '毎週の勉強時間', 'レベルの高い授業を受けたいか'),
        ('母親の仕事', '友人と出かける頻度', 'レベルの高い授業を受けたいか'),
        ('学校以外での教育サポート有無', '毎週の勉強時間', '母親の仕事'),
        ('母親の仕事', '学校を休んだ回数', '放課後の自由時間'),
        ('学校を休んだ回数', '母親の仕事', 'レベルの高い授業を受けたいか'),
        ('学校以外での教育サポート有無', '母親の仕事', '父親の仕事')
    ]

    y_pred = [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]

    # カラム名を指定してデータフレームを作成
    df = pd.DataFrame(data, columns=["f1","f2","f3"])

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



    # ユーザーに選択を促す
    selected_options = st.multiselect(
        "以下から3つ選んでください：",
        options,
    )

    # 各行とリストが一致しているかを判定
    def is_row_matching(row, target_list):
        return sorted(row.tolist()) == sorted(target_list)

    # 選択の数をチェック
    if len(selected_options) != 3:
        st.error("3つ選択してください。")
    else:
        st.success(f"選択された項目: {', '.join(selected_options)}")

    # ボタンが押されたらセッション状態を更新
    if st.button('AIの意見を聞く'):
        if len(selected_options) != 3:
            st.warning("特徴を3つ選択してください。")
        else:
            
            st.session_state.select_count += 1

            worksheet = workbook.sheet1
            # A1のセルに入力
            worksheet.update_acell('A'+str(st.session_state.select_count), ', '.join(selected_options))

            # 各行について判定を実施
            is_match_list = df.apply(lambda row: is_row_matching(row, selected_options), axis=1).tolist()
            pred = 0
            count = 0
            for m in is_match_list:
                if m == True:
                    pred += y_pred[m]
                    count += 1
            if count > 0:
                pred = pred / count
                if pred >= 0.5:
                    AI_result = "平均より優れている"
                else:
                    AI_result = "平均より劣っている"

                st.markdown("#### AIもその特徴を重視します。<br>AIの予測は「"+AI_result+"」です。", unsafe_allow_html=True)
            else:
                st.markdown("#### AIはその特徴を重視しません。", unsafe_allow_html=True)




    #form = st.form(key="feature1")

    #with form:
    #    f1 = st.selectbox("1番目に重要だと思う特徴はなんですか？", ["選択してください", '家族の人数', '親の同居状況', '母親の仕事', '父親の仕事', 
    #                                              'この学校を選んだ理由', '家から学校までの通学時間', '毎週の勉強時間', '学校以外での教育サポート有無', 
    #                                              '課外活動(部活)の有無', 'レベルの高い授業を受けたいか', '家族関係', '放課後の自由時間', '友人と出かける頻度', '学校を休んだ回数'])
    #    f2 = st.selectbox("2番目に重要だと思う特徴はなんですか？", ["選択してください", '家族の人数', '親の同居状況', '母親の仕事', '父親の仕事', 
    #                                              'この学校を選んだ理由', '家から学校までの通学時間', '毎週の勉強時間', '学校以外での教育サポート有無', 
    #                                              '課外活動(部活)の有無', 'レベルの高い授業を受けたいか', '家族関係', '放課後の自由時間', '友人と出かける頻度', '学校を休んだ回数'])
    #    f3 = st.selectbox("3番目に重要だと思う特徴はなんですか？", ["選択してください", '家族の人数', '親の同居状況', '母親の仕事', '父親の仕事', 
    #                                              'この学校を選んだ理由', '家から学校までの通学時間', '毎週の勉強時間', '学校以外での教育サポート有無', 
    #                                              '課外活動(部活)の有無', 'レベルの高い授業を受けたいか', '家族関係', '放課後の自由時間', '友人と出かける頻度', '学校を休んだ回数'])

    #    submitted_f = st.form_submit_button(label="AIの意見を聞く")

    #if submitted_f:
    #    if f1 == "選択してください" or f2 == "選択してください" or f3 == "選択してください":
    #        st.warning("3つ選択してください。")
    #    elif f1 == "友人と出かける頻度" or f2 == "放課後の自由時間" or f3 == "母親の仕事":
    #        st.markdown("#### AIもその特徴を重視します。", unsafe_allow_html=True)


    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("・別の特徴を選択することで、また違う特徴に基づくAIの意見を聞くことができます。", unsafe_allow_html=True)

    st.markdown("・AIとのやり取りを繰り返して、自分の予想が固まったら回答を選んで提出しましょう！", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("", unsafe_allow_html=True)

    form = st.form(key="q1")

    with form:
        text1 = st.selectbox("生徒の成績はどちらだと思いますか？", [None, "平均より優れている", "平均よりも劣っている"], format_func=lambda x: "選択してください" if x is None else x)
        submitted = st.form_submit_button(label="回答を提出")

    if submitted:
        st.session_state.question_1_finished = True