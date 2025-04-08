import streamlit as st
from financial_agent import multi_ai_agent

st.set_page_config(page_title="Financial AI Assistant", page_icon="💰")
st.title("💰 Financial AI Assistant")

st.markdown("Enter your question about a stock, market news, etc:")

# Simple text input
user_query = st.text_input("")

# Store response in session state
if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Ask button
if st.button("Ask") and user_query.strip():
    with st.spinner("Thinking..."):
        response = multi_ai_agent.run(user_query)
        st.session_state.last_response = response.content
        st.markdown(response.content)

# Display previous response
if st.session_state.last_response:
    st.markdown("---")
    st.subheader("🧠 Agent's Last Response")
    st.markdown(st.session_state.last_response)
