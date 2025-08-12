from htbuilder import HtmlElement, div, hr, a, p, styles
from htbuilder.units import percent, px
import streamlit as st

def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)

def layout(*args):
    style = """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      /* Remove .stApp { bottom: 105px; } completely */
    </style>
    """
    
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        background_color="#F1F1F1",
        color="black",
        text_align="center",
        padding=px(5, 5, 5, 5),
        height="auto",
        opacity=1,
        border_top="1px solid #ddd",
        font_size="14px",
        z_index=998  )
    
    body = p()
    foot = div(style=style_div)(
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)
        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)

def footer():
    myargs = [
        "Made with ❤️ by ",
        link("https://www.linkedin.com/in/pritiyax-shukla-0646982b3/", "Pritiyax Shukla",
             color="#2563EB", text_decoration="none", font_weight="bold"),
    ]
    layout(*myargs)
