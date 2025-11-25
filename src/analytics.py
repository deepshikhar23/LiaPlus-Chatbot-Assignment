import pandas as pd
import plotly.express as px

def create_sentiment_chart(history):
    # Extract user messages only
    data = []
    for i, msg in enumerate(history):
        if msg['role'] == "user":
            data.append({
                "Index": i,
                "Score": msg.get('sentiment_score', 0),
                "Label": msg.get('sentiment_label', 'Neutral'),
                "Snippet": msg['content'][:20] + "..."
            })

    if not data:
        return None

    df = pd.DataFrame(data)

    fig = px.line(
        df, 
        x="Index", 
        y="Score", 
        markers=True,
        title="Sentiment Trend",
        range_y=[-1.1, 1.1],
        hover_data=["Label", "Snippet"]
    )
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(template="plotly_dark", height=300)
    
    return fig