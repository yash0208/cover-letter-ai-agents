# Generative AI Resume & Cover Letter Tool

This project leverages generative AI to assist job seekers by analyzing their resumes and generating tailored cover letters. The tool aligns resumes with job descriptions scraped from job posting URLs, providing actionable feedback for improvement and creating compelling cover letters.

## Features

1. **Resume Analysis**:
   - Critiques resumes against a given job description.
   - Identifies missing skills and provides suggestions for improvement.

2. **Cover Letter Generation**:
   - Generates a professional, tailored cover letter.
   - Aligns resume points with job requirements.

3. **Job Description Scraping**:
   - Scrapes content from job posting URLs to use as the job description.

## Prerequisites

- Python 3.8+
- API keys for:
  - [Serper API](https://serper.dev/)
  - [OpenAI API](https://openai.com/api/)
- Required Python libraries:
  - `os`
  - `requests`
  - `beautifulsoup4`
  - `langchain`
  - `crewai`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/generative-ai-tools.git](https://github.com/yash0208/cover-letter-ai-agents.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Add the following keys to your environment variables:
   ```bash
   export SERPER_API_KEY="your-serper-api-key"
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## Usage

1. **Prepare Inputs**:
   - **Resume**: Provide the resume file path (TXT or similar text format).
   - **Job Description**: Provide the URL of the job posting.

2. **Run the Script**:
   Update the script with the resume file path and job description URL:
   ```python
   resume_path = "path/to/your/resume.txt"
   job_description_url = "https://example.com/job-description"
   ```

   Execute the script:
   ```bash
   python generative_ai_tools.py
   ```

3. **Output**:
   - The script will output:
     - A critique of the provided resume.
     - A tailored cover letter.

## File Structure

```
.
├── generative_ai_tools.py    # Main script
├── requirements.txt          # List of dependencies
└── README.md                 # Documentation
```

## API Details

1. **Serper API**:
   - Used for scraping job descriptions from URLs.

2. **OpenAI API**:
   - Powers the agents for resume analysis and cover letter generation.

## Key Functions

### Scrape Job Description
Scrapes the content from a given job posting URL.
```python
def scrape_job_description(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text(separator='\n', strip=True)
```

### Resume Analysis Task
Analyzes the resume and suggests improvements based on the job description.

### Cover Letter Generation Task
Generates a professional cover letter tailored to the job description.

## Notes
- Ensure your resume is in a text-readable format (e.g., `.txt`).
- The job description URL should contain accessible text content.

## Future Enhancements
- Support for PDF resumes.
- Enhanced parsing of job descriptions for structured data.
- Additional language support.


