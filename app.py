# app.py

import streamlit as st
from datetime import datetime
from agents import academic_coordinator

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Research AI",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# TIME GREETING
# -----------------------------------
hour = datetime.now().hour

if hour < 12:
    greeting = "🌅 Good Morning"
elif hour < 17:
    greeting = "☀️ Good Afternoon"
elif hour < 21:
    greeting = "🌇 Good Evening"
else:
    greeting = "🌙 Good Night"

# -----------------------------------
# CSS
# -----------------------------------
st.markdown("""
<style>

/* Main */
.stApp {
    background-color: #0b0b0f;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111217;
    border-right: 1px solid #222;
    width: 310px !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Sidebar buttons */
.stButton > button {
    width: 100%;
    background-color: transparent;
    color: white;
    border: none;
    text-align: left;
    padding: 10px;
    border-radius: 12px;
    font-size: 15px;
}

.stButton > button:hover {
    background-color: #1f2128;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background: linear-gradient(
        135deg,
        rgba(0,255,200,0.08),
        rgba(0,120,255,0.08)
    );
    border-radius: 18px;
    padding: 14px;
    margin-bottom: 14px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* User Chat */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: linear-gradient(
        135deg,
        rgba(255,0,150,0.10),
        rgba(255,120,0,0.08)
    );
}

/* Assistant Chat */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: linear-gradient(
        135deg,
        rgba(0,255,200,0.10),
        rgba(0,120,255,0.10)
    );
}

/* Greeting */
.greeting {
    text-align: center;
    font-size: 34px;
    color: #d9d9d9;
    margin-top: 60px;
}

/* Main title */
.main-title {
    font-size: 72px;
    font-weight: bold;
    text-align: center;
    margin-top: 20px;
    color: white;
}

/* Search box */
.stChatInput {
    position: fixed;
    bottom: 18px;
    left: 360px;
    right: 40px;
    z-index: 999;
}

/* Input */
.stChatInput textarea {
    background-color: #1b1d24 !important;
    color: white !important;
    border-radius: 30px !important;
    border: 1px solid #333 !important;
    padding: 18px !important;
    font-size: 17px !important;
}

/* Sidebar title */
.top-title {
    font-size: 34px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
    margin-left: 8px;
}

/* Hide Streamlit */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SESSION STATE
# -----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model" not in st.session_state:
    st.session_state.model = "meta-llama/llama-3-8b-instruct"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pinned_chats" not in st.session_state:
    st.session_state.pinned_chats = []

if "active_menu" not in st.session_state:
    st.session_state.active_menu = None

# -----------------------------------
# SIDEBAR
# -----------------------------------
with st.sidebar:

    st.markdown(
        "<div class='top-title'>📘 RESEARCH AI</div>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # New Chat
    if st.button("➕ New Chat"):

        st.session_state.messages = []

        st.rerun()

    st.markdown("### Chats")

    # -----------------------------------
    # CHAT HISTORY
    # -----------------------------------
    for index, chat in enumerate(
        reversed(st.session_state.chat_history)
    ):

        real_index = len(st.session_state.chat_history) - 1 - index

        col1, col2 = st.columns([8,1])

        # Chat Name
        with col1:

            st.markdown(
                f"""
<div style="
padding:12px;
border-radius:12px;
margin-bottom:8px;
background:#1b1d24;
color:white;
font-size:15px;
">
{chat[:40]}
</div>
""",
                unsafe_allow_html=True
            )

        # 3 dots
        with col2:

            if st.button("⋮", key=f"menu_{real_index}"):

                if st.session_state.active_menu == real_index:
                    st.session_state.active_menu = None
                else:
                    st.session_state.active_menu = real_index

        # Popup menu
        if st.session_state.active_menu == real_index:

            st.markdown(
                """
<div style="
background:#1f2128;
padding:10px;
border-radius:12px;
margin-bottom:10px;
">
""",
                unsafe_allow_html=True
            )

            # Share
            if st.button(
                "🔗 Share Chat",
                key=f"share_{real_index}"
            ):

                st.success("Share feature added!")

            # Pin
            if st.button(
                "📌 Pin Chat",
                key=f"pin_{real_index}"
            ):

                if chat not in st.session_state.pinned_chats:

                    st.session_state.pinned_chats.append(chat)

                    st.success("Chat pinned!")

            # Delete
            if st.button(
                "🗑 Delete Chat",
                key=f"delete_{real_index}"
            ):

                st.session_state.chat_history.pop(real_index)

                st.session_state.active_menu = None

                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### Settings")

    st.session_state.model = st.selectbox(
        "Choose Model",
        [
            "meta-llama/llama-3-8b-instruct",
            "openai/gpt-4o-mini"
        ]
    )

# -----------------------------------
# HOME SCREEN
# -----------------------------------
if len(st.session_state.messages) == 0:

    st.markdown(
        f"""
<div class="greeting">
{greeting}
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown(
        """
<div class="main-title">
What's on your mind today?
</div>
""",
        unsafe_allow_html=True
    )

# -----------------------------------
# DISPLAY CHAT
# -----------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -----------------------------------
# INPUT
# -----------------------------------
prompt = st.chat_input("Ask Research AI")

# -----------------------------------
# MAIN CHAT
# -----------------------------------
if prompt:

    # Save history
    st.session_state.chat_history.append(prompt)

    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # Assistant
    with st.chat_message("assistant"):

        with st.spinner("Researching..."):

            papers, analysis = academic_coordinator(
                prompt,
                st.session_state.model
            )

            response = f"# 📚 Research Topic: {prompt}\n\n"

            # Papers
            if papers:

                response += "## 📄 Research Papers\n\n"

                for i, paper in enumerate(papers, start=1):

                    response += f"""
### {i}. {paper['title']}

👨‍🔬 Authors: {', '.join(paper['authors'])}

📅 Published: {paper['published']}

🔗 {paper['url']}

📝 Summary:

{paper['summary'][:400]}

---

"""

            else:

                response += "No research papers found.\n\n"

            # Analysis
            response += f"""

# 🧠 AI Analysis

{analysis}
"""

            # Typing effect
            placeholder = st.empty()

            full_response = ""

            for line in response.split("\n"):

                full_response += line + "\n"

                placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
