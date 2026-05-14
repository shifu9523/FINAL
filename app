import streamlit as st
import speech_recognition as sr
import os
from playsound import playsound

# -----------------------------
# CONFIG
# -----------------------------
PASSWORD = "open sesame"
MAX_ATTEMPTS = 3

# -----------------------------
# SESSION STATE
# -----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# -----------------------------
# FUNCTION VOICE TO TEXT
# -----------------------------
def listen_password():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("🎤 Habla ahora...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        return text.lower()

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        st.error("Error conectando con el servicio de voz.")
        return ""


# -----------------------------
# LOGIN PAGE
# -----------------------------
if not st.session_state.authenticated:

    st.title("🔐 Acceso por Voz")

    st.write("Presiona el botón y di la contraseña.")

    if st.button("🎙️ Hablar"):

        spoken_text = listen_password()

        st.write(f"Escuché: **{spoken_text}**")

        if spoken_text == PASSWORD:

            st.session_state.authenticated = True
            st.success("✅ Contraseña correcta")
            st.rerun()

        else:

            st.session_state.attempts += 1

            remaining = MAX_ATTEMPTS - st.session_state.attempts

            st.error("❌ Contraseña incorrecta")

            if remaining > 0:
                st.warning(f"Te quedan {remaining} intentos")

            # ACTIVAR ALARMA
            if st.session_state.attempts >= MAX_ATTEMPTS:

                st.error("🚨 DEMASIADOS INTENTOS")

                playsound("alarm.mp3")

# -----------------------------
# PROTECTED PAGE
# -----------------------------
else:

    st.title("🛡️ Página Secreta")

    st.success("Bienvenido.")

    st.write("Contenido protegido aquí.")

    if st.button("Cerrar sesión"):
        st.session_state.authenticated = False
        st.session_state.attempts = 0
        st.rerun()
