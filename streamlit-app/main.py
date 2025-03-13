import streamlit as st

app1_page = st.Page("./pages/app1.py", title="app1")
app2_page = st.Page("./pages/app2.py", title="app2")

pg = st.navigation([app1_page, app2_page])
st.set_page_config(
    page_title="For Ds"
)
pg.run()


