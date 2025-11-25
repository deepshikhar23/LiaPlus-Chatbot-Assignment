import streamlit as st
import os
from dotenv import load_dotenv
from src.sentiment import SentimentEngine
from src.chatbot import ChatbotManager
from src.analytics import create_sentiment_chart

st.set_page_config(page_title="LiaPlus Assignment", page_icon="🤖", layout="wide")
load_dotenv()

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "bot" not in st.session_state:
    st.session_state.bot = None
if "analyzer" not in st.session_state:
    st.session_state.analyzer = SentimentEngine()

# Initialize Chatbot
if st.session_state.bot is None:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            st.session_state.bot = ChatbotManager(api_key)
        except Exception as e:
            st.error(f"Error initializing AI: {e}")
    else:
        st.error("API Key missing. Please check .env or repository secrets.")

# Sidebar
with st.sidebar:
    st.header("Live Analytics")
    if st.session_state.messages:
        fig = create_sentiment_chart(st.session_state.messages)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Analytics will appear here once conversation starts.")
            
    st.divider()
    
    if st.button("End Chat & Report", type="primary"):
        if st.session_state.bot and st.session_state.messages:
            with st.spinner("Generating Execution Summary..."):
                full_response = st.session_state.bot.generate_final_summary(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": full_response, "is_report": True})
                st.rerun()

# Main Interface
st.title("Customer Support Bot")

for msg in st.session_state.messages:
    if msg.get("is_report"):
        # --- NEW REPORT RENDERING LOGIC ---
        content = msg["content"]
        
        try:
            # Split the raw text into Timeline and Detail parts
            parts = content.split("### REPORT_START ###")
            timeline_raw = parts[0].strip()
            detailed_report = parts[1].strip() if len(parts) > 1 else "Report generation incomplete."

            st.markdown("## 📍 Conversation Journey")
            
            # Parse and render the timeline cards
            for line in timeline_raw.split('\n'):
                if "|" in line:
                    try:
                        sentiment, title, desc = [x.strip() for x in line.split('|')]
                        
                        # Choose color based on sentiment text
                        if "Negative" in sentiment:
                            st.error(f"**{title}**\n\n{desc}")
                        elif "Positive" in sentiment:
                            st.success(f"**{title}**\n\n{desc}")
                        else:
                            st.info(f"**{title}**\n\n{desc}")
                    except:
                        continue # Skip malformed lines
            
            st.divider()
            st.markdown("## 📋 Detailed Analysis")
            st.markdown(detailed_report)
            
        except Exception as e:
            # Fallback if splitting fails
            st.error("Could not parse visual timeline.")
            st.markdown(content)
            
    else:
        # Standard Chat Rendering
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if msg["role"] == "user" and "sentiment_label" in msg:
                color = msg['sentiment_color']
                lbl = msg['sentiment_label']
                score = msg['sentiment_score']
                st.markdown(
                    f"<div style='margin-top:5px;'><span style='background-color: {color}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px;'>{lbl} ({score:.2f})</span></div>", 
                    unsafe_allow_html=True
                )

if prompt := st.chat_input("How can I help you?"):
    if not st.session_state.bot:
        st.error("System not initialized.")
        st.stop()

    analysis = st.session_state.analyzer.analyze(prompt)
    
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "sentiment_score": analysis['score'],
        "sentiment_label": analysis['label'],
        "sentiment_color": analysis['color']
    })
    
    with st.chat_message("user"):
        st.write(prompt)
        st.markdown(
            f"<div style='margin-top:5px;'><span style='background-color: {analysis['color']}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px;'>{analysis['label']} ({analysis['score']:.2f})</span></div>", 
            unsafe_allow_html=True
        )

    with st.chat_message("assistant"):
        reply = st.session_state.bot.get_response(prompt)
        st.write(reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()