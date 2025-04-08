import streamlit as st
from financial_agent import multi_ai_agent
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import requests

# Set Streamlit page configuration FIRST
st.set_page_config(page_title="Financial AI Assistant", layout="wide")

# ---------------- UTILS ---------------- #

def get_ticker_symbol(company_name):
    """Fetch ticker symbol from Yahoo Finance search."""
    base_url = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": company_name, "quotes_count": 1, "news_count": 0}
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'quotes' in data and len(data['quotes']) > 0:
            return data['quotes'][0]['symbol']
    except requests.RequestException as e:
        print(f"Error fetching ticker symbol: {e}")
    return None

# ------------- STYLE (centered layout) ------------- #

st.markdown(
    """
    <style>
        .main {
            max-width: 900px;
            margin: auto;
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- APP ---------------- #

st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("💰 Financial AI Assistant")

user_query = st.text_input("Enter your question about a stock, market news, etc:")

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

if st.button("Ask"):
    response = multi_ai_agent.run(user_query)
    st.session_state.last_response = response.content
    st.markdown(response.content)

# ---------------- RESPONSE + CHART ---------------- #

if st.session_state.last_response:
    st.markdown("---")
    st.markdown("### 🤖 Assistant's Response")
    st.markdown(st.session_state.last_response)

    st.markdown("## 📉 Stock Price Chart")

    symbol = get_ticker_symbol(user_query)

    if symbol:
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1mo")
            info = stock.info

            if data is not None and not data.empty:
                # Plotting
                fig, ax = plt.subplots(figsize=(10, 4))
                ax.plot(data.index, data["Close"], label=f"{symbol} Closing Price", color="orange", linewidth=2)

                ax.set_title(f"{info.get('shortName', symbol)} ({symbol}) - Last 30 Days")
                ax.set_xlabel("Date")
                ax.set_ylabel("Price (USD)")
                ax.grid(True)
                ax.legend()

                # Formatting
                ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
                ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
                fig.autofmt_xdate(rotation=30)

                st.pyplot(fig)

                # Company Info
                st.markdown("### 🧾 Company Overview")
                st.write(f"**Name:** {info.get('shortName', 'N/A')}")
                st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
                st.write(f"**Current Price:** ${info.get('currentPrice', 'N/A')}")
            else:
                st.warning("Couldn't fetch stock price history. Please check the symbol.")
        except Exception as e:
            st.error(f"⚠️ Failed to retrieve stock data for '{symbol}'. Error: {e}")
    else:
        st.info("No valid stock ticker symbol could be identified from your query.")

st.markdown('</div>', unsafe_allow_html=True)
