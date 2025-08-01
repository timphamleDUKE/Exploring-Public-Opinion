import streamlit as st

tool_overview_page = st.Page("pages/Tool_Overview.py", title="Tool Overview")
affective_polarization_page = st.Page("pages/Affective_Polarization.py", title="Affective Polarization")
issue_positions_page = st.Page("pages/Issue_Position.py", title="Issue Positions")
rate_and_compare_page = st.Page("pages/Rate_and_Compare.py", title="How do you Compare?")
about_page = st.Page("pages/About.py", title="About")

pg = st.navigation([tool_overview_page, affective_polarization_page, issue_positions_page, rate_and_compare_page, about_page])
pg.run()