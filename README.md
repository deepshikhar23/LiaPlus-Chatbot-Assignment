# Customer Support Bot with Sentiment Analysis

### 📄 About This Project
This is an AI-powered Customer Support Chatbot built for the LiaPlus AI internship assignment. It simulates a support agent that can understand if a user is happy, frustrated, or neutral in real-time.

Try it here- https://huggingface.co/spaces/deepshikhar23/LiaPlus-Support-Bot

**The Goal:** To build a system that is fast enough for live chat but smart enough to generate detailed psychological reports for managers.

### ✨ Key Features
* **Real-Time Sentiment:** As you type, the bot instantly tags messages as **Positive (Green)**, **Negative (Red)**, or **Neutral (Grey)**.
* **Smart "Pain" Detection:** I customized the system to recognize specific complaints like "slow," "lag," or "complicated" as negative, which standard tools often miss.
* **Visual Journey Map:** When you end the chat, the bot creates a visual timeline showing how the user's mood changed from start to finish.
* **Live Graph:** A line chart on the sidebar updates instantly to track the emotional trend of the conversation.

### 🛠️ Technologies Used
* **Frontend:** Streamlit (Python)
* **AI Brain:** Google Gemini 1.5 Flash
* **Sentiment Engine:** NLTK VADER (Customized)
* **Charts:** Plotly

### ⚙️ How to Run It

1.  **Clone the code**
    ```bash
    git clone https://github.com/deepshikhar23/LiaPlus-Chatbot-Assignment
    cd LiaPlus-Chatbot-Assignment
    ```

2.  **Install the requirements**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your API Key**
    * Create a file named `.env` in the main folder.
    * Add your Google Gemini API key inside it like this:
        ```text
        GEMINI_API_KEY=your_actual_api_key_here
        ```
    * *Note: If you don't have a .env file, you can also paste the key directly into the sidebar when the app runs.*

4.  **Start the App**
    ```bash
    streamlit run app.py
    ```

### 🧠 Why I Built It This Way (Architecture)
I used a **Hybrid Approach** to balance speed and intelligence:

1.  **For Real-Time Chat (VADER):** I used a lightweight local tool (VADER) to analyze sentiment for every single message. This ensures there is **zero delay** for the user. Using a large LLM for every "hello" would be too slow and expensive.
2.  **For the Final Report (Gemini):** I used the large Language Model (Gemini) only at the end. This allows it to "read" the whole history and provide a deep, complex analysis without slowing down the chat.

### 📂 Project Structure
* `src/sentiment.py`: The logic that detects emotions (Happy/Sad/Angry).
* `src/chatbot.py`: Connects to Google Gemini to generate the final report.
* `src/analytics.py`: Draws the graph in the sidebar.
* `app.py`: The main file that runs the user interface.

---
*Submitted by Deepshikhar Saxena for LiaPlus AI.*
