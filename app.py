import streamlit as st
import yfinance as yf
import pandas as pd

PASSWORD = "MBEYA2026"
st.set_page_config(page_title="BLD V2 PRO", layout="wide")

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("BLD V2 PRO")
    pwd = st.text_input("Password", type="password")
    if st.button("Fungua"):
        if pwd == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Sahihi!")
    st.stop()

st.title("BLD V2 PRO - KANUNI 19")
pair = st.selectbox("Pair", ["EURUSD=X"])
tf = st.selectbox("Time", ["1h"])
if st.button("Pakua Soko"):
    df = yf.download(pair, period="10d", interval=tf)
    if df.empty:
        st.error("Hakuna data")
        st.stop()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.dropna()
    st.write(df.tail())
    st.line_chart(df['Close'])
    st.balloons()
