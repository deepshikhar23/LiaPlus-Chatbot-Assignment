import google.generativeai as genai
import os

class ChatbotManager:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API Key missing")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initial context setup
        sys_prompt = "You are a Customer Support AI for LiaPlus. Be helpful, concise, and professional."
        self.chat = self.model.start_chat(history=[
            {"role": "user", "parts": [sys_prompt]},
            {"role": "model", "parts": ["Understood."]}
        ])

    def get_response(self, msg):
        try:
            response = self.chat.send_message(msg)
            return response.text
        except Exception as e:
            return f"Error connecting to AI: {e}"

    def generate_final_summary(self, history):
        transcript = ""
        for h in history:
            role = h['role'].upper()
            txt = h['content']
            transcript += f"{role}: {txt}\n"
            
        prompt = (
            f"Analyze this transcript. Output TWO parts separated by '### REPORT_START ###'.\n\n"
            f"PART 1: VISUAL TIMELINE\n"
            f"Identify 3 to 5 key moments in the conversation order. Format EXACTLY like this:\n"
            f"Sentiment(Positive/Neutral/Negative) | Title | Brief Description\n"
            f"Example: Negative | Connection Issue | User reported lag.\n\n"
            f"PART 2: DETAILED REPORT\n"
            f"Write a professional Markdown managerial report (Overall Sentiment, Key Issues, Resolution, Trend).\n\n"
            f"TRANSCRIPT:\n{transcript}"
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "Failed to generate report."