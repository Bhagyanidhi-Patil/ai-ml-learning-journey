import streamlit as st
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# extract article text
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,"html.parser")
        paragraphs = soup.find_all("p")
        text = "".join([p.get_text() for p in paragraphs])
        return text[:5000]   #limit text to 5000 letters
    except:
        return "Error extracting article"
    
#call llm (OpenRouter)
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
        return f"Error from API: {data}"

#streamlit UI
st.title("📰 News Summarizer + Explainer")
url = st.text_input("Enter new article URL")

if st.button("Analyze news"):
    if url:
        st.info("Fetching article")

        article_text = extract_text_from_url(url)
        if article_text == "Error extracting article":
            st.error("Could not fetch article")
        else:
            st.success("Article fetched!")
    #prompt
    summary_prompt = f"""
    Summarize this news in 5 bullet points:
    {article_text}
    """
    explain_prompt = f"""
    Explain this news in simple terms for a beginner:
    {article_text}
    """

    impact_prompt = f"""
    What are the key takeaways and why does this news matter?
    {article_text}
    """

    #call llm
    #st.spinner is used to show a loading message (spinner) while your code is running.
    with st.spinner("Generating summary..."):
        summary = ask_llm(summary_prompt)

    with st.spinner("Generating explanation..."):
        explanation = ask_llm(explain_prompt)

    with st.spinner("Analyzing impact..."):
        impact = ask_llm(impact_prompt)
    
    #output
    st.subheader("📰 Summary")
    st.write(summary)

    st.subheader("🧠 Explanation (Simple)")
    st.write(explanation)

    st.subheader("📊 Why It Matters")
    st.write(impact)

else:
    st.warning("Please enter a URL")


# To run the above code:
# 1. First install required library 
#      ->pip install streamlit requests beautifulsoup4 python-dotenv
# 2. then in terminal run below command
#     ->streamlit run app.py
#          [OR]
#     ->streamlit run app.py --server.port 8502
