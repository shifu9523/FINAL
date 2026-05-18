import streamlit as st
from streamlit_js_eval import streamlit_js_eval

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

if "spoken_text" not in st.session_state:
    st.session_state.spoken_text = ""

# -------------------------
# JAVASCRIPT SPEECH RECOGNITION
# -------------------------

speech_js = """
var recognition = new webkitSpeechRecognition();
recognition.lang = 'es-ES';
recognition.start();

recognition.onresult = function(event) {
    var text = event.results[0][0].transcript;
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: text
    }, '*');
};

recognition.onerror = function(event) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: 'ERROR'
    }, '*');
};
"""

# -------------------------
# LOGIN PAGE
# -------------------------

if not st.session_state.authenticated:

    st.title("🔐 Acceso por Voz")

    st.write("Presiona el botón y di la contraseña.")

    if st.button("🎙️ Hablar"):

        spoken_text = streamlit_js_eval(
            js_expressions=speech_js,
            key="speech"
        )

        if spoken_text:

            spoken_text = spoken_text.lower()

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
