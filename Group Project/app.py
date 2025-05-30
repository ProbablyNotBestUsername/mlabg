import streamlit as st
import requests
import os

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

st.title('Предсказание жалоб')
input_text = st.text_area("Введите текст жалобы", height=200)

if st.button('Предсказать'):
    if input_text == "":
        st.write("Введите текст")
    else:
        data = {
            "text": input_text
        }

        url = "http://127.0.0.1:8000/predict"
        response = requests.post(url, json=data)
        result = response.json()
        clust = result.get("cluster")

        st.markdown(f"""
                    #### Предсказаный кластер
                    """)
        st.write(f"Кластер: {clust[0]}")
        st.write(f"{clust[1]}")