import streamlit as st
import random
from fetch_content import get_latest_articles
from summarize import summarize_text, extract_concepts
from concepts import add_to_learned, add_to_future_list
from memory import update_memory
from memory import get_learned_topics
from concepts import get_to_learn_topics

# --- Set page title and icon ---
st.set_page_config(page_title="LearnPulse", page_icon="🧠")

# --- Initialize session state ---
if "step" not in st.session_state:
    st.session_state.step = "start"
    st.session_state.article = None
    st.session_state.summary = ""
    st.session_state.concepts = []
    st.session_state.selected_concept = ""
    st.session_state.articles = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Message logger ---
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- Custom CSS for Modern UI ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:wght@400;700&family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Inter', 'DM Serif Display', serif !important;
        background-color: #f8f6ef;
    }
    .big-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3.5rem;
        color: #23422e;
        margin-bottom: 0.2em;
        margin-top: 0.5em;
        letter-spacing: -2px;
    }
    .subtitle {
        font-size: 1.3rem;
        color: #23422e;
        margin-bottom: 1.5em;
    }
    .card {
        background: #fff;
        border-radius: 24px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        padding: 1.5em 1.5em 1em 1.5em;
        margin-bottom: 1.2em;
        display: flex;
        align-items: center;
        gap: 1em;
    }
    .card-emoji {
        font-size: 2.2rem;
        margin-right: 0.7em;
    }
    .learn-btn button {
        background: #23422e !important;
        color: #fff !important;
        border-radius: 32px !important;
        font-size: 1.2rem !important;
        padding: 0.7em 2.2em !important;
        margin-top: 1.2em;
        margin-bottom: 1.2em;
    }
    .sidebar-section {
        background: #fff;
        border-radius: 18px;
        padding: 1em 1em 0.5em 1em;
        margin-bottom: 1.2em;
        box-shadow: 0 1px 6px rgba(0,0,0,0.03);
    }
    .sidebar-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.2rem;
        color: #23422e;
        margin-bottom: 0.5em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Topics History Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🏆 Topics Covered</div>', unsafe_allow_html=True)
    learned = get_learned_topics()
    if learned:
        for topic in learned:
            st.markdown(f"- {topic}")
    else:
        st.markdown("_No topics learned yet._")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📌 Topics To Cover</div>', unsafe_allow_html=True)
    to_learn = get_to_learn_topics()
    if to_learn:
        for topic in to_learn:
            st.markdown(f"- {topic}")
    else:
        st.markdown("_No topics saved for later._")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Free Text Q&A ---
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">💬 Ask a Question</div>', unsafe_allow_html=True)
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []
    user_question = st.text_input("Type your question and press Enter", key="free_text_qa")
    if user_question:
        answer = summarize_text(user_question, prompt_type="concept")
        st.session_state.qa_history.append((user_question, answer))
        st.experimental_rerun()
    for q, a in reversed(st.session_state.qa_history[-5:]):
        st.markdown(f"<b>You:</b> {q}", unsafe_allow_html=True)
        st.markdown(f"<b>LearnPulse:</b> {a}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- App Header ---
st.markdown('<div class="big-title">I’m LearnPulse</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your AI-powered learning assistant for mastering new AI concepts. Get summaries, explore key topics, and track your progress—all in one place.</div>', unsafe_allow_html=True)

# --- Main Action Cards (only on start screen) ---
if st.session_state.step == "start":
    st.markdown('<div class="learn-btn">', unsafe_allow_html=True)
    if st.button("✅ I'm ready to learn"):
        articles = get_latest_articles()
        st.session_state.articles = articles
        st.session_state.step = "choose_article"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- Article Selection Step ---
if st.session_state.step == "choose_article":
    st.subheader("📰 Choose an article to explore:")
    for i, article in enumerate(st.session_state.articles):
        if st.button(article["title"], key=f"article_{i}"):
            st.session_state.article = article
            st.session_state.summary = summarize_text(article["content"], prompt_type="summary")
            st.session_state.concepts = extract_concepts(article["content"])
            add_message("user", f"I want to learn about: {article['title']}")
            add_message("ai", f"Here’s a summary of: {article['title']}\n\n{st.session_state.summary}")
            st.session_state.step = "summary"
            st.rerun()

# --- STEP 2: Show Summary + Key Concepts ---
if st.session_state.step == "summary":
    st.subheader("📘 Here’s something interesting I found:")
    st.markdown(st.session_state.summary)

    st.write("💡 **Key Concepts** — which one do you want to explore?")
    for i, concept in enumerate(st.session_state.concepts):
        if st.button(f"📖 Learn more about: {concept}", key=f"concept_{i}"):
            st.session_state.selected_concept = concept
            st.session_state.step = "concept"
            st.rerun()

    if st.button("❌ Skip for now"):
        for concept in st.session_state.concepts:
            add_to_future_list(concept)
        update_memory(st.session_state.article["title"], "skipped")
        st.success("Topics saved for later.")
        st.session_state.step = "start"

# --- STEP 3: Dive into Concept ---
if st.session_state.step == "concept":
    concept = st.session_state.selected_concept
    st.subheader(f"🧠 Let’s learn about: {concept}")
    explanation = summarize_text(f"Explain the AI concept: {concept} in beginner-friendly terms. Use a clear, concise, and professional tone.", prompt_type="concept")
    st.markdown(explanation)

    add_message("user", f"Tell me more about: {concept}")
    add_message("ai", explanation)

    if st.button("👍 That was helpful"):
        add_to_learned(concept)
        update_memory(st.session_state.article["title"], "yes")
        add_message("user", "That was helpful 👍")
        st.success("Awesome! I’ve added this to your learned topics.")
        st.session_state.step = "choose_article"

    if st.button("👎 Not helpful"):
        update_memory(st.session_state.article["title"], "no")
        add_message("user", "That wasn’t helpful 👎")
        st.info("No worries — I’ll adjust next time.")
        st.session_state.step = "choose_article"
