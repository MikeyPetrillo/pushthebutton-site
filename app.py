import streamlit as st
import random
import time

# --- Constants ---
BADGES = {5: "Cadet Clicker", 15: "Rhythm Master", 25: "Button Lord", 50: "Master of Timing", 100: "The Button Legend"}

TRIVIA = [
    "Bananas are berries, but strawberries aren't.",
    "Octopuses have three hearts.",
    "Honey never spoils.",
    "Sharks existed before trees.",
    "Butterflies can taste with their feet.",
    "The Eiffel Tower can grow taller in the summer.",
    "Sloths can hold their breath longer than dolphins can.",
    "Some turtles can breathe through their butts.",
    "A day on Venus is longer than a year on Venus.",
    "Cows have best friends.",
    "Wombat poop is cube-shaped.",
    "The moon has moonquakes.",
    "Ketchup was sold as medicine in the 1830s.",
    "Jellyfish have survived 500 million years without brains.",
    "A group of flamingos is called a flamboyance.",
    "Butterflies can see ultraviolet light.",
    "Bees can recognize human faces.",
    "Polar bears have black skin under their fur.",
    "Bananas glow blue under black lights.",
    "A single sneeze travels 100 miles per hour.",
    "Snails can sleep for three years.",
    "Sloths move so slowly that algae grows on their fur.",
    "The unicorn is the national animal of Scotland.",
    "Dolphins have names for each other.",
    "Elephants can't jump.",
    "Cats can't taste sweetness.",
    "The fingerprints of a koala are virtually indistinguishable from a human's.",
    "A shrimp's heart is located in its head.",
    "Tomatoes and avocados are fruits.",
    "The world's largest snowflake was 15 inches wide.",
    "Lightning strikes the earth 8 million times per day.",
    "Birds are the closest living relatives to dinosaurs.",
    "Sea otters hold hands while sleeping to keep from drifting apart.",
    "Rabbits can't vomit.",
    "The M's in M&Ms stand for Mars and Murrie.",
    "Horses and cows can sleep standing up.",
    "A group of porcupines is called a prickle.",
    "The world's smallest reptile was discovered in 2021.",
    "A crocodile can't stick its tongue out.",
    "Mosquitoes are the deadliest animals on Earth.",
    "Penguins propose to their mates with a pebble.",
    "Sloths only defecate once a week.",
    "Some frogs can freeze solid and still live.",
    "There are more trees on Earth than stars in the Milky Way.",
    "A cloud can weigh over a million pounds.",
    "The inventor of Pringles is buried in a Pringles can.",
    "Apples float because 25% of their volume is air.",
    "The tongue is the strongest muscle relative to its size in the human body.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
    "Octopuses have blue blood.",
    "Dolphins sleep with one eye open.",
    "The heart of a blue whale is as big as a small car.",
    "Wolves change the course of rivers.",
    "Koalas sleep up to 22 hours a day.",
    "Some cats are allergic to humans.",
    "Jellyfish have no brains, hearts, or bones.",
    "The electric chair was invented by a dentist.",
    "The Eiffel Tower was originally intended for Barcelona.",
    "Bananas are naturally radioactive.",
    "Cows produce more milk when they listen to music.",
    "The average person walks the equivalent of five times around the world in their lifetime.",
    "Sharks never stop moving.",
    "Horses have the largest eyes of any land mammal.",
    "A group of owls is called a parliament.",
    "The wood frog can hold its pee for up to eight months.",
    "Sea cucumbers fight off predators by shooting out their own intestines.",
    "Flamingos are born gray, not pink.",
    "The dot over the lowercase 'i' and 'j' is called a tittle.",
    "The Guinness World Record for longest hiccups lasted 68 years.",
    "A panda's diet is 99% bamboo.",
    "The average lifespan of a mosquito is two weeks.",
    "Some fish cough.",
    "A group of crows is called a murder.",
    "The unicorn is the national animal of Scotland (yes, again, it's just that cool).",
    "A single strand of spaghetti is called a spaghetto.",
    "The fingerprints of a koala are indistinguishable from humans'.",
    "A group of ravens is called an unkindness.",
    "The blue whale is the largest animal to have ever lived on Earth.",
    "Octopuses have nine brains.",
    "Tigers have striped skin, not just striped fur.",
    "There are more fake flamingos in the world than real ones.",
    "The world's oldest piece of chewing gum is over 9,000 years old.",
    "Humans share about 60% of their DNA with bananas.",
    "The smell of freshly-cut grass is a plant distress call.",
    "You can't hum while holding your nose closed.",
    "A shrimp's heart is in its head.",
    "Rats laugh when tickled.",
    "Butterflies remember being caterpillars.",
    "There's a basketball court on the top floor of the U.S. Supreme Court called the "Highest Court in the Land."
]

# --- Init State ---
def reset_game():
    st.session_state.target_time = random.uniform(3, 7)
    st.session_state.start_time = None
    st.session_state.started = False
    st.session_state.elapsed_time = 0
    st.session_state.tries = 0
    st.session_state.last_diff = None
    st.session_state.streak = 0

if 'target_time' not in st.session_state:
    reset_game()
    st.session_state.best_time = None
    st.session_state.badges = []
    st.session_state.trivia_history = []
    st.session_state.play_count = 0
    st.session_state.play_limit = 10

# --- Page Setup ---
st.set_page_config(page_title="The Button Game", layout="centered")
st.markdown("""
<style>
.title { font-size: 36px; animation: shimmer 2s infinite linear; }
@keyframes shimmer { 0% {opacity: 1;} 50% {opacity: 0.3;} 100% {opacity: 1;} }
.badge { animation: shimmer 1.5s infinite linear; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🟢 Push the Button</div>", unsafe_allow_html=True)

# --- Scarcity Mode Check ---
if st.session_state.play_count >= st.session_state.play_limit:
    st.error("⚠️ Daily play limit reached. Come back tomorrow!")
    st.stop()

# --- Start Game ---
if st.button("🚀 Start Game"):
    reset_game()
    st.session_state.start_time = time.time()
    st.session_state.started = True
    st.audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg")

# --- Stopwatch ---
timer_placeholder = st.empty()
if st.session_state.started and st.session_state.start_time:
    elapsed = time.time() - st.session_state.start_time
    timer_placeholder.markdown(f"## ⏱️ Elapsed Time: {elapsed:.2f} seconds")
    st.session_state.elapsed_time = elapsed
else:
    timer_placeholder.markdown("## ⏱️ Timer not running")

# --- Push the Button ---
if st.session_state.started:
    if st.button("🔘 Push the Button"):
        st.session_state.play_count += 1
        reaction = time.time() - st.session_state.start_time
        diff = abs(st.session_state.target_time - reaction)
        st.audio("https://actions.google.com/sounds/v1/cartoon/pop.ogg")

        if diff <= 1:
            st.success(f"🎯 Nailed it at {reaction:.2f}s!")
            st.balloons()
            st.session_state.streak += 1
            st.session_state.started = False

            if st.session_state.best_time is None or reaction < st.session_state.best_time:
                st.session_state.best_time = reaction
                st.info(f"🏆 New Personal Best: {reaction:.2f}s!")

            fact = random.choice([f for f in TRIVIA if f not in st.session_state.trivia_history])
            st.session_state.trivia_history.append(fact)
            st.info(f"💡 Fun Fact: {fact}")

            if st.session_state.streak in BADGES and BADGES[st.session_state.streak] not in st.session_state.badges:
                badge = BADGES[st.session_state.streak]
                st.session_state.badges.append(badge)
                st.markdown(f"<div class='badge'>🏅 Badge Unlocked: {badge}</div>", unsafe_allow_html=True)

        else:
            feedback = "Hotter!" if st.session_state.last_diff is not None and diff < st.session_state.last_diff else "Colder!"
            st.warning(f"You clicked at {reaction:.2f}s. {feedback}")
            st.session_state.last_diff = diff
            st.session_state.tries += 1

# --- Show Stats ---
if st.session_state.badges:
    st.subheader("🏆 Your Badges")
    for badge in st.session_state.badges:
        st.markdown(f"<div class='badge'>{badge}</div>", unsafe_allow_html=True)

if st.session_state.trivia_history:
    st.subheader("💡 Trivia Unlocked")
    for fact in st.session_state.trivia_history:
        st.write(f"- {fact}")

if st.session_state.best_time:
    st.markdown(f"### 🥇 Personal Best: {st.session_state.best_time:.2f} seconds")

remaining_plays = st.session_state.play_limit - st.session_state.play_count
st.markdown(f"**Scarcity Mode:** {remaining_plays} plays left today.")

st.markdown("**Leaderboard:** Coming soon! [Firebase/Supabase]")
