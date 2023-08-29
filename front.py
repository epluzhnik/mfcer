import logging
import random
import time
from typing import List, Tuple, Any
import requests
import streamlit as st
from streamlit_searchbox import st_searchbox
from urllib3.util import url

logging.getLogger("streamlit_searchbox").setLevel(logging.DEBUG)

st.set_page_config(page_title="Поиск по документации", layout="wide", initial_sidebar_state="auto", page_icon="📖")

import requests

# URL для отправки POST-запроса
url_metrika = 'https://al-dente.serveo.net/metrika'

st.header = "Поиск по документации"






st.markdown("---")


def getMetrica() -> list[Tuple[Any, Any]]:
    response = requests.get(
        "https://al-dente.serveo.net/metrics",
        timeout=15
    ).json()

    print(response)
    return [
        (
            qa['question']
        )
        for qa in response
    ]




def search_docs_ids(question: str) -> List[Tuple[str, str]]:
    if not question:
        return []
    response = requests.post(
        "https://al-dente.serveo.net/answer",
        timeout=15,
        json={"question": question}
    ).json()
    print(response)
    candidates = response['candidates']
    # first element will be shown in search, second is returned from component
    return [
        (
            candidate["candidate"]['question'],
            candidate["candidate"]['answer']
        )
        for candidate in candidates

    ]


def search_empty_list(_: str):
    if not st.session_state.get("search_empty_list_n", None):
        st.session_state["search_empty_list_n"] = 1
        return ["a", "b", "c"]

    return []


#################################
#### application starts here ####
#################################



with st.container():
    selected_value = st_searchbox(
        search_function=search_docs_ids,
        placeholder="Поиск... ",
        label="Поиск по документам",
        default="Нет ответа",
        clear_on_submit=False,
        clearable=True,
        key="docs_search_main",
    )
    st.info(selected_value)
    # st.info(selected_value)

col1, col2, col3, col4, col5 = st.columns(5)
metrica = getMetrica()

for col, idx in zip([col1, col2, col3, col4, col5], range(5)):
    with col:
        if len(metrica) > idx:
            st.info(metrica[idx])


def main():
    st.title = "Поиск по документации"
    getMetrica()


if __name__ == '__main__':
    main()
