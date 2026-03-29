# file: app.py

import streamlit as st
import random


def classify(num):
    return "SMALL" if num <= 4 else "BIG"


def get_last_numbers(numbers, limit=10):
    return numbers[-limit:]


def analyze(numbers):
    big = sum(1 for n in numbers if classify(n) == "BIG")
    small = len(numbers) - big
    total = len(numbers)

    return {
        "BIG": big / total if total else 0,
        "SMALL": small / total if total else 0,
    }


def detect_streak(numbers):
    if not numbers:
        return None, 0

    last_type = classify(numbers[-1])
    streak = 1

    for i in range(len(numbers) - 2, -1, -1):
        if classify(numbers[i]) == last_type:
            streak += 1
        else:
            break

    return last_type, streak
def generate_result():
    num = random.randint(0, 9)
    size = classify(num)
    color = "Green" if size == "BIG" else "Red"
    return num, size, color

def predict(numbers):
    numbers = get_last_numbers(numbers)

    probs = analyze(numbers)
    last_type, streak = detect_streak(numbers)

    if streak >= 3:
        return "SMALL" if last_type == "BIG" else "BIG"

    if probs["BIG"] > probs["SMALL"]:
        return "BIG"
    elif probs["SMALL"] > probs["BIG"]:
        return "SMALL"

    return random.choice(["BIG", "SMALL"])


# ---------------- UI ----------------

st.set_page_config(page_title="Big Small Predictor PRO", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .card {
        padding: 15px;
        border-radius: 10px;
        background-color: #1c1f26;
        margin-bottom: 10px;
    }
    .big {
        color: #00ffcc;
        font-size: 24px;
        font-weight: bold;
    }
    .small {
        color: #ff4b4b;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 Big Small Predictor PRO")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Enter numbers (0-9 space separated)")

col1, col2 = st.columns(2)

if col1.button("Predict"):
    try:
        numbers = list(map(int, user_input.split()))
        st.session_state.history.extend(numbers)

        last_numbers = get_last_numbers(st.session_state.history)
        probs = analyze(last_numbers)
        result = predict(last_numbers)

        st.markdown("<div class='card'>📊 Analysis</div>", unsafe_allow_html=True)
        st.write(f"BIG: {probs['BIG']:.2f}")
        st.write(f"SMALL: {probs['SMALL']:.2f}")

        st.markdown("<div class='card'>🔮 Prediction</div>", unsafe_allow_html=True)

        if result == "BIG":
            st.markdown(f"<div class='big'>{result}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='small'>{result}</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>📜 History</div>", unsafe_allow_html=True)
        st.write(st.session_state.history)

    except:
        st.error("Invalid input! Use format: 1 5 3 8")

if col2.button("Clear"):
    st.session_state.history = []
    st.success("History cleared!")
st.markdown("---")
st.subheader("⚡ One Tap Result")

if st.button("🎲 Generate"):
    num, size, color = generate_result()

    st.markdown("### 🎯 Result")
    st.write(f"Number: {num}")

    if size == "BIG":
        st.markdown(f"<div class='big'>{size}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='small'>{size}</div>", unsafe_allow_html=True)

    st.write(f"Colour: {color}")
