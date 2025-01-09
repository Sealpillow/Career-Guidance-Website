import json
import re
import time
from ResumePromptCreator import ResumePromptCreator
from json_validator import JSONValidator
from groq import Groq

class ResumeGenerator:
    
    def __init__(self, api_key):
        self.resume_prompt_creator = ResumePromptCreator()
        self.json_validator = JSONValidator()  # Instantiate JSONValidator
        self.client = Groq(api_key=api_key)  # Initialize Groq client with API key

    @staticmethod
    def extract_json_from_string(text):
        # Use a general regular expression pattern to find the JSON structure within the string from the first { to the last }
        json_pattern = r'{.*}'
        
        # Search for the JSON block in the string
        match = re.search(json_pattern, text, re.DOTALL)
        
        if match:
            # Extract the JSON part from the matched string
            json_str = match.group(0)
            
            # Attempt to parse the JSON string to a Python dictionary
            try:
                json_data = json.loads(json_str)
                return json_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("No JSON found in the string.")
            return None

    @staticmethod
    def save_json_to_file(data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def generate_response(self, content):
        # Use the Groq client to make a completion request
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": content,
                        }],model="llama3-8b-8192",)
                    
        
        parsed_response = chat_completion.choices[0].message.content
        return parsed_response

    def create_resume(self, job_description, education_section=None, project_section=None, 
                      intern_experience_section=None, 
                      co_curricular_section=None, skills_section=None,
                      achievement_section=None, interest_section=None, contact_section=None, filePath=None):
        
        # Dictionary to hold all resume sections
        resume = {}

        # Add the contact section
        if contact_section:
            resume['contact'] = contact_section  # Directly assign the string to the contact field
            print(json.dumps(resume['contact'], indent=2))
        else:
            resume['contact'] = None

        # Check and handle education section
        if education_section:
            while True:
                education_response = self.generate_response(
                    self.resume_prompt_creator.create_resume_prompt_education(job_description, education_section)
                )
                education_response = self.extract_json_from_string(education_response)
                if JSONValidator.is_valid_education_format(education_response):
                    resume['education'] = education_response  # Save directly as dictionary
                    print(json.dumps(resume['education'], indent=2))
                    break  # Exit loop if the response is valid
        else:
            resume['education'] = None

        # Check and handle academic project section
        if project_section:
            while True:
                academic_response = self.generate_response(
                    self.resume_prompt_creator.create_resume_prompt_academic(job_description, project_section)
                )
                academic_response = self.extract_json_from_string(academic_response)
                if JSONValidator.is_valid_projects_format(academic_response):
                    resume['projects'] = academic_response  # Save directly as dictionary
                    print(json.dumps(resume['projects'], indent=2))
                    break  # Exit loop if the response is valid
        else:
            resume['projects'] = None

        # Check and handle intern experience section
        if intern_experience_section:
            while True:
                experience_response = self.generate_response(
                    self.resume_prompt_creator.create_resume_prompt_experience(
                        job_description, 
                        intern_experience_section=intern_experience_section
                    )
                )
                experience_response = self.extract_json_from_string(experience_response)
                if JSONValidator.is_valid_experience_format(experience_response):
                    resume['experience'] = experience_response  # Save directly as dictionary
                    print(json.dumps(resume['experience'], indent=2))
                    break  # Exit loop if the response is valid
        else:
            resume['experience'] = None

        # Check and handle co-curricular section
        if co_curricular_section:
            while True:
                co_curricular_response = self.generate_response(
                    self.resume_prompt_creator.create_resume_prompt_co_curricular(job_description, co_curricular_section)
                )
                co_curricular_response = self.extract_json_from_string(co_curricular_response)
                if JSONValidator.is_valid_co_curricular_activities_format(co_curricular_response):
                    resume['co_curricular'] = co_curricular_response  # Save directly as dictionary
                    print(json.dumps(resume['co_curricular'], indent=2))
                    break  # Exit loop if the response is valid
        else:
            resume['co_curricular'] = None

        # Check and handle skills section
        if skills_section:
            while True:
                skills_response = self.generate_response(
                    self.resume_prompt_creator.create_resume_prompt_skills(job_description, skills_section)
                )
                skills_response = self.extract_json_from_string(skills_response)
                if JSONValidator.is_valid_skills_format(skills_response):
                    resume['skills'] = skills_response  # Save directly as dictionary
                    print(json.dumps(resume['skills'], indent=2))
                    break  # Exit loop if the response is valid
        else:
            resume['skills'] = None

        # Check and handle achievements section
        if achievement_section:
            while True:
                achievement_response = self.generate_response(
                    self.resume_prompt_creator.create_resume_prompt_achievements_certifications(job_description, achievement_section)
                )
                achievement_response = self.extract_json_from_string(achievement_response)
                if JSONValidator.is_valid_achievements_certifications_format(achievement_response):
                    resume['achievements'] = achievement_response  # Save directly as dictionary
                    print(json.dumps(resume['achievements'], indent=2))
                    break  # Exit loop if the response is valid
        else:
            resume['achievements'] = None

        # Check and handle interests section
        if interest_section:
            while True:
                interest_response = self.generate_response(
                    self.resume_prompt_creator.create_resume_prompt_hobbies(job_description, interest_section)
                )
                interest_response = self.extract_json_from_string(interest_response)
                if JSONValidator.is_valid_hobbies_format(interest_response):
                    resume['interests'] = interest_response  # Save directly as dictionary
                    print(json.dumps(resume['interests'], indent=2))
                    break  # Exit loop if the response is valid
        else:
            resume['interests'] = None

        # Save the combined resume dictionary as a JSON file
        self.save_json_to_file(resume, filePath)

        # Return the combined resume dictionary
        return {key: value if value is not None else None for key, value in resume.items()}


