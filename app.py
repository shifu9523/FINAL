import streamlit as st
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import os

# -------------------------
# CONFIG
# -------------------------

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
# VOICE TO TEXT
# -------------------------

def speech_to_text(audio_bytes):

    recognizer = sr.Recognizer()

    temp_webm = "temp_audio.webm"
    temp_wav = "temp_audio.wav"

    # Guardar audio del navegador
    with open(temp_webm, "wb") as f:
        f.write(audio_bytes)

    # Convertir WEBM -> WAV
    os.system(
        f"ffmpeg -i {temp_webm} {temp_wav} -y > /dev/null 2>&1"
    )

    try:

        # Leer WAV
        with sr.AudioFile(temp_wav) as source:
            audio = recognizer.record(source)

        # Reconocimiento de voz
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

    st.write("Presiona grabar y di la contraseña.")

    audio = mic_recorder(
        start_prompt="🎙️ Grabar",
        stop_prompt="⏹️ Detener",
        key="recorder"
    )

    if audio:

        spoken_text = speech_to_text(audio["bytes"])

        st.write(f"Escuché: {spoken_text}")

        # PASSWORD CORRECTA
        if spoken_text == PASSWORD:

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

    st.write("Contenido oculto aquí.")

    st.write("🔥 Funcionó el reconocimiento de voz.")

    if st.button("Cerrar sesión"):

        st.session_state.authenticated = False
        st.session_state.attempts = 0

        st.rerun()
