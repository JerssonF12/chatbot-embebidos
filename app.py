import streamlit as st
import anthropic

st.set_page_config(
    page_title="Edith 🤖",
    page_icon="🔌",
    layout="centered"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Exo 2', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 50%, #0a1628 100%);
        color: #e0f0ff;
    }

    .main-title {
        font-family: 'Share Tech Mono', monospace;
        font-size: 2.2rem;
        color: #00d4ff;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85rem;
        color: #4a9ebb;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.15em;
    }

    .stChatMessage {
        background: rgba(0, 212, 255, 0.05) !important;
        border: 1px solid rgba(0, 212, 255, 0.15) !important;
        border-radius: 12px !important;
        margin-bottom: 0.8rem !important;
    }

    .stChatInputContainer {
        border-top: 1px solid rgba(0, 212, 255, 0.2) !important;
        padding-top: 1rem !important;
    }

    .topic-chip {
        display: inline-block;
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.78rem;
        color: #00d4ff;
        margin: 3px;
        font-family: 'Share Tech Mono', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown('<div class="main-title">⚡ Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">// SISTEMAS EMBEBIDOS //</div>', unsafe_allow_html=True)

# Temas iniciales
st.markdown("""
<div style="text-align:center; margin-bottom: 1.5rem;">
    <span class="topic-chip">🔧 Microcontroladores</span>
    <span class="topic-chip">🔌 Arduino / ESP32</span>
</div>
""", unsafe_allow_html=True)

# System prompt especializado
SYSTEM_PROMPT = """Eres Edith, un asistente experto en sistemas embebidos. 
Tu conocimiento abarca:
- Microcontroladores: PIC, AVR, ARM Cortex-M, ESP32, STM32, Arduino
- Protocolos de comunicación: UART, SPI, I2C, CAN, USB, Ethernet
- Sistemas operativos en tiempo real (RTOS): FreeRTOS, Zephyr, VxWorks
- Programación en C/C++ para embebidos, manejo de registros y periféricos
- Electrónica básica: GPIO, ADC, DAC, PWM, timers, interrupciones
- Diseño de hardware: PCB, esquemáticos, consumo de energía
- Depuración y herramientas: JTAG, oscilloscopio, analizadores lógicos
- IoT y conectividad: MQTT, WiFi, Bluetooth, LoRa
- Bootloaders, memoria flash, EEPROM, RAM

Responde siempre en español, de forma clara, técnica pero accesible. 
Cuando sea útil, incluye ejemplos de código en C o pseudocódigo.
Si la pregunta no está relacionada con sistemas embebidos, redirige amablemente la conversación al tema.
Usa emojis ocasionalmente para hacer las respuestas más amigables. 🔌"""

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "¡Hola! Soy **Edith** 🤖⚡\n\nEstoy aquí para ayudarte con todo lo relacionado a **sistemas embebidos**: microcontroladores, protocolos de comunicación, RTOS, programación en C, IoT y mucho más.\n\n¿Qué quieres aprender hoy?"
    })

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Pregunta sobre sistemas embebidos..."):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar a la API de Anthropic
    with st.chat_message("assistant"):
        with st.spinner("Procesando..."):
            client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            
            assistant_response = response.content[0].text
            st.markdown(assistant_response)
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
