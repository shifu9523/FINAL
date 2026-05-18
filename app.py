import streamlit as st
from st_audiorec import st_audiorec
import speech_recognition as sr
import tempfile
import base64

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

    st.title("🔐 SISTEMA DE ACCESO")

    st.write("🎙️ Di la contraseña correcta para entrar.")

    audio_data = st_audiorec()

    if audio_data is not None:

        spoken_text = speech_to_text(audio_data)

        st.write(f"🗣️ Texto detectado: {spoken_text}")

        # -------------------------
        # PASSWORD CORRECTA
        # -------------------------

        if PASSWORD in spoken_text:

            st.success("✅ ACCESO CONCEDIDO")

            st.session_state.authenticated = True

            st.rerun()

        # -------------------------
        # PASSWORD INCORRECTA
        # -------------------------

        else:

            st.session_state.attempts += 1

            remaining = MAX_ATTEMPTS - st.session_state.attempts

            st.error("❌ CONTRASEÑA INCORRECTA")

            if remaining > 0:

                st.warning(
                    f"⚠️ Intentos restantes: {remaining}"
                )

            # -------------------------
            # ALARMA EXTREMA
            # -------------------------

            if st.session_state.attempts >= MAX_ATTEMPTS:

                # PANTALLA ROJA + FLASH
                st.markdown(
                    """
                    <style>

                    .stApp {
                        background-color: #2b0000;
                        animation: flash 0.3s infinite;
                    }

                    @keyframes flash {
                        0% {background-color:#2b0000;}
                        50% {background-color:#ff0000;}
                        100% {background-color:#2b0000;}
                    }

                    .big-alert {
                        font-size: 70px;
                        color: white;
                        text-align: center;
                        font-weight: bold;
                        animation: blink 0.5s infinite;
                    }

                    @keyframes blink {
                        0% {opacity: 1;}
                        50% {opacity: 0;}
                        100% {opacity: 1;}
                    }

                    </style>
                    """,
                    unsafe_allow_html=True
                )

                # TEXTO GIGANTE
                st.markdown(
                    """
                    <div class="big-alert">
                    🚨 ACCESS DENIED 🚨
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.error("🚨 INTRUSO DETECTADO 🚨")

                st.warning("📡 Enviando alerta de seguridad...")


                # -------------------------
                # SONIDO AUTOMÁTICO
                # -------------------------

                with open("alarm.mp3", "rb") as f:
                    audio_bytes = f.read()

                audio_base64 = base64.b64encode(
                    audio_bytes
                ).decode()

                audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
                """

                st.markdown(
                    audio_html,
                    unsafe_allow_html=True
                )

# -------------------------
# SECRET PAGE
# -------------------------

else:

    st.title("🛡️ ZONA RESTRINGIDA")

    st.success("✅ IDENTIDAD VERIFICADA")

    st.write("🔥 Bienvenido al sistema secreto.")

    st.balloons()

    if st.button("Cerrar sesión"):

        st.session_state.authenticated = False
        st.session_state.attempts = 0

        st.rerun()
