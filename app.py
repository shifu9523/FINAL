import streamlit as st
from st_audiorec import st_audiorec
import speech_recognition as sr
import tempfile

PASSWORD = "hola"
MAX_ATTEMPTS = 3

# -------------------------
# SESSION STATE
# -------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# -------------------------
# AUDIO TO TEXT
# -------------------------

def speech_to_text(audio_bytes):

    recognizer = sr.Recognizer()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes)
        filename = tmp.name

    try:

        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language="es-ES"
        )

        return text.lower()

    except:
        return ""

# -------------------------
# LOGIN PAGE
# -------------------------

if not st.session_state.authenticated:

    st.title("🔐 Acceso por Voz")

    st.write("1. Presiona grabar")
    st.write("2. Di la contraseña")
    st.write("3. Detén la grabación")

    audio_data = st_audiorec()

    if audio_data is not None:

        spoken_text = speech_to_text(audio_data)

        st.write(f"Texto detectado: {spoken_text}")

        # PASSWORD CORRECTA
        if PASSWORD in spoken_text:

            st.success("✅ Acceso concedido")

            st.session_state.authenticated = True

            st.rerun()

        # PASSWORD INCORRECTA
        else:

            st.session_state.attempts += 1

            remaining = MAX_ATTEMPTS - st.session_state.attempts

            st.error("❌ Contraseña incorrecta")

            if remaining > 0:

                st.warning(
                    f"Intentos restantes: {remaining}"
                )

            # ALARMA
            if st.session_state.attempts >= MAX_ATTEMPTS:

                st.error("🚨 ALARMA ACTIVADA")

                st.audio("alarm.mp3")

# -------------------------
# SECRET PAGE
# -------------------------

else:

    st.title("🛡️ Página Secreta")

    st.success("Bienvenido")

    st.write("🔥 Reconocimiento de voz funcionando.")

    if st.button("Cerrar sesión"):

        st.session_state.authenticated = False
        st.session_state.attempts = 0

        st.rerun()
