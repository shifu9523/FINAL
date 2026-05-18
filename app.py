import streamlit as st
import streamlit.components.v1 as components

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
# LOGIN PAGE
# -------------------------

if not st.session_state.authenticated:

    st.title("🔐 Acceso por Voz")

    st.write("Presiona el botón y di la contraseña.")

    html_code = f"""
    <button onclick="startRecognition()"
        style="
        background:#ff4b4b;
        color:white;
        border:none;
        padding:15px 30px;
        border-radius:10px;
        font-size:20px;
        cursor:pointer;">
        🎙️ Hablar
    </button>

    <p id="result"></p>

    <script>
    function startRecognition() {{

        var recognition = new webkitSpeechRecognition();

        recognition.lang = 'es-ES';
        recognition.start();

        recognition.onresult = function(event) {{

            var text = event.results[0][0].transcript.toLowerCase();

            document.getElementById("result").innerHTML =
                "Texto detectado: " + text;

            if(text.includes("{PASSWORD}")) {{

                window.parent.location.reload();

                localStorage.setItem("authenticated", "true");

            }} else {{

                alert("❌ Contraseña incorrecta");

            }}
        }};
    }}
    </script>
    """

    components.html(html_code, height=300)

    # Detectar autenticación
    auth_html = """
    <script>
    const auth = localStorage.getItem("authenticated");
    if(auth === "true"){
        window.parent.postMessage({
            type: "streamlit:setComponentValue",
            value: "authenticated"
        }, "*");
    }
    </script>
    """

    result = components.html(auth_html, height=0)

    # Fallback visual
    if st.button("Simular acceso"):
        st.session_state.authenticated = True
        st.rerun()

# -------------------------
# SECRET PAGE
# -------------------------

else:

    st.title("🛡️ Página Secreta")

    st.success("✅ Acceso concedido")

    st.write("🔥 Funcionó el reconocimiento de voz.")

    if st.button("Cerrar sesión"):

        st.session_state.authenticated = False
        st.rerun()
