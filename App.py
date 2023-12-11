import streamlit as st
import numpy as np
import pandas as pd
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Truck Articles",
    page_icon="🚚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

df = pd.read_csv("All headlines.csv").drop_duplicates("Headlines",keep="first")

# Function to read content from a PDF file
def read_pdf_content(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        content = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            content += page.extract_text()
        return content

st.title("Freight Focus: Exploring the World of Trucking 🚚")

search_words = st.text_input("",placeholder="Enter the keywords to search")
search = st.button("Search")

if search:
    st.title("Filtered Articles")
    for index in df.index:    

        url = df.loc[index,"URL"]
        text = df.loc[index,"Headlines"]

        if text.lower().count(search_words.lower()):
            html = f"""
            <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
                <span style="font-size: 24px; transition: text-decoration 0.3s ease-in-out;">
                    {text}
                </span>
            </a>
            <style>
                a:hover span {{
                    text-decoration: underline;
                    color: rgb(46, 154, 255); /* This will change the text color to blue on hover */
                }}
            </style>
            """

            # Display the text with the hover effect and redirection in Streamlit
            st.markdown(html, unsafe_allow_html=True)



if not search:
    st.title("All Articles")

    for index in df.index:    

        # st.subheader(df.loc[index,"Headlines"]+" [link](%s)" % df.loc[index,"URL"])

        url = df.loc[index,"URL"]
        text = df.loc[index,"Headlines"]
        html = f"""
        <a href="{url}" target="_blank" style="text-decoration: none; color: inherit;">
            <span style="font-size: 24px; transition: text-decoration 0.3s ease-in-out;">
                {text}
            </span>
        </a>
        <style>
            a:hover span {{
                text-decoration: underline;
                color: rgb(46, 154, 255); /* This will change the text color to blue on hover */
            }}
        </style>
        """

        # Display the text with the hover effect and redirection in Streamlit
        st.markdown(html, unsafe_allow_html=True)

# Your large string content
document_content = read_pdf_content("Content2.pdf")

# Split the document content into sentences
sentences = list(pd.Series(document_content.split('|')).drop_duplicates())

search_content = st.text_input("",placeholder="Type the words you are looking for in the articles")
search_words = st.button("Search",key="Button 2")

if search_words:

    # Input text for which you want to find similar sentences
    input_text = "Limit space for semi parking"

    # Combine the input text with the list of sentences for vectorization
    combined_text = [input_text] + sentences

    # Vectorize the text
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(combined_text)

    # Calculate similarity between the input text and all sentences
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Get the indices of the top 5 similar sentences
    top5_indices = np.argsort(-cosine_similarities)[:5]

    # Retrieve and print the top 5 similar sentences
    print("Top 5 similar content you are looking for:")
    
    for index in top5_indices:
        st.text(sentences[index])
    
    
