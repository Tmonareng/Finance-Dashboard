import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Personal Finance Dashboard", layout="wide")
st.title("Personal Finance -- Quick Dashboard")

@st.cache_data
def load_csv(path="data/transactions.csv"):
    df = pd.read_csv(path, parse_dates=["date"])
    return df

try:
    df = load_csv()
except Exception as e:
    st.error(f"Could not load data: {e}")
    st.stop()

assets = df.loc[df['type']=="asset", 'amount'].sum()
liabilities = df.loc[df['type']=="liability", 'amount'].sum()
net_worth = assets - liabilities

col1, col2, col3 = st.columns(3)
col1.metric("Assets (ZAR)", f"R{assets:,.2f}")
col2.metric("Liabilities (ZAR)", f"R{liabilities:,.2f}")
col3.metric("Net worth (ZAR)", f"R{net_worth:,.2f}")

spend = (
    df.loc[df['type']=="expense"]
      .groupby('category', as_index=False)['amount']
      .sum()
      .sort_values('amount', ascending=False)
)
st.subheader("Spending by category (expenses)")
if not spend.empty:
    fig = px.bar(spend, x='category', y='amount', labels={'amount':'ZAR'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No expense data yet.")

st.subheader("Recent transactions")
st.dataframe(df.sort_values('date', ascending=False).reset_index(drop=True).head(200))