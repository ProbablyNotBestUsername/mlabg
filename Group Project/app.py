import streamlit as st
import requests
import os

os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''

st.title('Предсказание жалоб')

tab1, tab2 = st.tabs(["Предсказание", "Руководство"])

with tab1:
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
            st.write(f"Название кластера: {clust[0]}")
            st.write(f"{clust[1]}")

    with tab2:
        tab2.subheader("Руководство пользователя")

        st.markdown(f"""
                    ### ⚠️ Для работы программы требуется запущенный API
                    """)
        
        st.markdown(f"""
                    ### Как использовать программу:\n
                    **1.** Введите текст в поле ввода.\n
                    **2.** Нажмите кнопку **"Предсказать".**\n
                    **3.** Программа выдаст номер кластера, к которому относится текст.\n
                    """)