import streamlit as st

# Set page config
st.set_page_config(page_title="Push the Button!", page_icon="🚀", layout="centered")

# Title
st.title("🚨 Push The Button! 🚨")
st.write("Can you push the button more times than anyone else?")

# Initialize session state for score
if "score" not in st.session_state:
    st.session_state.score = 0

# Display current score
st.metric(label="Your Score", value=st.session_state.score)

# Button to increment score
if st.button("Push the Button! 🔘"):
    st.session_state.score += 1
    st.success(f"You pushed it! Total: {st.session_state.score}")

# Reset button
if st.button("Reset Game 🔄"):
    st.session_state.score = 0
    st.warning("Score reset. Start again!")

# Footer
st.caption("Built with ❤️ in Streamlit")

