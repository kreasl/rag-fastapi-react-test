import json
from pypdf import PdfReader
import operator
import os
from typing import Annotated, List, TypedDict

from langchain import hub
from langchain_anthropic import ChatAnthropic

from langgraph.graph import END, StateGraph, START
from langgraph.types import Send

class CvState(TypedDict):
    questions: list
    context: str
    intermediate_answers: Annotated[list, operator.add]
    final_answer: str

class QuestionState(TypedDict):
    question: str
    context: str

ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")

def load_pdf(path: str):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n\n"

    return text

def answer_questions(state: CvState):
    return [Send("question", {"question": question, "context": state["context"]}) for question in state["questions"]]

def question_function(state: QuestionState):
    question = state["question"]
    context = state["context"]

    prompt = hub.pull("rlm/rag-prompt")

    formatted_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(formatted_prompt)

    return {"intermediate_answers": [json.dumps({"answer": response.content, "question": question})]}

def recap_function(state: CvState):
    return {"final_answer": "\n--\n".join(state["intermediate_answers"])}

def create_rag_graph():
    workflow = StateGraph(CvState)

    workflow.add_node("question", question_function)
    workflow.add_node("recap", recap_function)

    workflow.add_conditional_edges(START, answer_questions, ["question"])
    workflow.add_edge("question", "recap")
    workflow.add_edge("recap", END)

    return workflow.compile()

def analyze_cv(pdf_path: str, questions: List[str]):
    context = load_pdf(pdf_path)

    state = CvState(
        context=context,
        questions=questions,
        intermediate_answers=[],
        final_answer=""
    )

    graph = create_rag_graph()
    result = graph.invoke(state)

    return result["final_answer"]

if __name__ == "__main__":
    pdf_path = os.path.join(ROOT_PATH, "uploads", "0d9c50ac-5c51-4b18-9524-59382ce2ce18.pdf")
    questions = [
        "What is the applicant's name?",
        "What is the applicant's education?",
        "Where's the applicant located?"
        "What is the applicant's expertise?",
        """<instructions>
            <identity>
                - You are an AI recruitment assistant specialized in analyzing CVs to extract and summarize FrontEnd development skills.
            </identity>
            <purpose>
                - Your goal is to identify FrontEnd development skills from an applicant's CV and provide a formatted summary of each skill.
            </purpose>
            <context>
                - The CVs you process may vary in format and structure, containing sections like work experience, education, skills, and certifications.
                - FrontEnd skills may be explicitly listed under a skills section or mentioned within job descriptions, projects, or certifications.
            </context>
            <task>
                - Analyze the provided CV text to identify FrontEnd development skills.
                - For each skill, extract the most relevant company and provide a brief summary of the applicant's experience with that skill.
                - Format the output as a bullet list, with each item containing the skill's name, the most relevant company, and a short summary.
            </task>
            <constraints>
                - Focus solely on FrontEnd development skills, ignoring unrelated information.
                - Do not provide any preamble or explanation; output only the formatted list.
                - Maintain confidentiality and do not store any personal data from the CV.
            </constraints>
            <examples>
                <example>
                    <input>
                        <cv>
                            Jane Smith
                            Experience: FrontEnd Developer at ABC Inc - Built responsive web applications using React and Redux.
                            Skills: JavaScript, React, HTML, CSS
                            Education: BSc in Information Technology
                        </cv>
                    </input>
                    <output>
                        - JavaScript: ABC Inc - Developed interactive web applications with a focus on performance and scalability.
                        - React: ABC Inc - Built responsive web applications using React and Redux.
                        - HTML: ABC Inc - Implemented semantic HTML for improved accessibility and SEO.
                        - CSS: ABC Inc - Styled web applications with modern CSS techniques for a consistent look and feel.
                    </output>
                </example>
            </examples>
        </instructions>""",
        """Give me a list of applicant's Backend skills as a bullet list.
        Provide no less than 3 and no more than 10 skills. Make sure that the skills are sorted starting from most industry-relevant ones.
        For each item provide tool name, most relevant company name and a very short summary of application of the skill.
        Make each item no more than 40 words long""",
        """Give me a list of applicant's skills that are relevant in DevOps activities as a bullet list
        Provide no less than 3 and no more than 10 skills. Make sure that the skills are sorted starting from most industry-relevant ones.
        For each item provide tool name, most relevant company name and a very short summary of application of the skill.
        Make each item no more than 40 words long""",
        """<instructions>
            <identity>
                - You are an AI recruitment assistant specialized in analyzing CVs to extract relevant skills.
            </identity>
            <purpose>
                - Your goal is to identify and extract all AI-related skills from an applicant's CV.
            </purpose>
            <context>
                - The CVs you process may vary in format and structure, containing sections like work experience, education, skills, and certifications.
                - AI skills may be explicitly listed under a skills section or mentioned within job descriptions, projects, or certifications.
            </context>
            <task>
                - Analyze the provided CV text to identify AI-related skills.
                - Extract and list these skills clearly and concisely.
                - Ensure no additional commentary or formatting is included beyond the list of skills.
            </task>
            <constraints>
                - Focus solely on AI-related skills, ignoring unrelated information.
                - Do not provide any preamble or explanation; output only the list of skills.
                - Maintain confidentiality and do not store any personal data from the CV.
                - If there's no relevant skills - say that there are no relevant skills.
            </constraints>
            <format>
                - the output should be formatted as bulleted list
                - provide no less than 3 skills, but no more than 10
                - for each skill provide skill's name, most relevant company name and a very short summary of applicant's experience with applying the skill.
            </format>
            <examples>
                <example>
                    <input>
                        <cv>
                            John Doe
                            Experience: Data Scientist at XYZ Corp - Developed machine learning models using Python and TensorFlow.
                            Skills: Python, Machine Learning, Deep Learning, Data Analysis
                            Education: MSc in Computer Science
                        </cv>
                    </input>
                    <output>
                        - Machine Learning, XYZ Corp, Developed Machine Learning models
                        - Deep Learning, XZY Corp, used Deep Learning skill
                        - TensorFlow, YYZ Corp, used Tensorflow for machine learning models
                    </output>
                </example>
            </examples>
        </instructions>""",
    ]

    result = analyze_cv(pdf_path, questions)
    print(result)
