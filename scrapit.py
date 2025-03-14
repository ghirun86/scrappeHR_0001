import streamlit as st
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd

# Function to scrape selected websites
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
st.title("🔎 Web Scraper & Google Search")

# User input for search query
query = st.text_input("Enter your search keyword:", "Andre Rosiade")

# Number of results
num_results = st.slider("Number of Google search results:", 5, 20, 10)

# Fetch results
if st.button("Search & Scrape"):
    st.write(f"🔍 Searching Google for: **{query}**...")
    
    # Get Google search results
    links = list(search(query, num_results=num_results))
    
    # Store selected links
    selected_links = []
    with st.form("select_links_form"):
        st.write("### ✅ Select Websites to Scrape:")
        for idx, url in enumerate(links):
            selected = st.checkbox(url, key=idx)
            if selected:
                selected_links.append(url)
        submitted = st.form_submit_button("Scrape Selected Websites")

    # Scrape selected websites
    if submitted and selected_links:
        scraped_data = []
        for url in selected_links:
            title, content = scrape_website(url)
            scraped_data.append([url, title, content])
        
        # Convert to DataFrame and display
        df = pd.DataFrame(scraped_data, columns=["URL", "Title", "Content"])
        st.write("### 📑 Scraped Data:")
        st.dataframe(df)

        # Save to CSV
        csv_filename = "scraped_results.csv"
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        st.success(f"✅ Data saved to **{csv_filename}**")
        st.download_button(label="📥 Download CSV", data=df.to_csv(index=False), file_name="scraped_results.csv", mime="text/csv")