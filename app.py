import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response(prompt, task):
    # Get only models that support text generation
    text_models = [
        m for m in genai.list_models()
        if "generateContent" in m.supported_generation_methods
    ]

    model = genai.GenerativeModel(text_models[0].name)

    if task == "Explain Topic":
        final_prompt = f"Explain this topic in simple student-friendly language:\n{prompt}"
    elif task == "Summarize Notes":
        final_prompt = f"Summarize the following notes into clear bullet points:\n{prompt}"
    elif task == "Generate Quiz":
        final_prompt = f"Create 3 multiple-choice questions with answers:\n{prompt}"
    elif task == "Create Flashcards":
        final_prompt = f"Create 3 question-answer flashcards:\n{prompt}"
    else:
        final_prompt = prompt

    response = model.generate_content(final_prompt)
    return response.text




# ---------------- STREAMLIT UI ----------------

st.title("🎓 AI-Powered Study Buddy")

st.write("Enter a topic or paste your study notes below:")

user_input = st.text_area("")

mode = st.selectbox(
    "Choose what you want to do:",
    [
        "Explain Topic",
        "Summarize Notes",
        "Generate Quiz",
        "Create Flashcards"
    ]
)

if st.button("Generate"):
    if user_input.strip() == "":
        st.warning("Please enter a topic or notes.")
    else:
        with st.spinner("Thinking..."):
            output = get_ai_response(user_input, mode)

        st.success(mode)
        st.write(output)
