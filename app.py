import streamlit as st
import random
import time
import base64
import numpy as np
import matplotlib.pyplot as plt

# --- Constants ---
BADGES = {
    5: "Cadet Clicker",
    15: "Rhythm Master",
    25: "Button Lord"
}

TRIVIA = [
    "The first button was patented in 1841.",
    "Streamlit is an open-source Python library for building data apps.",
    "Clicking activates parts of your brain tied to motor response.",
    "Your reaction time improves with regular practice.",
    "Games like this stimulate dopamine release.",
    "The world record for fastest reaction time is about 0.101 seconds.",
    "Monkeys can be trained to play simple computer games.",
    "Your brain can process images in as little as 13 milliseconds.",
    "Tapping games have been used in cognitive research.",
    "Reflex training is used in elite athlete conditioning.",
    "Human eyes can detect light from a single photon.",
    "The average human reaction time is 0.25 seconds.",
    "Reaction time slows with fatigue.",
    "Older adults can train to improve reflex speed.",
    "Games can enhance decision-making speed.",
    "Animals like cats have faster reflexes than humans.",
    "Sound reaches your ears faster than you consciously react.",
    "Tapping games can improve hand-eye coordination.",
    "People with ADHD may respond better to rhythmic feedback.",
    "The cerebellum helps with timing and motor control.",
    "Touchscreens use capacitive sensing to detect input.",
    "Light travels at 299,792,458 meters per second.",
    "Gamification can improve learning outcomes.",
    "Your dominant hand is usually faster in reflex games.",
    "Streamlit apps can be deployed with a single click.",
    "Boredom can reduce reaction performance.",
    "The human nervous system transmits signals at 120 m/s.",
    "Clicking engages the motor cortex.",
    "Color contrast can affect button visibility.",
    "Trivia enhances game retention in casual apps.",
    "Timing games are common in esports training.",
    "The Guinness World Record for most taps in 30 seconds is 402.",
    "Visual reaction time is generally slower than auditory.",
    "People blink faster under stress.",
    "Blue light from screens can suppress melatonin.",
    "Speed typing games use similar timing loops.",
    "Reaction-based games are older than video games.",
    "Ping pong is often used to train reflexes.",
    "People often underestimate time intervals by ~20%.",
    "Gamers may have better peripheral awareness.",
    "Red is perceived faster than blue.",
    "Multitasking increases error rate in timing games.",
    "The amygdala can influence reflex under fear.",
    "Microseconds matter in competitive gaming.",
    "The Stroop effect is a famous reaction time experiment.",
    "Some species of flies react 10x faster than humans.",
    "Reflex tests are common in driver licensing exams.",
    "The Spacebar is the most commonly used key in reaction games.",
    "Hand-eye coordination can improve with drumming."
]

# --- Utility Functions ---
def get_audio_tag():
    sound_url = "https://actions.google.com/sounds/v1/cartoon/pop.ogg"
    return f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/ogg">
        </audio>
    """

def get_hot_cold_feedback(current_diff, last_diff):
    if last_diff is None:
        return ""
    if current_diff < last_diff:
        return "You're getting hotter!"
    elif current_diff > last_diff:
        return "You're getting colder!"
    else:
        return "No change..."

def shimmer_text(text):
    return f"<div style='animation: shimmer 1.5s infinite linear;'>⭐ {text} ⭐</div>"

def reset_game():
    st.session_state.target_time = random.uniform(3, 7)
    st.session_state.last_click_diff = None
    st.session_state.tries = 0
    st.session_state.success = False
    st.session_state.start_time = 0
    st.session_state.timer_running = False
    st.session_state.clicked_this_round = False
    st.session_state.elapsed_time = 0
    st.session_state.total_elapsed_start = time.time()

# --- Session State Init ---
if 'target_time' not in st.session_state:
    reset_game()
    st.session_state.badges = []
    st.session_state.history = []
    st.session_state.best_time = None
    st.session_state.global_start_time = time.time()
    st.session_state.total_elapsed_start = time.time()

# --- Page Layout ---
st.set_page_config(page_title="Push The Button", layout="centered")
st.markdown("""
<style>
@keyframes shimmer {
  0% {opacity: 1;}
  50% {opacity: 0.3;}
  100% {opacity: 1;}
}
div.stButton > button:first-child {
    font-size: 24px;
    height: 80px;
    width: 80%;
    margin: auto;
    display: block;
    border: 2px solid #00ccff;
    animation: shimmer 1.5s infinite linear;
}
</style>
""", unsafe_allow_html=True)

st.title("🟢 Push the Button")

# --- Game Control ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Start Game"):
        reset_game()
        st.session_state.start_time = time.time()
        st.session_state.global_start_time = time.time()
        st.session_state.timer_running = True
        st.session_state.clicked_this_round = False
        st.session_state.total_elapsed_start = time.time()

with col2:
    if st.button("🛑 Stop Game"):
        st.session_state.timer_running = False
        st.session_state.clicked_this_round = True

# --- Timer Display ---
if st.session_state.timer_running and not st.session_state.clicked_this_round:
    st.session_state.elapsed_time = time.time() - st.session_state.start_time
else:
    st.session_state.elapsed_time = 0.0

# Live timer
st.markdown("""
<script>
    const updateTime = () => {
        const el = window.document.getElementById("live_timer")
        if (el) {
            const now = Date.now() / 1000;
            const start = Number(el.getAttribute("data-start"));
            const diff = (now - start).toFixed(2);
            el.innerText = `⏱️ ${diff} seconds this round`;
        }
    };
    setInterval(updateTime, 100);
</script>
""", unsafe_allow_html=True)

st.markdown(f"""
<h2 id="live_timer" data-start="{st.session_state.start_time}" style='text-align: center;'>⏱️ 0.00 seconds this round</h2>
""", unsafe_allow_html=True)

# Show total elapsed time
total_elapsed = time.time() - st.session_state.total_elapsed_start
st.markdown(f"<h4 style='text-align: center; color: gray;'>⏳ Total Time Elapsed: {total_elapsed:.2f} seconds</h4>", unsafe_allow_html=True)

# --- Audio Effect (Auto Play) ---
if st.session_state.clicked_this_round:
    st.markdown(get_audio_tag(), unsafe_allow_html=True)

# --- Game Logic ---
if st.button("🔘 Push the Button"):
    current_time = time.time()
    reaction_time = current_time - st.session_state.start_time
    diff = abs(st.session_state.target_time - reaction_time)
    feedback = get_hot_cold_feedback(diff, st.session_state.last_click_diff)
    st.session_state.last_click_diff = diff
    st.session_state.tries += 1
    st.session_state.clicked_this_round = True

    if diff < 1.0:
        st.success(f"🎯 Nailed it! You hit it at {reaction_time:.2f}s!")
        st.balloons()
        st.session_state.success = True

        if st.session_state.best_time is None or reaction_time < st.session_state.best_time:
            st.session_state.best_time = reaction_time
            st.info(f"🏆 New Personal Best: {reaction_time:.2f} seconds!")

        fact = random.choice([fact for fact in TRIVIA if fact not in st.session_state.history])
        st.session_state.history.append(fact)
        st.info(fact)

        if st.session_state.tries in BADGES and BADGES[st.session_state.tries] not in st.session_state.badges:
            st.session_state.badges.append(BADGES[st.session_state.tries])
            st.markdown(shimmer_text(f"🏅 You unlocked: {BADGES[st.session_state.tries]}!"), unsafe_allow_html=True)

        reset_game()
    else:
        st.warning(f"You clicked at {reaction_time:.2f}s. {feedback}")
        st.markdown("🔁 Try again and get closer to the target!")
        st.session_state.start_time = time.time()
        st.session_state.clicked_this_round = False

# --- Show Badges ---
if st.session_state.badges:
    st.subheader("🏆 Your Badges")
    for badge in st.session_state.badges:
        st.markdown(shimmer_text(badge), unsafe_allow_html=True)

# --- Trivia Archive ---
if st.session_state.history:
    with st.expander("💡 Trivia Unlocked"):
        for fact in st.session_state.history:
            st.markdown(f"- {fact}")

# --- Personal Best ---
if st.session_state.best_time:
    st.markdown(f"<h4 style='text-align: center;'>🥇 Personal Best: {st.session_state.best_time:.2f} seconds</h4>", unsafe_allow_html=True)

# --- AdSense Placeholder ---
st.markdown("""
<div style='margin: 20px auto; text-align: center;'>
  <ins class="adsbygoogle"
       style="display:block"
       data-ad-client="ca-pub-xxxxxxxxxxxxxxxx"
       data-ad-slot="1234567890"
       data-ad-format="auto"
       data-full-width-responsive="true"></ins>
  <script>
       (adsbygoogle = window.adsbygoogle || []).push({});
  </script>
</div>
""", unsafe_allow_html=True)
