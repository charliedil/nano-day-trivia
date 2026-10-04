import streamlit as st
from sqlalchemy.sql import text
from trivia_bank import qa
import random
from style import apply_style, show_leaderboard

st.set_page_config(page_title="Nano Day Trivia", page_icon="🔬")
apply_style()

conn = st.connection('rankings_db', type='sql', url="sqlite:///rankings.db")

# Draw the questions once per session, not on every rerun
if "questions_sample" not in st.session_state:
    st.session_state.questions_sample = random.sample(qa, k=5)  # no duplicates

questions_sample = st.session_state.questions_sample
answers = []

with st.form("my_form"):
    username = st.text_area('Player name', height="content")
    st.write("Use the graph or your brain to answer the following!")
    for i in range(len(questions_sample)):
        answers.append(st.text_area(questions_sample[i][0], key=i))
    submit = st.form_submit_button('Submit')

if submit:
    score = 0
    for i in range(len(questions_sample)):
        if answers[i].strip().lower() in questions_sample[i][1]:
            score += 5
    with conn.session as s:
        s.execute(text('CREATE TABLE IF NOT EXISTS scores_ranked (username TEXT, score INT);'))
        s.execute(
            text('INSERT INTO scores_ranked (username, score) VALUES (:username, :score);'),
            params=dict(username=username, score=score)
        )
        s.commit()
    if "score" not in st.session_state:
        st.session_state.score = score

    st.switch_page("pages/1_Rankings.py")
