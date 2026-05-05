import streamlit as st

def footer_home():

    st.markdown("""
        <div style="
            margin-top:2rem;
            display:flex;
            gap:6px;
            justify-content:center;
            align-items:center;
        ">
            <p style="
                font-weight:bold;
                color:white;
                margin:0;
            ">
                Created with ❤️ by Harshit Pundir
            </p>
        </div>
    """, unsafe_allow_html=True)