import streamlit as st
st.write("Enter userid aand password")
id = st.text_input("Name: ", placeholder="Type here..")
pswd = st.text_input("PSWD: ", placeholder="Type here..")
if st.button("submit"):
    st.success("id")
    st.success("pswd")
