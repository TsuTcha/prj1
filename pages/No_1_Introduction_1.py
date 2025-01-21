import streamlit as st

if st.session_state.user_random_id >= 0:

    st.markdown('# タスク1の概要説明')

    st.markdown('## 概要')

    st.markdown("""
                タスク1では、生徒のプロフィール情報をもとに、成績を当てるタスクを10問行っていただきます。<br>
                それぞれの問題ページに行ったら、スタートボタンをクリックしてください。<br>
                対象となる生徒のプロフィールが表示されます。<br>
                また、ヒントとして、AIが予想した成績も記載されています。<br>
                プロフィール情報とAIの予想を考慮して、この生徒の数学の成績を予想しましょう。<br>
                成績の予想ができたら、該当する成績のボタンを選んで、最後に提出ボタンを押してください。<br>
                """, unsafe_allow_html=True)

    st.markdown('## 例')



    st.markdown('## 注意事項など')

    st.markdown("""
                ※必ず提出ボタンを押してください。<br>
                準備ができましたら、左のサイドバーの No 2 Question1 から No.12 Question 10 を順にクリックして、<br>
                それぞれの問題を解いてください。
                """, unsafe_allow_html=True)
    
else:
    st.markdown("""
                #### メインメニューでユーザIDが正しく入力されていません。<br>
                左のサイドバー(表示されない場合は、左上の「>」ボタンを押してください)の一番上にあるページにアクセスして、
                ユーザIDを入力しなおしてください。
                """, unsafe_allow_html=True)