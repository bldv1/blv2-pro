import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# MAELEZO YAKO
JINA = "LUSAJO fredrick pandilla"
SIMU = "0792166322"
PASSWORD = "MBEYA2026"

st.set_page_config(page_title="BLD V2 PRO", layout="wide")

# LOGIN
if 'auth' not in st.session_state:
    st.session_state.auth = False
if not st.session_state.auth:
    st.title("BLD V2 PRO")
    st.write(f"{JINA} - {SIMU}")
    pwd = st.text_input("Weka Password", type="password")
    if st.button("Fungua"):
        if pwd == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Password si sahihi!")
    st.stop()

st.title("BLD V2 PRO - BANK SYSTEM")
st.caption(f"{JINA} | {SIMU}")
pair = st.selectbox("Chagua Pair", ["EURUSD=X","GBPUSD=X","XAUUSD=X","USDJPY=X","BTC-USD","AAPL"])
tf = st.selectbox("Timeframe", ["15m","1h","4h","1d"])

if st.button("CHAMBUA SOKO"):
    df = yf.download(pair, period="20d", interval=tf)
    if df.empty:
        st.error("Hakuna data")
        st.stop()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.dropna()

    # 1. PIVOT
    df['PH'] = df['High'][(df['High'].shift(1) < df['High']) & (df['High'].shift(-1) < df['High'])]
    df['PL'] = df['Low'][(df['Low'].shift(1) > df['Low']) & (df['Low'].shift(-1) > df['Low'])]
    highs = df.dropna(subset=['PH'])
    lows = df.dropna(subset=['PL'])

    # 2. SUPPORT / RESISTANCE
    support = df['Low'].rolling(20).min().iloc[-1]
    resistance = df['High'].rolling(20).max().iloc[-1]

    # 3. TRENDLINE ZINAZOGUSA PIVOT - SIO EMA
    # Support trendline
    if len(lows) >= 2:
        x = np.arange(len(lows))
        y = lows['PL'].values
        m_sup, b_sup = np.polyfit(x, y, 1)
        sup_trend_val = m_sup*(len(lows)-1)+b_sup
        df['SUP_LINE'] = np.nan
        # line yote
        full_x = np.arange(len(df))
        # tengeneza line kutoka mwanzo hadi mwisho kwa mteremko huo
        df['SUP_LINE'] = m_sup*full_x + b_sup - (m_sup*len(df) - m_sup*len(lows))
    else:
        sup_trend_val = support
        df['SUP_LINE'] = support

    # Resistance trendline
    if len(highs) >= 2:
        x = np.arange(len(highs))
        y = highs['PH'].values
        m_res, b_res = np.polyfit(x, y, 1)
        res_trend_val = m_res*(len(highs)-1)+b_res
        df['RES_LINE'] = m_res*np.arange(len(df)) + b_res - (m_res*len(df) - m_res*len(highs))
    else:
        res_trend_val = resistance
        df['RES_LINE'] = resistance

    last = df.iloc[-1]
    # 4. MWANZO / MWISHO TREND
    mwanzo_up = last['Close'] > df['Close'].rolling(50).mean().iloc[-1]
    mwisho_trend = last['Close'] < df['Close'].rolling(20).mean().iloc[-1] and mwanzo_up==False

    # 5. PULLBACK / REVERSAL
    pullback = last['Close'] < df['Close'].rolling(10).mean().iloc[-1] and mwanzo_up
    reversal = (last['Close'] < support*1.01) or (last['Close'] > resistance*0.99)

    # KANUNI 10 ZA BANK
    st.divider()
    st.subheader("KANUNI 10 ZA BANK")
    st.write(f"1. Liquidity Sweep: {'NDIO' if last['Low'] < support else 'Hapana'}")
    st.write(f"2. Market Structure: {'UPTREND' if mwanzo_up else 'DOWNTREND'}")
    st.write(f"3. Support: {support:.2f} | Resistance: {resistance:.2f}")
    st.write(f"4. Mwanzo wa Trend: {'✅ NDIO - Anza BUY' if mwanzo_up else 'Bado'}")
    st.write(f"5. Mwisho wa Trend: {'✅ NDIO - Toka' if mwisho_trend else 'Bado inaendelea'}")
    st.write(f"6. Pullback: {'✅ NDIO - Subiri bei irudi' if pullback else 'Hapana - Ingia'}")
    st.write(f"7. Reversal: {'✅ NDIO - Geuka' if reversal else 'Hapana'}")
    st.write(f"8. Pivot Highs: {len(highs)} | Pivot Lows: {len(lows)}")
    st.write(f"9. BUY kama bei inagusa SUP TRENDLINE: {'✅' if abs(last['Close']-sup_trend_val)<(last['Close']*0.002) else '❌'}")
    st.write(f"10. SELL kama bei inagusa RES TRENDLINE: {'✅' if abs(last['Close']-res_trend_val)<(last['Close']*0.002) else '❌'}")

    # METRICS
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("SUP TRENDLINE", f"{sup_trend_val:.2f}")
    c2.metric("RES TRENDLINE", f"{res_trend_val:.2f}")
    c3.metric("PRICE", f"{last['Close']:.2f}")
    c4.metric("PIVOT", f"{(last['High']+last['Low']+last['Close'])/3:.2f}")

    # CHATI - TRADELINE ZINAZOGUSA PIVOT
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(df['Close'].values[-100:], label="Price", color="black")
    ax.plot(df['SUP_LINE'].values[-100:], label="Support Trendline - Inagusa Pivot Lows", linestyle="--", color="green")
    ax.plot(df['RES_LINE'].values[-100:], label="Resistance Trendline - Inagusa Pivot Highs", linestyle="--", color="red")
    # weka dots za pivot
    ax.scatter(highs.index[-10:], highs['PH'].values[-10:], color="red")
    ax.scatter(lows.index[-10:], lows['PL'].values[-10:], color="green")
    ax.legend()
    st.pyplot(fig)

    # SIGNAL MWISHO
    if abs(last['Close']-sup_trend_val) < (last['Close']*0.003):
        st.success(f"🔵 SIGNAL: BUY - Bei imegusa Support Trendline ({sup_trend_val:.2f})")
    elif abs(last['Close']-res_trend_val) < (last['Close']*0.003):
        st.error(f"🔴 SIGNAL: SELL - Bei imegusa Resistance Trendline ({res_trend_val:.2f})")
    elif pullback:
        st.warning("🟡 PULLBACK INAENDELEA - Subiri")
    elif reversal:
        st.warning("🟡 REVERSAL - Geuka sasa")

    st.divider()
    st.write(f"**Mmiliki: {JINA} | {SIMU} | Password: {PASSWORD}**")
