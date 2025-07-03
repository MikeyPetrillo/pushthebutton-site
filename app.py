
import streamlit as st
import random
import time
import numpy as np
import matplotlib.pyplot as plt

# --- Constants and Session State ---
BADGES = {
    5: "Cadet Clicker",
    10: "Rhythm Rookie",
    15: "Rhythm Master",
    25: "Button Lord"
}

TRIVIA = [
    "The first button was patented in 1841.",
    "Streamlit is an open-source Python library for building data apps.",
    "Clicking activates parts of your brain tied to motor response.",
    "Your reaction time improves with regular practice.",
    "Games like this stimulate dopamine release.",
    "Reflex-based games are used in neuroscience studies.",
    "The world's fastest button press record is over 16 presses per second.",
    "Typing fast is a sign of high digital fluency.",
    "Tapping with your index finger is usually fastest.",
    "Mobile games represent over 50% of gaming revenue globally.",
    "The term 'button mashing' became popular in the early console era.",
    "Short bursts of reaction time training can improve cognitive sharpness.",
    "The first commercial video game console was the Magnavox Odyssey.",
    "A human blink lasts about 300 milliseconds.",
    "Clicking a mouse burns about 1.4 calories per 100 clicks.",
    "Buttons in video games often represent power or choice.",
    "Tapping games are a popular genre on mobile platforms.",
    "Reaction time varies by time of day and alertness.",
    "The Guinness World Record for fastest reflexes was measured via gaming.",
    "Streamlit apps run from Python scripts with minimal front-end code.",
    "Your average reaction time is around 250 milliseconds.",
    "The color red can slightly increase your reaction time.",
    "Competitive gaming is recognized as an official sport in many countries.",
    "Some animals have faster reaction times than humans.",
    "The brain processes visual information in under 100 milliseconds.",
    "Old arcade machines used mechanical buttons.",
    "Digital dexterity is a sought-after skill in tech jobs.",
    "Clicker games are often used to study reinforcement loops.",
    "Anticipation improves reaction time.",
    "Smartphone touchscreens delay input by a few milliseconds.",
    "Muscle memory plays a role in button-based games.",
    "Fidgeting can improve focus for some people.",
    "Fast-paced music may reduce your reaction speed.",
    "Reaction time declines with age.",
    "Practicing hand-eye coordination improves typing speed.",
    "Games are increasingly used in education.",
    "Esports revenue has surpassed $1 billion annually.",
    "Multiplayer games often require faster decisions than single-player ones.",
    "Video games were first developed in the 1950s.",
    "The word 'pixel' is short for 'picture element'.",
    "In gaming, HUD stands for Heads-Up Display.",
    "Speed training improves both motor and cognitive skills.",
    "The average PC gamer plays 6–8 hours a week.",
    "Leaderboard systems boost competition and replay value.",
    "Button layouts are tested rigorously for ergonomics.",
    "Repetitive tapping can cause fatigue over time.",
    "Haptic feedback mimics real-world touch sensations.",
    "Flash games popularized casual online gaming.",
    "Games like this improve sustained attention.",
    "Some trivia questions are designed to improve memory retention.",
    "Gamification is often used in workplace productivity tools.",
    "Reaction training is popular in sports psychology.",
    "The average mobile user taps their screen over 2,600 times per day.",
    "Speed-based games help with ADHD focus techniques.",
    "The word 'gamer' was added to the Oxford dictionary in 1999.",
    "Arcades peaked in popularity during the 1980s.",
    "Finger tapping speed is sometimes tested in neurology.",
    "Some watches use tapping games to test reflexes.",
    "Trivia improves long-term memory encoding.",
    "Gaming can lead to improvements in decision-making under pressure.",
    "AI models can now create games from text prompts.",
    "The brain uses predictive modeling to anticipate button press success.",
    "Some keyboards are optimized for speed clicking.",
    "Dark themes improve contrast for visual clarity.",
    "Hand-eye coordination improves with time-based games.",
    "You can train your non-dominant hand for faster responses.",
    "Gaming mice are tested for response latency.",
    "Online tournaments often measure input precision.",
    "The concept of 'combo chains' comes from arcade games.",
    "Gamers develop a sense of rhythm through repetition.",
    "Most humans can only tap a screen 6-8 times per second.",
    "Reflex games are used in pilot training.",
    "The phrase 'test your reflexes' is a common game trope.",
    "Some fitness games use step-tap mechanics.",
    "Multitasking in games improves task-switching speed.",
    "Voice assistants now support trivia modes.",
    "Augmented reality is being used in training simulations.",
    "Competitive button-pressing is a real esports niche.",
    "Tactile surfaces can boost response speed.",
    "Reaction time drills are common in boxing gyms.",
    "The oldest trivia contest dates back to 1924.",
    "The more you tap, the better you map — motor memory!",
    "Trick questions are often used to test attention.",
    "Some clicker games are used to study addiction loops.",
    "Video game reflexes can rival those of elite athletes.",
    "Speed-based games often appear in hackathons.",
    "Microinteractions improve digital experience engagement.",
    "Button color affects click rate in UX testing.",
    "Tap sounds offer satisfying reinforcement.",
    "Racing games sharpen short-term timing accuracy.",
    "Neurons transmit signals up to 120 meters/second.",
    "Typing rhythm is used in behavioral biometrics.",
    "Trivia helps develop semantic recall pathways.",
    "Tactile gaming controllers improve immersion.",
    "Faster response time correlates with better game scores.",
    "The 'tap-to-start' trend began with mobile app games."
]

if "target_time" not in st.session_state:
    st.session_state.target_time = random.uniform(3, 7)
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "unlocked_mode" not in st.session_state:
    st.session_state.unlocked_mode = False
if "available_plays" not in st.session_state:
    st.session_state.available_plays = 10
if "trivia_seen" not in st.session_state:
    st.session_state.trivia_seen = set()

# --- Helper Functions ---
def reset_game():
    st.session_state.target_time = random.uniform(3, 7)
    st.session_state.start_time = None
    st.session_state.clicked = False
    st.session_state.attempts = 0

def unlock_badge(streak):
    return BADGES.get(streak, None)

def play_sound():
    st.audio("https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg")

def get_trivia():
    unseen = list(set(TRIVIA) - st.session_state.trivia_seen)
    if unseen:
        t = random.choice(unseen)
        st.session_state.trivia_seen.add(t)
        return t
    return "You've seen all the trivia!"

def render_streak():
    st.markdown(f"""
        <div style='padding: 10px; background: linear-gradient(90deg, #00ff99, #00ccff); 
        border-radius: 10px; color: black; font-weight: bold; animation: shimmer 2s infinite; 
        background-size: 200% 100%; background-position: left center;'>
        🔥 Current Streak: {st.session_state.streak} 🔥
        </div>
        <style>
        @keyframes shimmer {{
            0% {{ background-position: -1000px 0; }}
            100% {{ background-position: 1000px 0; }}
        }}
        </style>
    """, unsafe_allow_html=True)

def render_cosmetic_mode():
    st.markdown(f"""
        <div style='margin: 10px; padding: 10px; border: 2px dashed gold; 
        border-radius: 15px; background: #fffbe6;'>
            🎨 Cosmetic Mode Enabled: Enhanced visuals and sparkles
        </div>
    """)

# --- Scarcity Mode Check ---
if st.session_state.available_plays <= 0:
    st.error("🚫 You've used all your plays for today. Come back tomorrow!")
    st.stop()

# --- Title and UI ---
st.title("🟢 PUSH THE BUTTON")
st.caption("Time it right. Beat your reflexes. Unlock rewards.")

render_streak()

if st.session_state.unlocked_mode:
    render_cosmetic_mode()

if st.button("Start Game"):
    st.session_state.start_time = time.time()
    st.session_state.clicked = False
    st.session_state.attempts = 0
    st.success("Wait... and click at the perfect moment!")

if st.session_state.start_time and not st.session_state.clicked:
    elapsed = time.time() - st.session_state.start_time
    if st.button("CLICK NOW"):
        actual_time = time.time() - st.session_state.start_time
        delta = abs(actual_time - st.session_state.target_time)
        play_sound()
        st.session_state.available_plays -= 1

        if delta <= 0.2:
            st.success(f"🔥 Perfect! You hit at {actual_time:.2f}s (target: {st.session_state.target_time:.2f}s)")
            st.session_state.streak += 1
            badge = unlock_badge(st.session_state.streak)
            if badge:
                st.balloons()
                st.success(f"🏅 You unlocked: {badge}")
            if st.session_state.streak >= 10:
                st.session_state.unlocked_mode = True
            reset_game()
        else:
            hint = "Too soon!" if actual_time < st.session_state.target_time else "Too late!"
            st.warning(f"{hint} Try again. You were off by {delta:.2f}s")
            st.session_state.streak = 0
            reset_game()

# --- Trivia ---
st.markdown("## 🧠 Fun Fact")
st.info(get_trivia())

# --- Google AdSense Placeholder ---
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
