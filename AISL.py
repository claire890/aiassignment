import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# 🔐 Directly set API key — this bypasses secrets.toml issues
os.environ["OPENAI_API_KEY"] = "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"

# ✅ Initialize model
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7
)

# ✅ Prompt
template = """
You are a personalized educational assistant for an after-school program.

Based on the student’s profile below, generate:
1. A weekly personalized learning plan
2. 3 engaging lesson titles
3. 2 creative activity suggestions
4. 1 motivational message

Student Profile:
- Name: {name}
- Age: {age}
- Grade: {grade}
- Learning Style: {learning_style}
- Interests: {interests}
- Academic Challenges: {difficulty}

Ensure the content is age-appropriate, encouraging, and creatively written.
"""

prompt = PromptTemplate(
    input_variables=["name", "age", "grade", "learning_style", "interests", "difficulty"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# ✅ Streamlit UI
st.set_page_config(page_title="Youth Ed Assistant", page_icon="📚")
st.title("📚 Youth Development: Personalized Learning Assistant")

with st.form("student_form"):
    name = st.text_input("👤 Student Name")
    age = st.text_input("🎂 Age")
    grade = st.text_input("🏫 Grade Level")
    learning_style = st.selectbox("🧠 Learning Style", ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"])
    interests = st.text_area("🎨 Interests", placeholder="e.g. space, animals, puzzles")
    difficulty = st.text_area("⚠️ Academic Challenges", placeholder="e.g. reading comprehension")

    submitted = st.form_submit_button("Generate Learning Plan")

if submitted:
    with st.spinner("🧠 Thinking..."):
        try:
            result = chain.run({
                "name": name,
                "age": age,
                "grade": grade,
                "learning_style": learning_style,
                "interests": interests,
                "difficulty": difficulty
            })

            st.success("✅ Personalized Plan Generated!")
            st.markdown("### 📝 Personalized Learning Plan")
            st.write(result)

        except Exception as e:
            st.error("🚨 An error occurred while generating the content.")
            st.exception(e)
