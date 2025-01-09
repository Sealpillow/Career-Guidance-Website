

# NTUCCDS: Career Connection & Development System for NTU Students

> Empowering Futures: Your Pathway to Career Success at NTU. </br>

## Features

- Job matching: Based on skill set listed on the resume, match job listing to skill set. 
- AI chatbots Interview: Generate personalized interview questions based on the job requirements and the interviewee's resume.
- Improve Resume: Enhancing the user's resume to align with the job requirements.

## Table of Contents

- [About the Project](#about-the-project)
  - [Overview](#overview)   
  - [Built With](#built-with)  
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
---

## About the Project

### Overview
> To match users with tech roles based on their skill sets and improve their chances of landing their dream job.

### Built With
Major frameworks, libraries, and languages used in this project. For example:
- [Flask](https://flask.palletsprojects.com/)
- [Python](https://www.python.org/)
- [Groq](https://groq.com/)
- [sentence-transformers](https://pypi.org/project/sentence-transformers/)
- [langchain-chroma](https://pypi.org/project/langchain-chroma/)
- [langchain-huggingface](https://pypi.org/project/langchain-huggingface/)
- [langchain-groq](https://pypi.org/project/langchain-groq/)
- [pandas](https://pypi.org/project/pandas/)
- [streamlit](https://pypi.org/project/streamlit/)
- [flask](https://pypi.org/project/flask/)
- [openpyxl](https://pypi.org/project/openpyxl/)
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)
- [reportlab](https://pypi.org/project/reportlab/)
- [waitress](https://pypi.org/project/waitress/)

---

## Getting Started

These instructions will help you set up the project on your local machine.

### Prerequisites
- Install [Python](https://www.python.org/downloads/)
- Ensure that an IDE is installed:
  - Visual Studio Code (Recommended): Download [VS Code](https://code.visualstudio.com/Download)
- Create [Groq Account](https://console.groq.com/login)
  - Create [API Key](https://console.groq.com/keys)
  - Create .env file in the main directory and copy over the API Key
    ```
    API_Key = xxxxxxxxxxxxx
    ```     

### Installation
1. Download the Zip File
2. Install dependencies:
   ```python
   pip install -r requirements.txt
   ```
3. If there is error during installing of dependencies: chromadb==0.5.0
   - Go to this page: [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Click on "Download Build Tools" and run what you downloaded
   - Click on "Install" (a window with different options to click should show up)
   - Click only on "Desktop Development with C++" and click on install 
   - Reboot your system


---

## Usage

Step 1: Run webApp.py
```python
python webApp.py
```
Step 2: Copy this to browser to access application
```
http://localhost:8080/
```
Step 3: Open Video Folder for full demo
        
## My Role in the project
- Contributed to the backend development of the application using the Flask web framework as part of a team.
- Created a chatbot using a large language model (LLM) 
- Developed an interview practice chatbot using the Llama 3-8B-8192 large language model, deployed and optimized on GroqCloud for scalable, high-performance inference. The chatbot simulates interview scenarios, providing real-time feedback and personalized question generation to enhance user practice.
- Developed a program that generates recommended LeetCode questions tailored to specific job titles, utilizing algorithms to match relevant coding problems with job requirements and skill levels.
