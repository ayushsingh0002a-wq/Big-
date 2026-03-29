import streamlit as st
import random

def classify(num):
    return "SMALL" if num <= 4 else "BIG"

def analyze(numbers):
    big = sum(1 for n in numbers if classify(n) == "BIG")
    small = len(numbers) - big
    total = len(numbers)
    return {
        "BIG": big / total if total else 0,
        "SMALL": small / total if total else 0,
    }

def predict(probs):
    if probs["BIG"] > probs["SMALL"]:
        return "BIG"
    elif probs["SMALL"] > probs["BIG"]:
        return "SMALL"
    return random.choice(["BIG", "SMALL"])

st.title("🎯 Big Small Predictor")

user_input = st.text_input("Enter numbers (0-9 space separated)")

if st.button("Predict"):
    try:
        numbers = list(map(int, user_input.split()))
        probs = analyze(numbers)
        result = predict(probs)

        st.write(f"BIG: {probs['BIG']:.2f}")
        st.write(f"SMALL: {probs['SMALL']:.2f}")
        st.success(f"Prediction: {result}")
    except:
        st.error("Invalid input")
