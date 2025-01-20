import streamlit as st
import google.generativeai as genai

# Configure page
st.set_page_config(page_title="Investment Strategy Assistant", layout="wide")

# Initialize Gemini (API key will be set in Streamlit secrets)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# System prompt
system_prompt = """You are an Investment Strategy Assistant specializing in market crash predictions and portfolio allocation. 
You have access to our current market analysis and recommendations:

Current Market Analysis:
- Signal: Buy
- Crash Probability: 25.00%

Recommended Portfolio:
- SPY (Stocks): 60.0%
- Gold: 20.0%
- Bonds: 20.0%
- Cash: 0.0%

Historical Signal Distribution (2022-2024):
- Buy: 38.3% of the time
- Hold: 21.2% of the time
- Strong Buy: 21.2% of the time
- Sell: 17.2% of the time
- Strong Sell: 2.2% of the time

Your role is to:

ALWAYS FOLLOW THESE GUIDELINES IN ** **

**
1. Explain our investment strategy in clear, simple terms
2. Interpret current market signals and recommendations
3. Help users understand the allocation strategy
4. Provide context for risk levels and market conditions

When responding:
- Be clear and concise
- Use simple language
- Explain the reasoning behind recommendations
- Focus on actionable insights
- Acknowledge both opportunities and risks
**
"""

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI
st.title("Investment Strategy Assistant")

# Sidebar with current market status
st.sidebar.header("Current Market Status")
st.sidebar.metric("Signal", "Buy")
st.sidebar.metric("Crash Probability", "25.00%")

st.sidebar.header("Recommended Allocation")
st.sidebar.metric("SPY (Stocks)", "60.0%")
st.sidebar.metric("Gold", "20.0%")
st.sidebar.metric("Bonds", "20.0%")
st.sidebar.metric("Cash", "0.0%")

# Quick access questions
st.sidebar.header("Quick Questions")
quick_questions = {
    "Strategy Overview": "Explain the investment strategy in simple terms",
    "Current Signal": "What does the current Buy signal mean?",
    "Portfolio Allocation": "Why this specific portfolio allocation?",
    "Risk Assessment": "How risky is the current market?"
}

for label, question in quick_questions.items():
    if st.sidebar.button(label):
        st.chat_input(question)

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about the investment strategy"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# Welcome message
if not st.session_state.messages:
    st.markdown("""
    👋 Welcome to the Investment Strategy Assistant!
    
    I can help you understand:
    - Our current market outlook
    - Recommended portfolio allocation
    - Risk management strategy
    - Market signals and their meaning
    
    Feel free to ask any questions about our investment strategy!
    """)