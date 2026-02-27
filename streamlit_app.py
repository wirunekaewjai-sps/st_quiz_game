# Import python packages
import json
import time
import uuid

import streamlit as st

# connect to snowflake database ()
conn = st.connection("snowflake")
session = conn.session()

st.title(body="QUIZ GAME", anchor=False, text_alignment="center")

# generate user id if not exists on current session
if "user_id" not in st.session_state:
    st.session_state.user_id = uuid.uuid4()

if "ended" not in st.session_state:
    st.session_state.ended = False

st.write(f"UUID: {st.session_state.user_id}")

# display tab UI
tab1, tab2 = st.tabs([
    "🔍 Play",
    "🏆 Leaderboard"
])

with tab1:
    if "step" not in st.session_state:
        if st.button("Start"):
            st.session_state.questions = session.sql("SELECT TITLE, CHOICES, ANSWER FROM QUIZ_GAME.PUBLIC.QUESTIONS ORDER BY RANDOM() LIMIT 5").to_pandas()
            st.session_state.start_time = time.time()
            st.session_state.step = 0
            st.session_state.score = 0
            st.rerun()

    elif st.session_state.ended:
        elapsed_time = st.session_state.elapsed

        if st.session_state.score < len(st.session_state.questions):
            st.write("Game Over!")
            st.write(f"Your score: {st.session_state.score} / {len(st.session_state.questions)}")
        else:
            st.write("Congratulations!")
            st.write(f"Your score: {st.session_state.score} / {len(st.session_state.questions)}")

        st.write(f"⏱️ Elapsed: {elapsed_time:.2f} seconds")

        if st.button("Play again"):
            st.session_state.questions = session.sql("SELECT TITLE, CHOICES, ANSWER FROM QUIZ_GAME.PUBLIC.QUESTIONS ORDER BY RANDOM() LIMIT 5").to_pandas()
            st.session_state.start_time = time.time()
            st.session_state.step = 0
            st.session_state.score = 0
            st.session_state.ended = False
            st.rerun()
    elif st.session_state.step >= len(st.session_state.questions):
        elapsed_time = time.time() - st.session_state.start_time

        session.sql(f"INSERT INTO QUIZ_GAME.PUBLIC.SCORES (USER_ID, SCORE, USAGE) VALUES ('{st.session_state.user_id}', '{st.session_state.score}', {elapsed_time})").collect()

        st.session_state.elapsed = elapsed_time
        st.session_state.ended = True
        st.rerun()

    else:
        # get row data
        question = st.session_state.questions.iloc[st.session_state.step]

        title = question[0]
        choices = json.loads(question[1])
        answer = question[2]

        st.header(title)

        for choice in choices:
            if st.button(f"{choice}: {choices[choice]}"):
                if choice == answer:
                    st.session_state.score += 1

                st.session_state.step += 1
                st.rerun()

with tab2:
    # st.write("this is leaderboard")
    df = session.sql("SELECT * FROM QUIZ_GAME.PUBLIC.LEADERBOARD LIMIT 10").collect()
    st.dataframe(df)
