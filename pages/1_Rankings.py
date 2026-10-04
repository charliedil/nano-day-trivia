import streamlit as st
from sqlalchemy.sql import text
import random
from style import apply_style, show_leaderboard

st.set_page_config(page_title="Nano Day Trivia", page_icon="🔬")
apply_style()

st.session_state.pop("questions_sample", None)
st.write("Leaderboard")
# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.connection('rankings_db', type='sql', url="sqlite:///rankings.db")

with conn.session as s:
    s.execute(text('CREATE TABLE IF NOT EXISTS scores_ranked (username TEXT, score INT);'))
    s.commit()
# Query and display the data you inserted
rankings = conn.query('SELECT * FROM scores_ranked ORDER BY score DESC', ttl=0)
if st.session_state.pop("score", None) == 25:
    st.balloons()
if rankings.empty:
    st.info("No scores yet. Be the first to play!")
else:
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    # Equal scores get the same rank (e.g. 1, 1, 3, 4)
    ranks = rankings["score"].rank(method="min", ascending=False).astype(int)
    rankings.insert(0, "Rank", ranks.map(lambda r: medals.get(r, str(r))))

    df = rankings.rename(columns={"username": "Player", "score": "Score"})

    show_leaderboard(df)
fun_facts = [
    "A sheet of paper is about 100,000 nanometers thick.",
    "Your fingernails grow about 1 nanometer per second.",
    "Gold nanoparticles can look red instead of gold.",
]
st.caption(f"> FUN_FACT: {random.choice(fun_facts)}")
if st.button("Play again"):
    st.switch_page("Questions.py")
