import streamlit as st, pandas as pd, plotly.graph_objects as go, yfinance as yf
st.set_page_config(page_title="BLD V2 PRO - 10 RULES", layout="wide")
PASSWORD="MBEYA2026"
if "ok" not in st.session_state: st.session_state.ok=False
if not st.session_state.ok:
    st.title("⛔ BLD V2 PRO - LUSAJO PANDILLA")
    st.info("M-Pesa 0792166322 - 15k")
    if st.text_input("Password", type="password") == PASSWORD or st.button("Fungua"):
        if st.session_state.get("pw","")==PASSWORD or True:
            pass
    pw=st.text_input("Weka Password", type="password", key="pw")
    if st.button("🔓 Fungua"):
        if pw==PASSWORD: st.session_state.ok=True; st.rerun()
    st.stop()

st.title("🔥 BLD V2 PRO - KANUNI 10 + TRENDLINE PIVOT")
pair=st.sidebar.selectbox("Pair",["EURUSD=X","XAUUSD=X","BTC-USD"]); tf=st.sidebar.selectbox("TF",["1m","1h","4h"], index=1)
df=yf.download(pair, period="10d", interval=tf, progress=False).tail(200).copy(); df.reset_index(inplace=True, drop=True)
df['pivot']=""; df['rule']=""; df['action']="SUBIRI"
last_HH=df['High'].max(); last_LL=df['Low'].min()
for i in range(2,len(df)-2):
    o,c,h,l=df['Open'][i],df['Close'][i],df['High'][i],df['Low'][i]; body=abs(c-o); w_up=h-max(c,o); w_dn=min(c,o)-l
    is_bull=c>o; prev_bull=df['Close'][i-1]>df['Open'][i-1]; diff=is_bull!=prev_bull
    # 10 FAKE
    if (w_up>body*1.8 or w_dn>body*1.8) and body<(h-l)*0.4:
        df.loc[i,'rule']="10.FAKE SL HUNT"; df.loc[i,'action']="🟡 SUBIRI - FAKE"; df.loc[i,'pivot']="FAKE"; continue
    if is_bull and c>last_HH and diff: df.loc[i,'rule']="1.GREEN OUTSIDE HH"; df.loc[i,'action']="🟢 NUNUA MWANZO"; df.loc[i,'pivot']="HH"; last_HH=c
    elif is_bull and diff: df.loc[i,'rule']="4.GREEN INSIDE HL"; df.loc[i,'action']="🟢 NUNUA PULLBACK"; df.loc[i,'pivot']="HL"
    elif not is_bull and diff: df.loc[i,'rule']="7.RED INSIDE LH"; df.loc[i,'action']="🔴 UZA MWISHO"; df.loc[i,'pivot']="LH"
    elif diff: df.loc[i,'rule']="9.CONTINUE"; df.loc[i,'action']="➡️ CONTINUE"
fig=go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
hl=df[df['pivot']=="HL"].tail(2)
if len(hl)==2:
    x0,x1=hl.index[0],hl.index[1]; y0,y1=hl['Low'].iloc[0],hl['Low'].iloc[1]; x2=len(df)+20; slope=(y1-y0)/(x1-x0) if x1!=x0 else 0; y2=y1+slope*(x2-x1)
    fig.add_trace(go.Scatter(x=[x0,x1,x2], y=[y0,y1,y2], mode="lines", name="HL TRENDLINE", line=dict(color="lime", width=3)))
lh=df[df['pivot']=="LH"].tail(2)
if len(lh)==2:
    x0,x1=lh.index[0],lh.index[1]; y0,y1=lh['High'].iloc[0],lh['High'].iloc[1]; x2=len(df)+20; slope=(y1-y0)/(x1-x0) if x1!=x0 else 0; y2=y1+slope*(x2-x1)
    fig.add_trace(go.Scatter(x=[x0,x1,x2], y=[y0,y1,y2], mode="lines", name="LH TRENDLINE", line=dict(color="red", width=3)))
for i,row in df.tail(20).iterrows():
    if "NUNUA" in row['action'] or "UZA" in row['action'] or "SUBIRI" in row['action']:
        fig.add_annotation(x=i, y=row['High'], text=row['action'], showarrow=True)
st.plotly_chart(fig, use_container_width=True)
st.dataframe(df.tail(20))
