import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

st.set_page_config(page_title="ECG Virtual Lab", layout="centered")

st.title("❤️ ECG Virtual Lab")

menu = st.sidebar.selectbox(
    "Select Section",
    ["Aim", "Theory", "Experiment", "Result", "Quiz", "Feedback"]
)

# -------------------------------
# 🎯 AIM
# -------------------------------
if menu == "Aim":
    st.header("🎯 Aim")
    st.write("""
    To simulate an ECG signal based on user-defined physiological parameters 
    and analyze heart rate and abnormalities using signal processing techniques.
    """)

# -------------------------------
# 📚 THEORY
# -------------------------------
elif menu == "Theory":
    st.header("📚 Theory")

    st.write("""
    An Electrocardiogram (ECG) records the electrical activity of the heart.

    • P wave → Atrial contraction  
    • QRS complex → Ventricular contraction  
    • T wave → Relaxation  

    The R-peak is the highest point in ECG and is used to calculate heart rate.

    Biomedical engineers use ECG signal processing to detect conditions such as:
    - Bradycardia (low heart rate)
    - Tachycardia (high heart rate)
    - Arrhythmia (irregular rhythm)
    """)

# -------------------------------
# 🧪 EXPERIMENT
# -------------------------------
elif menu == "Experiment":
    st.header("🧪 ECG Simulation Experiment")

    st.write("Adjust parameters and generate ECG signal")

    # USER INPUTS
    bpm_input = st.slider("Heart Rate (BPM)", 40, 150, 75)
    noise_level = st.slider("Noise Level", 0.0, 1.0, 0.2)
    amplitude = st.slider("Signal Strength", 0.5, 2.0, 1.0)

    if st.button("Generate ECG Signal"):

        # Time settings
        duration = 5
        fs = 200
        t = np.linspace(0, duration, duration * fs)

        # Convert BPM → frequency
        freq = bpm_input / 60

        # ECG-like signal
        ecg = amplitude * (
            np.sin(2 * np.pi * freq * t) +
            0.5 * np.sin(2 * np.pi * 3 * freq * t)
        )

        # Add noise
        ecg += np.random.normal(0, noise_level, len(t))

        # Store in session
        st.session_state.ecg = ecg
        st.session_state.t = t
        st.session_state.freq = freq
        st.session_state.bpm_input = bpm_input
        st.session_state.noise = noise_level

        st.success("✅ Signal Generated! Go to Result section")

# -------------------------------
# 📊 RESULT
# -------------------------------
elif menu == "Result":
    st.header("📊 Analysis Result")

    if "ecg" in st.session_state:

        ecg = st.session_state.ecg
        t = st.session_state.t
        bpm_input = st.session_state.bpm_input
        noise = st.session_state.noise

        # Plot ECG
        fig, ax = plt.subplots()
        ax.plot(t, ecg)
        ax.set_title("ECG Signal")
        st.pyplot(fig)

        # Peak detection
        peaks, _ = find_peaks(ecg, height=0.5)

        fig2, ax2 = plt.subplots()
        ax2.plot(t, ecg)
        ax2.plot(t[peaks], ecg[peaks], "rx")
        ax2.set_title("R-Peak Detection")
        st.pyplot(fig2)

        # Calculate BPM
        duration_sec = t[-1] - t[0]
        calc_bpm = (len(peaks) / duration_sec) * 60

        st.success(f"❤️ Calculated Heart Rate: {int(calc_bpm)} BPM")

        # CONDITIONS
        if bpm_input < 60:
            st.warning("⚠️ Bradycardia Detected")
        elif bpm_input > 100:
            st.warning("⚠️ Tachycardia Detected")
        else:
            st.success("✅ Normal Heart Rate")

        # Arrhythmia (noise-based)
        if noise > 0.6:
            st.error("🚨 Possible Arrhythmia (Irregular Signal)")

        # Risk score
        risk = abs(75 - bpm_input) + (noise * 50)
        risk = min(int(risk), 100)

        st.subheader("📊 Risk Level")
        st.progress(risk)
        st.write(f"Risk Score: {risk}/100")

    else:
        st.warning("⚠️ Please generate ECG signal first in Experiment section.")

# -------------------------------
# 📝 QUIZ
# -------------------------------
elif menu == "Quiz":
    st.header("📝 ECG Quiz")

    score = 0

    q1 = st.radio("1. ECG measures:", ["Blood pressure", "Heart electrical activity", "Oxygen"])
    if q1 == "Heart electrical activity":
        score += 1

    q2 = st.radio("2. Highest peak is:", ["P wave", "R peak", "T wave"])
    if q2 == "R peak":
        score += 1

    q3 = st.radio("3. QRS represents:", ["Atrial contraction", "Ventricular contraction", "Rest"])
    if q3 == "Ventricular contraction":
        score += 1

    if st.button("Submit Quiz"):
        st.success(f"Score: {score}/3")

# -------------------------------
# 💬 FEEDBACK
# -------------------------------
elif menu == "Feedback":
    st.header("💬 Feedback")

    name = st.text_input("Name")
    feedback = st.text_area("Your feedback")
    rating = st.slider("Rating", 1, 5)

    if st.button("Submit"):
        st.success(f"Thank you {name}! 😊")
        st.write("⭐ Rating:", rating)
        st.write("📝 Feedback:", feedback)
