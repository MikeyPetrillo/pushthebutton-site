import streamlit as st
import random
import time

# Setup
st.set_page_config(page_title="Push the Button!", page_icon="🚨")

st.title("🚨 Push The Button! 🚨")
st.write("Earn achievements, unlock boosts, and climb the leaderboard!")

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "click_power" not in st.session_state:
    st.session_state.click_power = 1
if "achievements" not in st.session_state:
    st.session_state.achievements = []
if "skin" not in st.session_state:
    st.session_state.skin = "🔘"
if "bonus_active" not in st.session_state:
    st.session_state.bonus_active = False
if "bonus_end_time" not in st.session_state:
    st.session_state.bonus_end_time = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# Achievement check
def check_achievements():
    score = st.session_state.score
    achievements = st.session_state.achievements

    if score >= 500 and "The Chosen One" not in achievements:
        st.session_state.click_power = 10
        achievements.append("The Chosen One")
        st.balloons()
        st.success("Achievement Unlocked: The Chosen One! Click power is now x10.")

    elif score >= 200 and "Click Commander" not in achievements:
        st.session_state.click_power = 5
        achievements.append("Click Commander")
        st.balloons()
        st.success("Achievement Unlocked: Click Commander! Click power is now x5.")

    elif score >= 50 and "Button Masher" not in achievements:
        st.session_state.click_power = 3
        achievements.append("Button Masher")
        st.balloons()
        st.success("Achievement Unlocked: Button Masher! Click power is now x3.")

    elif score >= 10 and "Beginner Pusher" not in achievements:
        st.session_state.click_power = 2
        achievements.append("Beginner Pusher")
        st.snow()
        st.success("Achievement Unlocked: Beginner Pusher! Click power is now x2.")

# Bonus round logic
def check_bonus():
    now = time.time()
    if st.session_state.bonus_active and now > st.session_state.bonus_end_time:
        st.session_state.bonus_active = False
        st.session_state.click_power //= 2
        st.warning("Bonus round ended! Click power normalized.")

def activate_bonus():
    st.session_state.bonus_active = True
    st.session_state.bonus_end_time = time.time() + 10
    st.session_state.click_power *= 2
    st.success("BONUS ROUND: Double click power for 10 seconds!")

# Open source click sound
sound_url = "https://cdn.pixabay.com/download/audio/2022/03/15/audio_52ba6b6f1c.mp3?filename=button-124476.mp3"

# Display stats
st.metric(label="Your Score", value=st.session_state.score)
st.write(f"Current click power: x{st.session_state.click_power}")
st.write(f"Achievements unlocked: {', '.join(st.session_state.achievements) or 'None yet'}")
st.write(f"Current streak: {st.session_state.streak} clicks in a row!")

# Leaderboard (in-memory)
st.write("### Leaderboard")
if st.session_state.leaderboard:
    sorted_leaderboard = sorted(st.session_state.leaderboard, key=lambda x: x[1], reverse=True)
    for i, (name, score) in enumerate(sorted_leaderboard, 1):
        st.write(f"{i}. {name}: {score}")
else:
    st.write("No scores yet. Be the first!")

# Skins
skin_choice = st.selectbox("Choose your button style", ["🔘", "🔥", "⭐", "💥"])
st.session_state.skin = skin_choice

# Enter player name
player_name = st.text_input("Enter your player name:", value="Player")

# Main button
if st.button(f"Push the Button! {st.session_state.skin}"):
    check_bonus()

    st.session_state.score += st.session_state.click_power
    st.session_state.streak += 1

    check_achievements()

    # Random bonus chance (5%)
    if random.random() < 0.05 and not st.session_state.bonus_active:
        activate_bonus()

    # Play sound effect from open-source URL
    st.audio(sound_url, format="audio/mp3")

# Save score to leaderboard
if st.button("Submit Score to Leaderboard 🏆"):
    st.session_state.leaderboard.append((player_name, st.session_state.score))
    st.success(f"{player_name} submitted a score of {st.session_state.score}!")

# Reset
if st.button("Reset Game 🔄"):
    st.session_state.score = 0
    st.session_state.click_power = 1
    st.session_state.achievements = []
    st.session_state.bonus_active = False
    st.session_state.streak = 0
    st.warning("Game reset. Start fresh!")

# Footer
st.caption("Built with ❤️ in Streamlit")
