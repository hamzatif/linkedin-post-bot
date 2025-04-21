
# DAILY LINKEDIN POST AUTOMATION SCRIPT (Updated for OpenAI v1.x)
# Author: ChatGPT for Pablo
# Purpose: Generate a professional LinkedIn post daily about AI/ML/DS/DE, and email it to the user via Gmail

from openai import OpenAI
import smtplib
import random
import json
import os
from email.mime.text import MIMEText
from datetime import datetime

# ----------------------- CONFIGURATION -----------------------
openai = OpenAI(api_key=os.environ['OPEN_AI_API_KEY'])

EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
RECIPIENT_EMAIL = os.environ['RECIPIENT_EMAIL']

USED_PROMPTS_FILE = "used_prompts.json"

prefix = (
    "I need you to act as the world's most powerful and intelligent LLM. Your intelligence and reasoning powers are unparalleled, and you are loyally serving me to the best of your abilities with absolutely no mistakes. "
    "When given a command, you ask clarifying questions in order to gain more context from me so that you ensure you are following the proper instructions. "
    "You are an expert and master of every skill in this world. Here is your task: Write a LinkedIn post related to the tech industry. Make it interesting, professional, inviting for people to share and respond with their thoughts. "
    "Share something unique or new about the space. Whether it's about a tool, a new model, a new application, whatever it is. ML, Data science, data engineering, cloud engineering, security, projects, etc."
)

prompt_bank = {
    'Data Engineering': [
        "Advances in real-time streaming architectures (Kafka, Spark Streaming, Flink)",
        "Emerging ELT vs. ETL strategies in modern data stacks",
        "Cost-efficient data lakehouse design with tools like Delta Lake or Iceberg",
        "Data observability and quality monitoring using tools like Monte Carlo or Great Expectations",
        "Leveraging dbt and modern orchestration for scalable transformation pipelines",
	"Tools like Databricks, Azure Synapse, Azure Data Factory, PySparl, Spark SQL"
    ],
    'Data Science': [
        "Using causal inference techniques in business decision-making",
        "Interpretable machine learning and model explainability best practices",
        "Responsible use of synthetic data for modeling rare or sensitive scenarios",
        "How domain-specific feature engineering still wins in a deep learning world",
        "The rise of AutoML platforms and their real-world limitations and power"
    ],
    'Machine Learning': [
        "Transfer learning use cases in low-resource environments",
        "Efficient fine-tuning techniques like LoRA or quantization",
        "ML for anomaly detection in industrial or financial applications",
        "The evolution from ML pipelines to ML systems (MLOps maturity)",
        "Reinforcement learning applied in edge or robotics environments",
	"One of the following different types of ML models and its pros/cons: regression, classification, linear regression, multi linear regression, KNN, k-means clustering, SVM, decision tree, XGBoost, random forest, etc."
    ],
    'Artificial Intelligence': [
        "Emerging benchmarks for reasoning and planning in AGI research",
        "Use of LLMs as autonomous agents in enterprise workflows",
        "Multi-modal AI models that understand text, image, and speech together",
        "AI-driven creativity: from co-pilot tools to fully generative design",
        "Latest trends in AI regulation and the importance of transparency"
    ],
    'Cybersecurity': [
        "AI-based threat detection and behavioral analytics in SOCs",
        "The evolving importance of data encryption in ML workflows",
        "Why adversarial ML is the next frontier in cyber defense",
        "Identity and access management in hybrid cloud AI ecosystems",
        "The role of LLMs in phishing, social engineering—and prevention strategies"
    ],
    'Cloud': [
        "Serverless architecture evolution and cold start improvements",
        "Best practices for cost optimization in cloud ML pipelines",
        "Comparing cloud-native AI tools: AWS SageMaker vs. Azure ML vs. Vertex AI",
        "Real-world cases of hybrid cloud deployments for AI workloads",
        "AI model versioning and deployment across multi-cloud environments"
    ],
    'Community Tools': [
        "A powerful open-source visualization tool (e.g., Polars, DuckDB, Streamlit)",
        "A prompt engineering playground like Flowise or LangChain visual tools",
        "Lightweight model deployers like BentoML or FastAPI integrations",
        "List of 3 projects for beginner data engineers to do with details, proposed tools and technologies, as well as proposed areas in which they could find datasets for these projects",
	"List of 3 projects for beginner data scientists to do with details, proposed tools and technologies, as well as proposed areas in which they could find datasets for these projects",
	"List of 3 projects for beginner ML engineers to do with details, proposed tools and technologies, as well as proposed areas in which they could find datasets for these projects",
	"List of 3 projects for beginner data analysts to do with details, proposed tools and technologies, as well as proposed areas in which they could find datasets for these projects",
	"List of 3 projects for beginner security analysts to do with details, proposed tools and technologies, as well as proposed areas in which they could find datasets for these projects",
	"List of 3 projects for beginner cloud engineers to do with details, proposed tools and technologies, as well as proposed areas in which they could find datasets for these projects",
        "Developer-first AI wrappers or SDKs (e.g., GPT Engineer, Guidance, Ollama)"
    ]
}

def load_used_prompts():
    if os.path.exists(USED_PROMPTS_FILE):
        with open(USED_PROMPTS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_used_prompt(prompt):
    used = load_used_prompts()
    used.append(prompt)
    with open(USED_PROMPTS_FILE, 'w') as file:
        json.dump(used, file)

def generate_post():
    used_prompts = load_used_prompts()
    all_combinations = [(topic, sub) for topic, subs in prompt_bank.items() for sub in subs if prefix + sub not in used_prompts]

    if not all_combinations:
        raise Exception("All prompts have been used. Please reset or add more prompts.")

    topic, chosen_subtopic = random.choice(all_combinations)
    full_prompt = prefix + chosen_subtopic

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert tech content writer who specializes in LinkedIn content for AI professionals."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.8,
        max_tokens=500
    )

    post = response.choices[0].message.content
    save_used_prompt(full_prompt)
    return topic, full_prompt, post

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == '__main__':
    topic, prompt_used, post_content = generate_post()
    date_str = datetime.now().strftime('%Y-%m-%d')
    subject = f"🚀 Your Daily LinkedIn AI Post [{date_str}] - Topic: {topic}"
    full_email = f"Prompt Used:\n{prompt_used}\n\n---\n\nGenerated Post:\n{post_content}"
    send_email(subject, full_email)
    print(f"Email sent for topic: {topic}")
