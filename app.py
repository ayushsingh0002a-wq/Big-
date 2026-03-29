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


# UI
st.set_page_config(page_title="Big Small Predictor", layout="centered")

st.title("🎯 Big Small Predictor PRO")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Enter numbers (0-9 space separated)")

if st.button("Predict"):
    try:
        numbers = list(map(int, user_input.split()))
        st.session_state.history.extend(numbers)

        last_numbers = get_last_numbers(st.session_state.history)
        probs = analyze(last_numbers)
        result = predict(last_numbers)

        st.subheader("📊 Last 10 Analysis")
        st.write(f"BIG: {probs['BIG']:.2f}")
        st.write(f"SMALL: {probs['SMALL']:.2f}")

        st.subheader("🔮 Prediction")
        st.success(result)

        st.subheader("📜 History")
        st.write(st.session_state.history)

    except:
        st.error("Invalid input! Enter like: 1 5 3 8")

if st.button("Clear History"):
    st.session_state.history = []
    st.success("History cleared!")

