import streamlit as st
from pdf_parser import extract_text_from_pdf
from quiz_engine import generate_quiz
from config import (
    DEFAULT_QUESTIONS, MIN_QUESTIONS,
    MAX_QUESTIONS, QUESTIONS_STEP, MIN_WORDS_IN_PDF, MODEL
)

st.set_page_config(page_title="AI Quiz Generator", page_icon="🧠", layout="centered")

st.title("🧠 AI Self-Assessment Quiz")
st.caption("Upload your study material and let AI generate a quiz for you.")

with st.sidebar:
    st.header("⚙️ Settings")
    num_questions = st.slider(
        "Number of questions",
        min_value=MIN_QUESTIONS,
        max_value=MAX_QUESTIONS,
        value=DEFAULT_QUESTIONS,
        step=QUESTIONS_STEP
    )
    st.divider()
    st.info(f"Running **{MODEL}** via Ollama locally.")
    # st.code("ollama serve\nollama pull qwen2.5:3b", language="bash")

# --- File Upload ---
uploaded_file = st.file_uploader("📄 Upload your study material (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading and saving PDF..."):
        try:
            study_text = extract_text_from_pdf(uploaded_file)
            word_count = len(study_text.split())
            st.success(f"PDF saved to `uploads/` — {word_count} words extracted.")

            if word_count < MIN_WORDS_IN_PDF:
                st.warning("The PDF seems too short. Try a more detailed document.")
        except Exception as e:
            st.error(f"Failed to read PDF: {e}")
            st.stop()

    # --- Generate Button ---
    if st.button("🚀 Generate Quiz", type="primary", use_container_width=True):
        with st.spinner(f"Generating {num_questions} questions using {MODEL}... (may take a while)"):
            try:
                questions = generate_quiz(study_text, num_questions)
                st.session_state["questions"] = questions
                st.session_state["show_answers"] = [False] * len(questions)
                st.session_state["study_text_loaded"] = True
            except ConnectionError as e:
                st.error(str(e))
                st.stop()
            except ValueError as e:
                st.error(str(e))
                st.stop()
            except RuntimeError as e:
                st.error(str(e))
                st.stop()

# --- Render Quiz --- THIS MUST BE OUTSIDE THE if uploaded_file BLOCK
if "questions" in st.session_state and st.session_state["questions"]:
    questions = st.session_state["questions"]

    st.divider()
    st.subheader(f"📝 Quiz — {len(questions)} Questions")

    if st.button("🔄 Hide All Answers"):
        st.session_state["show_answers"] = [False] * len(questions)
        st.rerun()

    for i, q in enumerate(questions):
        with st.container(border=True):
            st.markdown(f"**Q{i+1}. {q['question']}**")

            options = q.get("options", {})
            for key, value in options.items():
                st.markdown(f"&nbsp;&nbsp;&nbsp;**{key}.** {value}")

            st.write("")

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button(
                    "👁 Hide Answer" if st.session_state["show_answers"][i] else "💡 Show Answer",
                    key=f"toggle_{i}"
                ):
                    st.session_state["show_answers"][i] = not st.session_state["show_answers"][i]
                    st.rerun()

            if st.session_state["show_answers"][i]:
                answer_key = q.get("answer", "")
                answer_text = options.get(answer_key, "")
                explanation = q.get("explanation", "")

                st.success(f"✅ Correct Answer: **{answer_key}. {answer_text}**")
                if explanation:
                    st.info(f"📖 **Explanation:** {explanation}")