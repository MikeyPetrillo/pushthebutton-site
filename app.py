import streamlit as st
import random
import time

# --- Constants ---
BADGES = {
    5: "Cadet Clicker",
    15: "Rhythm Master",
    25: "Button Lord",
    50: "Master of Timing",
    100: "The Button Legend"
}

TRIVIA = [
    "Bananas are berries, but strawberries aren't.",
    "Octopuses have three hearts.",
    "Honey never spoils.",
    "Sharks existed before trees.",
    "Butterflies can taste with their feet.",
    "The Eiffel Tower can grow taller in the summer.",
    "Some turtles can breathe through their butts.",
    "The inventor of the frisbee was turned into a frisbee after he died.",
    "Sloths can hold their breath longer than dolphins can.",
    "A day on Venus is longer than a year on Venus.",
    "Cows have best friends.",
    "Wombat poop is cube-shaped.",
    "The moon has moonquakes.",
    "Ketchup was sold as medicine in the 1830s.",
    "A group of flamingos is called a flamboyance.",
    "Jellyfish have survived 500 million years without brains.",
    "Penguins propose to their mates with a pebble.",
    "The longest hiccuping spree lasted 68 years.",
    "There are more trees on Earth than stars in the Milky Way.",
    "Bees can recognize human faces.",
    "A cloud can weigh over a million pounds.",
    "The unicorn is the national animal of Scotland.",
    "Snails can sleep for three years.",
    "Dolphins have names for each other.",
    "Koalas' fingerprints are almost indistinguishable from humans'.",
    "The heart of a blue whale is as big as a small car.",
    "Tomatoes and avocados are fruits.",
    "Lightning strikes about 8 million times per day worldwide.",
    "Birds are the closest living relatives to dinosaurs.",
    "A group of owls is called a parliament.",
    "Sea otters hold hands while they sleep.",
    "Camels have three eyelids.",
    "Sloths can hold their breath longer than dolphins.",
    "The world's largest snowflake was 15 inches wide.",
    "Antarctica is the driest place on Earth.",
    "Bananas glow blue under black lights.",
    "There’s a basketball court on the top floor of the U.S. Supreme Court building called the 'Highest Court in the Land.'",
    "Hot water freezes faster than cold water.",
    "A shrimp's heart is located in its head.",
    "A single sneeze travels 100 miles per hour.",
    "Some frogs can freeze solid and still live.",
    "Polar bears have black skin under their white fur.",
    "Sharks never stop moving.",
    "Lobsters taste with their legs.",
    "The dot over the lowercase 'i' and 'j' is called a tittle.",
    "The M's in M&Ms stand for Mars and Murrie.",
    "Apples float because 25% of their volume is air.",
    "Cows produce more milk when they listen to calming music.",
    "The longest English word is 189,819 letters long.",
    "A group of porcupines is called a prickle.",
    "Dolphins sleep with one eye open.",
    "Penguins can jump up to six feet in the air.",
    "Koalas sleep up to 22 hours a day.",
    "The electric chair was invented by a dentist.",
    "Elephants can't jump.",
    "Octopuses have blue blood.",
    "The national animal of Canada is the beaver.",
    "A panda's diet is 99% bamboo.",
    "Horses can't vomit.",
    "Jellyfish have no brains, hearts, or bones.",
    "The average person walks the equivalent of five times around the world in their lifetime.",
    "Sharks existed before dinosaurs.",
    "Cats can't taste sweetness.",
    "The tongue is the strongest muscle in the human body relative to its size.",
    "Dolphins can recognize themselves in a mirror.",
    "Some turtles breathe through their butts.",
    "Butterflies remember being caterpillars.",
    "Wolves change the course of rivers.",
    "The average lifespan of a mosquito is two weeks.",
    "Sloths are so slow that algae grow on their fur.",
    "A bolt of lightning contains enough energy to toast 100,000 slices of bread.",
    "Some cats are allergic to humans.",
    "The speed of a computer mouse is measured in 'Mickeys.'",
    "Bees sometimes sting other bees.",
    "The world's smallest reptile was discovered in 2021.",
    "A group of ravens is called an unkindness.",
    "The inventor of Pringles is buried in a Pringles can.",
    "The human nose can detect over 1 trillion scents.",
    "A group of crows is called a murder.",
    "Horses and cows can sleep standing up.",
    "The eye of an ostrich is bigger than its brain.",
    "Rabbits can't vomit.",
    "Frogs drink water through their skin.",
    "The fingerprints of a koala are virtually indistinguishable from humans'.",
    "The heart of a shrimp is located in its head.",
    "The unicorn is the national animal of Scotland.",
    "The only letter not appearing on the periodic table is J.",
    "The Guinness World Record for longest hiccups lasted 68 years."
]

# --- Init State ---
def reset_state():
    st.session_state.started = False
    st.session_state.target_time = random.uniform(3, 7)
    st.session_state.start_time = 0
    st.session_state.tries = 0
    st.session_state.last_diff = None
    st.session_state.best_time = None
    st.session_state.badges = []
    st.session_state.trivia_history = []
    st.session_state.streak = 0
    st.session_state.total_elapsed_start = time.time()
    st.session_state.play_count = 0
    st.session_state.play_limit = 10

if 'started' not in st.session_state:
    reset_state()

# --- Page Setup ---
st.set_page_config(page_title="The Button Game", layout="centered")
st.markdown("""
<style>
.title-shimmer {font-size: 36px; animation: shimmer 2s infinite linear;}
@keyframes shimmer { 0% {opacity: 1;} 50% {opacity: 0.3;} 100% {opacity: 1;} }
.badge {animation: shimmer 1.5s infinite linear;}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-shimmer'>🟢 Push the Button</div>", unsafe_allow_html=True)

# --- Scarcity Check ---
if st.session_state.play_count >= st.session_state.play_limit:
    st.error("⚠️ Daily play limit reached. Come back tomorrow!")
    st.stop()

# --- Start Game Button ---
if st.button("🚀 Start Game"):
    st.session_state.target_time = random.uniform(3, 7)
    st.session_state.start_time = time.time()
    st.session_state.started = True
    st.session_state.tries = 0
    st.session_state.last_diff = None

# --- Stopwatch ---
timer_placeholder = st.empty()

if st.session_state.started:
    start_time = st.session_state.start_time
    while st.session_state.started:
        elapsed_time = time.time() - start_time
        total_elapsed = time.time() - st.session_state.total_elapsed_start
        timer_placeholder.markdown(f"## ⏱️ Elapsed Time: {elapsed_time:.2f} seconds")
        st.markdown(f"Total Elapsed: {total_elapsed:.2f} seconds")
        time.sleep(0.1)
        st.experimental_rerun()

# --- Push the Button ---
if st.session_state.started and st.button("🔘 Push the Button"):
    st.session_state.play_count += 1
    reaction = time.time() - st.session_state.start_time
    diff = abs(st.session_state.target_time - reaction)

    st.audio("https://actions.google.com/sounds/v1/cartoon/pop.ogg")

    if diff <= 1:
        st.success(f"🎯 Nailed it at {reaction:.2f}s!")
        st.balloons()
        st.session_state.started = False
        st.session_state.streak += 1

        if st.session_state.best_time is None or reaction < st.session_state.best_time:
            st.session_state.best_time = reaction
            st.info(f"🏆 New Personal Best: {reaction:.2f}s!")

        fact = random.choice([fact for fact in TRIVIA if fact not in st.session_state.trivia_history])
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
        st.session_state.streak = 0

# --- Show Badges ---
if st.session_state.badges:
    st.subheader("🏆 Your Badges")
    for badge in st.session_state.badges:
        st.markdown(f"<div class='badge'>{badge}</div>", unsafe_allow_html=True)

# --- Show Trivia History ---
if st.session_state.trivia_history:
    st.subheader("💡 Trivia Unlocked")
    for fact in st.session_state.trivia_history:
        st.write(f"- {fact}")

# --- Show Best Time ---
if st.session_state.best_time:
    st.markdown(f"### 🥇 Personal Best: {st.session_state.best_time:.2f} seconds")

# --- Scarcity Mode Status ---
remaining_plays = st.session_state.play_limit - st.session_state.play_count
st.markdown(f"**Scarcity Mode:** {remaining_plays} plays left today.")

# --- Leaderboard Placeholder ---
st.markdown("**Leaderboard:** Coming soon! [Firebase/Supabase]")
