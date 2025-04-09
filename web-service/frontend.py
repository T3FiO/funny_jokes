import streamlit as st
import requests
import time

st.title("Ухаха анекдоты")

# Text input field
user_input = st.text_area("Введите текст:", height=100)

# Submit button
if st.button("Submit"):
    if user_input:
        # Start timer
        start_time = time.time()

        # Make request to backend
        try:
            response = requests.post(
                "http://localhost:8000/process",
                json={"text": user_input}
            )
            if response.status_code == 200:
                result = response.json()
                # Calculate elapsed time
                elapsed_time = time.time() - start_time
                st.write(result["response"])
                st.markdown(f'<p style="color: gray; font-size: 14px;">Response time: {elapsed_time:.2f} seconds</p>',
                            unsafe_allow_html=True)
            else:
                st.error("Error processing the request")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend server. Make sure it's running.")
    else:
        st.warning("Please enter some text before submitting.")