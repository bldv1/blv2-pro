import streamlit as st
import yfinance as yf
import pandas as pd

PASSWORD = "MBEYA2026"

st.set_page_config(page_title="BLD V2 PRO", layout="wide")

if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 BLD V2 PRO - Ingiza Password")
    pwd = st.text_input("Password", type="password")
    if st.button("Fungua"):
        if pwd == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Password si sahihi!")
    st.stop()

st.title("📈 BLD V2 PRO - KANUNI 19")
st.success("Umefanikiwa kuingia Mzee Lusajo!")

pair = st.selectbox("Chagua Pair", ["EURUSD=X", "GBPUSD=X", "USDJPY=X", "XAUUSD=X"])
tf = st.selectbox("Timeframe", ["15m", "1h", "4h", "1d"])

if st.button("Pakua Soko"):
    with st.spinner("Inapakua data..."):
        df = yf.download(pair, period="10d", interval=tf, auto_adjust=False)

        # REKEBISHO LA KEYERROR
        if df.empty:
            st.error("Data haipatikani, jaribu pair nyingine")
            st.stop()

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.dropna()
        st.write(df.tail())

        for i in range(len(df)):
            try:
                o = df['Open'].iloc[i]
                c = df['Close'].iloc[i]
                h = df['High'].iloc[i]
                l = df['Low'].iloc[i]
                # hapa kanuni zako 19 zinaendelea...
            except Exception as e:
                st.warning(f"Skip: {e}")
                continue

        st.line_chart(df['Close'])
        st.balloons()
