class ResumePromptCreator:
    def __init__(self):
        pass

    def create_resume_prompt_education(self, job_description, education_section):
        prompt = f"""
        Using the information provided, improve my education section to make it more compelling and relevant to potential employers in my field, based on the provided job description. Provide the improved version in the following JSON format, ensuring consistency and that each university and its details are properly structured. Use impactful words that align with the job description to enhance the appeal. Do not add any information that is not present.

        Job Description:
        {job_description}

        Current Education Section:
        {education_section}

        Requirements:
        - Highlight any academic achievements, honors, or awards.
        - Include relevant coursework, projects, or research that align with the desired industry.
        - Output the improved education section in this JSON format:

        {{
          "education": [
            {{
              "university": "University Name",
              "details": [
                "Detail 1",
                "Detail 2",
                "Detail 3"
              ]
            }},
            {{
              "university": "Another University",
              "details": [
                "Detail 1",
                "Detail 2",
                "Detail 3"
              ]
            }}
          ]
        }}

        Please provide only the JSON output as specified, without any additional text or explanations.
        """
        return prompt

    def create_resume_prompt_academic(self, job_description, project_section):
        prompt = f"""
        Using the information provided, improve my academic project section to make it more compelling and relevant to potential employers in my field, based on the provided job description. Provide the improved version in the following JSON format, ensuring consistency and that each project and its details are properly structured. Use impactful words that align with the job description to enhance the appeal. Do not add any information that is not present.

        Job Description:
        {job_description}

        Current Academic Project Section:
        {project_section}

        Requirements:
        - Highlight significant accomplishments, innovations, or results achieved.
        - Emphasize relevant skills, technologies, or methodologies used that align with the desired industry.
        - Output the improved academic project section in this JSON format:

        {{
          "projects": [
            {{
              "project_title": "Project Title",
              "details": [
                "Detail 1",
                "Detail 2",
                "Detail 3"
              ]
            }},
            {{
              "project_title": "Another Project Title",
              "details": [
                "Detail 1",
                "Detail 2",
                "Detail 3"
              ]
            }}
          ]
        }}

        Please provide only the JSON output as specified, without any additional text or explanations.
        """
        return prompt

    def create_resume_prompt_experience(self, job_description, intern_experience_section=None, work_experience_section=None):
        sections = []
        if intern_experience_section:
            sections.append("intern experience")
        if work_experience_section:
            sections.append("work experience")
        sections_str = " and ".join(sections)
        prompt = f"""
        Improve my {sections_str} section{'s' if len(sections) > 1 else ''} to make {'them' if len(sections) > 1 else 'it'} more compelling and relevant to potential employers in my field, based on the provided job description. Provide the improved version{'s' if len(sections) > 1 else ''} in JSON format only, ensuring consistency and that each position and its details are properly structured. Use impactful words that align with the job description to enhance the appeal. Use only the information provided.

        Job Description:
        {job_description}
        """
        if intern_experience_section:
            prompt += f"\nIntern Experience Section:\n{intern_experience_section}\n"
        if work_experience_section:
            prompt += f"\nWork Experience Section:\n{work_experience_section}\n"

        prompt += """\nRequirements:
        - Highlight significant accomplishments, responsibilities, or results achieved.
        - Emphasize relevant skills, technologies, or methodologies used that align with the desired industry.
        Output format:
        {{
          "experience": [
            {{
              "position_title": "Position Title",
              "company": "Company Name",
              "details": [
                "Detail 1",
                "Detail 2",
                "Detail 3"
              ]
            }},
            {{
              "position_title": "Another Position Title",
              "company": "Another Company Name",
              "details": [
                "Detail 1",
                "Detail 2",
                "Detail 3"
              ]
            }}
          ]
        }}

       Return only the JSON output as specified, without any additional content.
    """
        return prompt

    def create_resume_prompt_co_curricular(self, job_description, co_curricular_section):
        prompt = f"""
        Using the information provided, improve my co-curricular activities section to make it more compelling and relevant to potential employers in my field, based on the provided job description. Use impactful words that align with the job description to enhance the appeal. Provide the improved version in the following JSON format, ensuring consistency and that each activity and its details are properly structured. Do not add any information that is not present.

        Job Description:
        {job_description}

        Co-Curricular Activities Section:
        {co_curricular_section}

        Requirements:
        - Highlight key accomplishments, leadership roles, or initiatives taken in these activities.
        - Emphasize relevant skills, experiences, or projects that align with the desired industry.
        - Showcase any awards, recognitions, or specific results achieved through these activities.
        - Output the improved co-curricular activities section in this JSON format:

        {{
          "co_curricular_activities": [
            {{
              "activity_name": "Activity Name",
              "details": [
                "Detail 1",
                "Detail 2",
                "Detail 3"
              ]
            }},
            {{
              "activity_name": "Another Activity Name",
              "details": [
                "Detail 1",
                "Detail 2",
                "Detail 3"
              ]
            }}
          ]
        }}

        Please provide only the JSON output as specified, without any additional text or explanations.
        """
        return prompt

    def create_resume_prompt_skills(self, job_description, skills_section):
        prompt = f"""
        Using the information provided, improve my skills section to make it more compelling and relevant to potential employers in my field, based on the provided job description. This section may include language skills, programming languages, frameworks, libraries, and technologies. Use impactful words that align with the job description to enhance the appeal. Provide the improved version in the following JSON format, ensuring consistency and proper categorization of each skill. Do not add any information that is not present.

        Job Description:
        {job_description}

        Skills Section:
        {skills_section}

        Requirements:
        - Extract and clearly categorize language skills, specifying proficiency levels (e.g., proficient, conversant).
        - Separate and categorize programming languages, frameworks, libraries, and other technologies.
        - Highlight the most relevant skills that match the job description, prioritizing those highly sought after in the desired industry.
        - Ensure the section is concise, impactful, and easy to read.
        - Output the improved skills section in this JSON format:
        {{
            "skills": {{
                "languages": [
                    "Language 1 Proficiency Level",
                    "Language 2 Proficiency Level"
                ],
                "programming_languages": [
                    "Programming Language 1",
                    "Programming Language 2"
                ],
                "frameworks_libraries": [
                    "Framework/Library 1",
                    "Framework/Library 2"
                ],
                "technologies": [
                    "Technology 1",
                    "Technology 2"
                ]
            }}
        }}

        Note: If a category does not apply, it can be omitted or left empty.
        Please provide only the JSON output as specified, without any additional text or explanations.
        """
        return prompt

    def create_resume_prompt_achievements_certifications(self, job_description, achievements_section):
        prompt = f"""
        Using the information provided, improve my achievements and certifications section to make it more compelling and relevant to potential employers in my field, based on the provided job description. Use impactful words that align with the job description to enhance the appeal. This section may include professional achievements, awards, certifications, and recognitions. Provide the improved version in the following JSON format, ensuring consistency and proper categorization of each entry. Do not add any information that is not present.

        Job Description:
        {job_description}

        Achievements and Certifications Section:
        {achievements_section}

        Requirements:
        - Clearly categorize professional achievements, awards, certifications, and recognitions.
        - Highlight the most relevant achievements and certifications that match the job description, prioritizing those highly sought after in the desired industry.
        - Ensure the section is concise, impactful, and easy to read.
        - Output the improved achievements and certifications section in this JSON format:

        {{
          "achievements_certifications": {{
            "achievements": [
              {{
                "title": "Achievement Title 1",
                "description": "Brief Description"
              }},
              {{
                "title": "Achievement Title 2",
                "description": "Brief Description"
              }}
            ],
            "certifications": [
              {{
                "name": "Certification Name 1",
                "issuing_organization": "Issuing Organization",
                "date_obtained": "Date Obtained"
              }},
              {{
                "name": "Certification Name 2",
                "issuing_organization": "Issuing Organization",
                "date_obtained": "Date Obtained"
              }}
            ]
          }}
        }}

        Note: If a category does not apply, it can be omitted or left empty.
        Please provide only the JSON output as specified, without any additional text or explanations.
        """
        return prompt

    def create_resume_prompt_hobbies(self, job_description, hobbies_section):
        prompt = f"""
        Using the information provided, improve my hobbies section to make it more compelling and relevant to potential employers in my field, based on the provided job description. Use impactful words that align with the job description to enhance the appeal. This section may include personal interests, hobbies, and extracurricular activities that showcase transferable skills or relevant attributes. Provide the improved version in the following JSON format, ensuring consistency and proper categorization of each entry. Do not add any information that is not present.

        Job Description:
        {job_description}

        Hobbies Section:
        {hobbies_section}

        Requirements:
        - Clearly categorize hobbies and personal interests, highlighting those that demonstrate relevant skills or qualities (e.g., teamwork, leadership, creativity).
        - Highlight the most relevant hobbies that match the job description, prioritizing those that align with the desired industry or job role.
        - Ensure the section is concise, engaging, and easy to read.
        - Output the improved hobbies section in this JSON format:

        {{
          "hobbies": [
            {{
              "hobby": "Hobby 1",
              "description": "Brief Description of how it relates to the job or relevant skills"
            }},
            {{
              "hobby": "Hobby 2",
              "description": "Brief Description of how it relates to the job or relevant skills"
            }}
          ]
        }}

        Note: If there are no relevant hobbies, you may omit the section or provide a minimal entry.
        Please provide only the JSON output as specified, without any additional text or explanations.
        """
        return prompt

