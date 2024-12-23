import os
from langchain.agents import Tool
from langchain.agents import load_tools
from crewai import Agent, Task, Process, Crew
from langchain.utilities import GoogleSerperAPIWrapper
from bs4 import BeautifulSoup
import requests

# Set up API keys from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not SERPER_API_KEY or not OPENAI_API_KEY:
    raise EnvironmentError("API keys for SERPER or OpenAI are not set in environment variables.")

# Define tools
search = GoogleSerperAPIWrapper()
search_tool = Tool(
    name="Scrape Google Searches",
    func=search.run,
    description="Useful for when you need to ask the agent to search the internet",
)

human_tools = load_tools(["human"])

# Function to scrape job description from a URL
def scrape_job_description(url):
    """
    Function to scrape job description content from a given URL.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text content from the page
        return soup.get_text(separator='\n', strip=True)
    except Exception as e:
        print(f"Error scraping job description: {e}")
        return None

# Define agents
resume_analyzer = Agent(
    role="Resume Analyst",
    goal="Analyze resumes and provide specific, actionable feedback based on the job description.",
    backstory="""You are an expert in resume optimization. You help job seekers align their resumes with specific job descriptions, suggesting relevant
    skills, projects, and language enhancements to maximize their chances of success.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
)

cover_letter_writer = Agent(
    role="Professional Cover Letter Writer",
    goal="Generate professional and tailored cover letters that align resumes with job descriptions.",
    backstory="""You are an experienced cover letter writer who crafts personalized, compelling letters. You analyze the provided resume and job
    description to create tailored bullet points and a cohesive narrative.""",
    verbose=True,
    allow_delegation=True,
)

# Function to read resume data from a file
def get_resume_data(resume_file_path):
    """
    Function to read resume data from a file (e.g., PDF or text file).
    """
    try:
        with open(resume_file_path, 'r') as file:
            resume_data = file.read()
        return resume_data
    except Exception as e:
        print(f"Error reading resume: {e}")
        return None

# Example usage of the above functions to pass data to tasks
resume_path = "path/to/resume.txt"  # Replace with actual path
job_description_url = "https://example.com/job-description"  # Replace with actual job description URL

resume_data = get_resume_data(resume_path)
job_description_data = scrape_job_description(job_description_url)

if not resume_data or not job_description_data:
    raise ValueError("Resume or Job Description data is missing.")

# Create tasks for resume analysis and cover letter generation
task_analyze_resume = Task(
    description=f"""Analyze the following resume and provide a critique based on the job description:\n
    Resume:\n{resume_data}\n\nJob Description:\n{job_description_data}\n
    Highlight missing skills, suggest improvements, and ensure alignment with the job role.""",
    agent=resume_analyzer,
)

task_generate_cover_letter = Task(
    description=f"""Create a professional cover letter based on the following resume and job description:\n
    Resume:\n{resume_data}\n\nJob Description:\n{job_description_data}\n
    Align the resume's points with job requirements and ensure a compelling narrative.""",
    agent=cover_letter_writer,
)

# Instantiate the Crew
crew = Crew(
    agents=[resume_analyzer, cover_letter_writer],
    tasks=[task_analyze_resume, task_generate_cover_letter],
    verbose=2,
    process=Process.sequential,  # Tasks will be executed sequentially, passing outcomes between tasks.
)

# Run the Crew
result = crew.kickoff()

print("######################")
print(result)
