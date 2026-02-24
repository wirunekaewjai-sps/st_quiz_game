# Import python packages
import time
import uuid

import streamlit as st

st.title(body="QUIZ GAME", anchor=False, text_alignment="center")

if "user_id" not in st.session_state:
    st.session_state.user_id = uuid.uuid4()

st.write(f"UUID: {st.session_state.user_id}")

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

tab1, tab2 = st.tabs([
    "🔍 Play",
    "🏆 Leaderboard"
])

with tab1:
    if st.button("Reset"):
        st.session_state.start_time = time.time()
        st.rerun()

    if st.button("Elapsed"):
        elapsed_time = time.time() - st.session_state.start_time
        st.write(f"⏱️ Elapsed: {elapsed_time:.2f} seconds")

with tab2:
    st.write("this is leaderboard")
