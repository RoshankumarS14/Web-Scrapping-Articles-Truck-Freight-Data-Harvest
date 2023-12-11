import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Truck Articles",
    page_icon="🚚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

df = pd.read_csv("All headlines.csv").drop_duplicates("Headlines",keep="first")

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
