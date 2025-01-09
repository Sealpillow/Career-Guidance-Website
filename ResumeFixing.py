# main.py

# Add the 'my_classes' folder to Python's module search path
import sys
import os

# Debugging: print sys.path to verify that 'my_classes' is added
print(f"Python search paths: {sys.path}")

# Now import the modules from 'my_classes'
from pdf_text_extractor import PDFTextExtractor
from resume_generator import ResumeGenerator
from pdfgenerator import PDFGenerator
import json

current_dir = os.path.dirname(os.path.abspath(__file__))


def saveResumeJson(pdf_path, profileName):
    # Path to the JSON file storing job skills
    extractor = PDFTextExtractor(pdf_path)
    result_json = extractor.extract_to_json()
    resumeInfoPath = os.path.join(current_dir, f'json\{profileName}_resume.json')
    
    ### above here put at flask, pass over json to main.py
    # Save the JSON data to a file named 'extracted_resume.json'
    data = json.loads(result_json)
    print(type(data))
    with open(resumeInfoPath, 'w') as f:
        json.dump(data, f, indent=4)

    

def main(job_description, profileName):
    api_key = os.getenv('API_Key')
    resumeInfoPath = os.path.join(current_dir, f'json\{profileName}_resume.json')
    combinedResumeInfoPath = os.path.join(current_dir, f'etc\{profileName}_combined_resume.json')
    improvedResumePDFPath = os.path.join(current_dir, f'downloads\{profileName}_improved_resume.pdf')
    with open(resumeInfoPath, 'r') as json_file:
    # Load the JSON data from the file
        sections = json.load(json_file)
    print(sections)
    
    # Extract specific sections from the extracted JSON
    education_section = sections.get('EDUCATION')
    project_section = sections.get('PROJECTS')
    intern_experience_section = sections.get('intern_experience_section')  # Correct key used here
    co_curricular_section = sections.get('CCA')
    skills_section = sections.get('SKILLS')
    print(skills_section)
    contact_section = sections.get('CONTACT')
    achievement_section = sections.get('ACHIEVEMENT')
    interest_section = sections.get('INTEREST')



    # Step 2: Generate the resume using the extracted data and the job description
    resume_generator = ResumeGenerator(api_key=api_key)
    resume_data = resume_generator.create_resume(
        job_description=job_description,
        education_section=education_section,
        project_section=project_section,
        intern_experience_section=intern_experience_section,
        co_curricular_section=co_curricular_section,
        skills_section=skills_section,
        achievement_section=achievement_section,
        interest_section=interest_section,
        contact_section=contact_section,
        filePath=combinedResumeInfoPath
    )

    # Save the resume data into a JSON file
    print(combinedResumeInfoPath)
    with open(combinedResumeInfoPath, 'w') as file:
        json.dump(resume_data, file, indent=4)

    print(combinedResumeInfoPath)
    # Load the resume data from the saved JSON file
    with open(combinedResumeInfoPath, 'r') as file:
        resume_data = json.load(file)

    # Step 3: Generate a PDF from the resume data
    pdf_generator = PDFGenerator(resume_data, improvedResumePDFPath)
    pdf_generator.build_pdf()

    print(f"PDF generated: {improvedResumePDFPath}")

if __name__ == "__main__":
    # Initialize the API key for ResumeGenerator
    api_key = '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'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the path to your PDF file
    #file_path = "nobel.pdf"
    #profileName = 'Nobel'

    file_path = "nobel.pdf"
    profileName = 'nobel'

    # Define the job description for which we are creating the resume
    job_description = """
    position: cloud / .net developer location: 100% remoteduration: 3 months\r\nwork auth: us citizen or greencard only\r\n\r\nskills required: 1. azure (a lot of azure experience)2. (azure logic apps or azure service bus or azure data factory or azure event grid) must be recent3. .net/c#. must have good backend experience with 4. snowflake 5. kafka6. biztalk (must have recent experience from year 2020, 2021, 2022, 2023, or 2023)7. hl7  (must have recent experience)8. healthcare (must have recent experience)\r\n\r\n\r\nplease send your resumes to kalyan@redifcard.com  engineering, information technology
    """

    # Path to the JSON file storing job skills
    PDF_PATH = os.path.join(current_dir, f'uploads/{file_path}')
    saveResumeJson(PDF_PATH , profileName)
    main(job_description, profileName)
