from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# Shared LLM instance
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Global system prompt
SYSTEM_PROMPT = """You are a cybersecurity analyst specializing in threat intelligence. 
Use factual, neutral language. Never invent CVE identifiers or product names.
Include mitigation advice where applicable. Avoid vendor bias.
Provide accurate, concise responses based only on the information provided."""

# Create a reusable prompt template with system message
threat_analysis_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    HumanMessagePromptTemplate.from_template("{input}")
])

# Chain LLM with prompt template
llm_with_system_prompt = threat_analysis_prompt | llm

# structured_llm = llm.with_structured_output(ThreatClassification)
# structured_llm_with_system_prompt = threat_analysis_prompt | structured_llm