import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# fetch news article
def fetch_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = []
    for item in response.get("articles",[]):
        articles.append({
            "title":item["title"],
            "url": item["url"]
        })
    return articles

# extract article text
def extract_text(url):
    try:
        res = requests.get(url,timeout=5)
        soup = BeautifulSoup(res.text,"html.parser")
        paragraphs = soup.find_all("p")
        text = "".join([p.get_text() for p in paragraphs])
        return text[:3000]
    except:
        return ""

# call llm
def ask_llm(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        } 
    )
    data = response.json()
    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {data}"

#streamlit UI
st.title("🧠 AI News Intelligence Platform")
query = st.text_input("🔍 Enter a topic (e.g., AI, India economy, Tesla)")
if st.button("Analyze News"):
    if not query:
        st.warning("Please enter a topic")
    else:
        st.info("Fetching news articles...")

        articles = fetch_news(query)

        all_text = ""
        st.subheader("📰 Sources")
        for art in articles:
            st.write(f"- {art['title']}")
            text = extract_text(art["url"])
            all_text += text + "\n\n"

        if all_text.strip() == "":
            st.error("Could not extract article content")
        else:
            # -------------------------------
            # PROMPTS
            # -------------------------------
            summary_prompt = f"""
            Summarize the following news articles into 5 key bullet points:
            {all_text}
            """

            explanation_prompt = f"""
            Explain this news in simple terms for a beginner:
            {all_text}
            """

            bias_prompt = f"""
            Do these articles show different perspectives or bias? Explain clearly.
            {all_text}
            """

            trends_prompt = f"""
            What are the overall trends or patterns in these news articles?
            {all_text}
            """

            # -------------------------------
            # CALL LLM
            # -------------------------------
            with st.spinner("Generating summary..."):
                summary = ask_llm(summary_prompt)

            with st.spinner("Generating explanation..."):
                explanation = ask_llm(explanation_prompt)

            with st.spinner("Analyzing bias..."):
                bias = ask_llm(bias_prompt)

            with st.spinner("Finding trends..."):
                trends = ask_llm(trends_prompt)

            # -------------------------------
            # OUTPUT
            # -------------------------------
            st.subheader("📰 Combined Summary")
            st.write(summary)

            st.subheader("🧠 Simple Explanation")
            st.write(explanation)

            st.subheader("⚖️ Bias / Perspective")
            st.write(bias)

            st.subheader("📊 Trends")
            st.write(trends)