import streamlit as st

# Matrix mode: the config theme does the heavy lifting, so this only adds the box
MATRIX_CSS = """
<style>
[data-testid="stForm"] {
    border: 1px solid #00FF41 !important;
    border-radius: 8px;
    box-shadow: 0 0 14px rgba(0, 255, 65, 0.25);
    background-color: #020B05;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #0B7A2B !important;
    border-radius: 8px;
}
</style>
"""

# Regular mode: overrides the config theme with a light look
REGULAR_CSS = """
<style>
.stApp { background-color: #FFFFFF; }
html, body, .stApp, p, label, li, td, th, input, textarea, button,
h1, h2, h3, [data-testid="stMarkdownContainer"], [data-testid="stCaptionContainer"] {
    font-family: "Source Sans Pro", sans-serif !important;
}
.stApp, .stApp p, .stApp label, .stApp li,
[data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"] p {
    color: #262730 !important;
}
h1, h2, h3 { color: #262730 !important; }
[data-testid="stHeader"] { background: transparent; }
/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child,
[data-testid="stSidebarContent"] {
    background-color: #F1F3F6 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] a {
    color: #262730 !important;
}
[data-testid="stSidebar"] {
    border-right: 1px solid #D0D5DD;
}

/* Collapse / expand arrows */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapsedControl"] button {
    color: #262730 !important;
}
/* Box */
[data-testid="stForm"] {
    border: 1px solid #D0D5DD !important;
    border-radius: 8px;
    background-color: #F1F3F6;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #D0D5DD !important;
    border-radius: 8px;
}

/* Inputs */
/* Inputs: cover every layer that can paint the box */
[data-testid="stTextInputRootElement"],
[data-testid="stTextAreaRootElement"],
div[data-baseweb="input"],
div[data-baseweb="base-input"],
div[data-baseweb="textarea"],
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {
    background-color: #FFFFFF !important;
    border-radius: 6px;
}
[data-testid="stTextInputRootElement"],
[data-testid="stTextAreaRootElement"] {
    border: 1px solid #B8BEC7 !important;
}
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    background-color: #FFFFFF !important;
    color: #262730 !important;
    -webkit-text-fill-color: #262730 !important;
    caret-color: #262730;
}
div[data-baseweb="input"] input::placeholder,
div[data-baseweb="textarea"] textarea::placeholder {
    color: #9AA0A6 !important;
    -webkit-text-fill-color: #9AA0A6 !important;
}
[data-testid="stTextInputRootElement"]:focus-within,
[data-testid="stTextAreaRootElement"]:focus-within {
    border-color: #FF4B4B !important;
}
/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    background-color: #FF4B4B; border: none;
}
.stButton button p, .stFormSubmitButton button p { color: #FFFFFF !important; }

/* Leaderboard table */
.regular-table { width: 100%; border-collapse: collapse; }
.regular-table th { border-bottom: 2px solid #D0D5DD; text-align: left; padding: 8px; color: #262730; }
.regular-table td { border-bottom: 1px solid #E6E8EB; padding: 8px; color: #262730; }
</style>
"""


def _sync_mode():
    st.session_state.matrix_mode = st.session_state._matrix_toggle


def apply_style():
    """Call right after st.set_page_config on every page."""
    if "matrix_mode" not in st.session_state:
        st.session_state.matrix_mode = True  # set False to default to regular

    _, right = st.columns([3, 1])
    with right:
        st.toggle(
            "Matrix mode",
            value=st.session_state.matrix_mode,
            key="_matrix_toggle",
            on_change=_sync_mode,
        )

    css = MATRIX_CSS if st.session_state.matrix_mode else REGULAR_CSS
    st.markdown(css, unsafe_allow_html=True)


def show_leaderboard(df):
    """df has Rank, Player, Score columns."""
    if st.session_state.get("matrix_mode", True):
        # st.dataframe reads the config theme, so it already looks right here
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Score": st.column_config.ProgressColumn(
                    "Score", min_value=0, max_value=25, format="%d"
                )
            },
        )
    else:
        # st.dataframe can't be recolored with CSS, so regular mode uses an HTML table
        # (to_html escapes player names, which keeps unsafe_allow_html safe)
        st.markdown(
            df.to_html(index=False, classes="regular-table", border=0),
            unsafe_allow_html=True,
        )
