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
                    🚨 ACCESO DENEGADO 🚨
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

 # =========================
    # LIBRERÍAS
    # =========================

    import base64
    import numpy as np
    from PIL import Image
    from openai import OpenAI
    from streamlit_drawable_canvas import st_canvas
    import random

    # =========================
    # SESSION STATE
    # =========================

    if "historia" not in st.session_state:
        st.session_state.historia = ""

    if "descripcion_personaje" not in st.session_state:
        st.session_state.descripcion_personaje = ""

    # =========================
    # ESTILOS
    # =========================

    st.markdown("""
    <style>

    .main {
        background: linear-gradient(to bottom, #fff7d6, #ffe8f3);
    }

    h1 {
        text-align: center;
        color: #ff4b91;
        font-size: 3.2rem;
    }

    h2, h3 {
        color: #6a4c93;
    }

    .stButton>button {
        background-color: #ff4b91;
        color: white;
        border-radius: 15px;
        border: none;
        padding: 12px 22px;
        font-size: 18px;
        transition: 0.3s;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #ff85b3;
        transform: scale(1.05);
    }

    .story-box {
        background-color: white;
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
        font-size: 18px;
        color: #2d2d2d;
    }

    .tip-box {
        background-color: #fff0f7;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 20px;
        color: #6a4c93;
        font-weight: bold;
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        color: gray;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # FUNCIÓN BASE64
    # =========================

    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(
                image_file.read()
            ).decode("utf-8")

    # =========================
    # TÍTULO
    # =========================

    st.title("📖✨ Fábulas Mágicas para Niños")

    st.subheader(
        "Dibuja un personaje y crea una historia increíble 🌈"
    )

    # =========================
    # SIDEBAR
    # =========================

    with st.sidebar:

        st.header("🪄 Personaliza la historia")

        moraleja = st.selectbox(
            "💡 Elige una moraleja",
            [
                "La amistad es importante",
                "Nunca rendirse",
                "Ser amable con los demás",
                "Decir siempre la verdad",
                "Trabajar en equipo",
                "Compartir con otros"
            ]
        )

        lugar = st.selectbox(
            "🌍 Lugar de la aventura",
            [
                "Bosque mágico",
                "Castillo encantado",
                "Espacio",
                "Selva misteriosa",
                "Océano brillante",
                "Pueblo fantástico"
            ]
        )

        stroke_width = st.slider(
            "🖍️ Grosor del pincel",
            1,
            25,
            5
        )

    # =========================
    # API KEY DESDE LA PÁGINA
    # =========================

    api_key = st.text_input(
        "🔑 Ingresa tu API Key de OpenAI",
        type="password",
        placeholder="sk-..."
    )

    if not api_key:
        st.warning("⚠️ Ingresa tu API Key para continuar.")
        st.stop()

    # =========================
    # FRASES ALEATORIAS
    # =========================

    frases = [
        "🌟 Tu imaginación puede crear mundos mágicos",
        "🦄 Cada dibujo tiene una historia escondida",
        "📚 Los mejores personajes nacen aquí",
        "✨ Hoy puedes inventar algo increíble"
    ]

    st.markdown(
        f"""
        <div class="tip-box">
        {random.choice(frases)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # CANVAS DE DIBUJO
    # =========================

    st.markdown("## 🎨 Dibuja tu personaje")

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color="#000000",
        background_color="#FFFFFF",
        height=350,
        width=500,
        drawing_mode="freedraw",
        key="canvas",
    )

    # =========================
    # BOTÓN CREAR HISTORIA
    # =========================

    if st.button("✨ Crear Fábula"):

        if canvas_result.image_data is None:

            st.warning(
                "⚠️ Dibuja un personaje primero."
            )

        else:

            client = OpenAI(api_key=api_key)

            with st.spinner(
                "🎨 Analizando dibujo..."
            ):

                img_array = np.array(
                    canvas_result.image_data
                )

                image = Image.fromarray(
                    img_array.astype("uint8")
                ).convert("RGBA")

                image.save("personaje.png")

                base64_image = encode_image(
                    "personaje.png"
                )

                # =========================
                # ANALIZAR DIBUJO
                # =========================

                descripcion_prompt = """
                Analiza este dibujo infantil.

                Describe:
                - Qué personaje parece ser
                - Cómo se ve
                - Qué emociones transmite

                Responde en español
                de forma corta y amigable.
                """

                descripcion_response = (
                    client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": descripcion_prompt
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url":
                                            f"data:image/png;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=200,
                    )
                )

                descripcion = (
                    descripcion_response
                    .choices[0]
                    .message
                    .content
                )

                st.session_state.descripcion_personaje = descripcion

                st.success(
                    "🎉 ¡Personaje descubierto!"
                )

                st.markdown(
                    "### 🧸 Tu personaje"
                )

                st.write(descripcion)

            # =========================
            # CREAR HISTORIA
            # =========================

            with st.spinner(
                "📖 Creando fábula mágica..."
            ):

                historia_prompt = f"""
                Basado en esta descripción:

                {descripcion}

                Crea una fábula infantil
                corta y divertida.

                La historia debe:
                - Ocurrir en: {lugar}
                - Tener diálogos simples
                - Ser muy imaginativa
                - Tener un final feliz
                - Enseñar esta moraleja:
                '{moraleja}'

                Usa lenguaje fácil para niños.
                """

                historia_response = (
                    client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "user",
                                "content": historia_prompt
                            }
                        ],
                        max_tokens=700,
                    )
                )

                historia = (
                    historia_response
                    .choices[0]
                    .message
                    .content
                )

                st.session_state.historia = historia

                st.markdown(
                    "## 🌟 Tu Fábula Mágica"
                )

                st.markdown(
                    f"""
                    <div class="story-box">
                    {historia}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.balloons()
import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("voiceClienteValen1")
client1.on_message = on_message

st.title("INTERFACES MULTIMODALES")
st.subheader("COMPARTIMIENTO SECRETO")
image = Image.open('voice_ctrl.jpg')
st.image(image, width=200)

# 
st.markdown("### Comandos disponibles:")
st.markdown("""
- 🚪 *"abre el compartimiento secreto"*
- 🔒 *"cierra el compartimiento secreto"* 
""")

st.write("Toca el botón y habla")

stt_button = Button(label=" Inicio ", width=200)
stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'es-ES';

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)


comandos_validos = [
    "abre el compartimiento secreto",
    "cierra el compartimiento secreto"
]

if result:
    if "GET_TEXT" in result:
        texto_recibido = result.get("GET_TEXT").strip().lower()
        st.write(f"Escuché: *{texto_recibido}*")

       
        if texto_recibido in comandos_validos:
            st.success(f"✅ Comando reconocido: '{texto_recibido}'")
            client1.on_publish = on_publish
            client1.connect(broker, port)
            message = json.dumps({"Act1": texto_recibido})
            ret = client1.publish("voicevalen", message)
        else:
            st.warning(f"⚠️ Comando no reconocido. Intenta con uno de los comandos de la lista.")

    try:
        os.mkdir("temp")
    except:
        pass
    # =========================
    # FOOTER
    # =========================

    st.markdown("""
    <div class="footer">
    ✨ Hecho por Valentina Marin y Samuel Acevedo ✨
    </div>
    """, unsafe_allow_html=True)
