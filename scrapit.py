import streamlit as st
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd

# Function to scrape a website
def scrape_website(url):
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No title found"
            paragraphs = soup.find_all('p')
            content = "\n".join([p.get_text() for p in paragraphs[:5]])  # First 5 paragraphs
            return title, content
        else:
            return "Failed to retrieve", ""
    except Exception as e:
        return "Error", str(e)

# Streamlit UI
st.title("🔍 Google Search & Web Scraper")

# User input for search query
query = st.text_input("Enter your search keyword:", "malin kundang")
num_results = 10  # Fix to 10 results

# Button to start the search
if st.button("Search & Scrape"):
    st.write(f"🔍 Searching Google for: **{query}**...")
    
    # Get Google search results
    links = list(search(query, num_results=num_results))

    # Step 2: Allow user to **filter websites** based on keywords
    filter_keywords = ["news", "detik", "cnn", "kompas", "wikipedia", "tempo"]  # Example filters for news and Wikipedia
    filtered_links = [url for url in links if any(keyword in url for keyword in filter_keywords)]
    
    scraped_data = []
    
    # Scrape each website
    for url in filtered_links:
        title, content = scrape_website(url)
        scraped_data.append([url, title, content])

    # Convert to DataFrame and display
    df = pd.DataFrame(scraped_data, columns=["URL", "Title", "Content"])
    st.write("### 📑 Scraped Data:")
    st.dataframe(df)

    # Save to CSV
    csv_filename = "scraped_results.csv"
    csv_data = df.to_csv(index=False).encode("utf-8")

    # Download Button
    st.download_button(label="📥 Download CSV",
                       data=csv_data,
                       file_name=csv_filename,
                       mime="text/csv")
