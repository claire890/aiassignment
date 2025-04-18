import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# ✅ Set API key from Streamlit Cloud secrets
# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0.7,
    openai_api_key=st.secrets["OPENAI_API_KEY"]
)



# ✅ Define the prompt template
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
    interests = st.text_area("🎨 Interests (comma-separated)", placeholder="e.g. space, animals, puzzles")
    difficulty = st.text_area("⚠️ Academic Challenges", placeholder="e.g. reading comprehension")

    submitted = st.form_submit_button("Generate Learning Plan")

if submitted:
    with st.spinner("Generating personalized content..."):
        try:
            result = chain.run({
                "name": name,
                "age": age,
                "grade": grade,
                "learning_style": learning_style,
                "interests": interests,
                "difficulty": difficulty
            })

            st.success("✅ Plan Generated!")
            st.markdown("### 📝 Personalized Learning Plan")
            st.write(result)

        except Exception as e:
            st.error("🚨 Something went wrong while generating the plan.")
            st.exception(e)
