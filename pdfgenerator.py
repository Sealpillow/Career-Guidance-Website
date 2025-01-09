from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PDFGenerator:
    def __init__(self, json_data, pdf_filename):
        self.json_data = json_data or {}  # Ensure json_data is a dictionary, even if None
        self.pdf_filename = pdf_filename
        self.doc = SimpleDocTemplate(pdf_filename, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        self.styles = getSampleStyleSheet()

        # Define custom styles
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Heading1'],
            fontSize=20,
            leading=24,
            alignment=1,  # Centered
            spaceAfter=10
        )
        
        self.contact_style = ParagraphStyle(
            'Contact',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=12,
            textColor=colors.HexColor('#003366'),
            alignment=1,  # Centered
            spaceAfter=8
        )
        
        self.section_style = ParagraphStyle(
            'Section',
            parent=self.styles['Heading2'],
            fontSize=12,
            leading=14,
            textColor=colors.HexColor('#003366'),
            spaceBefore=8,
            spaceAfter=5
        )

        self.normal_style = ParagraphStyle(
            'Normal',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11
        )

        self.bullet_style = ParagraphStyle(
            'Bullet',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            leftIndent=15
        )

        self.bold_style = ParagraphStyle(
            'Bold',
            parent=self.styles['Normal'],
            fontSize=9,
            leading=11,
            leftIndent=0,
            spaceAfter=4,
            textColor=colors.black
        )
        self.bold_style.fontName = 'Helvetica-Bold'

        self.story = []

    def add_contact_info(self):
        contact_info = self.json_data.get('contact', None)
        if contact_info:
            self.story.append(Paragraph(contact_info, self.contact_style))

    def add_education_section(self):
        education_section = self.json_data.get('education', None)
        if isinstance(education_section, dict) and isinstance(education_section.get('education', []), list):
            self.story.append(Paragraph("EDUCATION", self.section_style))
            for edu in education_section['education']:
                university = edu.get('university', '')
                self.story.append(Paragraph(f"<b>{university}</b>", self.bold_style))
                for detail in edu.get('details', []):
                    fixed_detail = detail.replace('â', '–')  # Correct for em-dashes
                    self.story.append(Paragraph(f"• {fixed_detail}", self.bullet_style))
            self.story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor('#003366')))

    def add_projects_section(self):
        projects_section = self.json_data.get('projects', None)
        if isinstance(projects_section, dict) and isinstance(projects_section.get('projects', []), list):
            self.story.append(Paragraph("ACADEMIC PROJECTS", self.section_style))
            for project in projects_section['projects']:
                project_title = project.get('project_title', '')
                self.story.append(Paragraph(f"<b>{project_title}</b>", self.bold_style))
                for detail in project.get('details', []):
                    self.story.append(Paragraph(f"• {detail}", self.bullet_style))
            self.story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor('#003366')))

    def add_experience_section(self):
        experience_section = self.json_data.get('experience', None)
        if isinstance(experience_section, dict) and isinstance(experience_section.get('experience', []), list):
            self.story.append(Paragraph("INTERN EXPERIENCE", self.section_style))
            for exp in experience_section['experience']:
                position_title = exp.get('position_title', '')
                company = exp.get('company', '')
                self.story.append(Paragraph(f"<b>{position_title} at {company}</b>", self.bold_style))
                for detail in exp.get('details', []):
                    self.story.append(Paragraph(f"• {detail}", self.bullet_style))
            self.story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor('#003366')))

    def add_co_curricular_section(self):
        co_curricular_section = self.json_data.get('co_curricular', None)
        if isinstance(co_curricular_section, dict) and isinstance(co_curricular_section.get('co_curricular_activities', []), list):
            self.story.append(Paragraph("CO-CURRICULAR ACTIVITIES", self.section_style))
            for activity in co_curricular_section['co_curricular_activities']:
                activity_name = activity.get('activity_name', '')
                self.story.append(Paragraph(f"<b>{activity_name}</b>", self.bold_style))
                for detail in activity.get('details', []):
                    self.story.append(Paragraph(f"• {detail}", self.bullet_style))
            self.story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor('#003366')))

    def add_skills_section(self):
        skills_section = self.json_data.get('skills', None)
        if isinstance(skills_section, dict) and isinstance(skills_section.get('skills', {}), dict):
            skills = skills_section['skills']
            self.story.append(Paragraph("SKILLS", self.section_style))

            # Check and append each skill category
            if 'languages' in skills and skills['languages']:
                # Highlight the category "Language Skills"
                self.story.append(Paragraph("Language Skills:", self.bold_style))
                # Append the actual skills in normal style
                self.story.append(Paragraph(", ".join(skills['languages']), self.normal_style))
                self.story.append(Spacer(1, 6))

            if 'programming_languages' in skills and skills['programming_languages']:
                # Highlight the category "Programming Languages"
                self.story.append(Paragraph("Programming Languages:", self.bold_style))
                # Append the actual skills in normal style
                self.story.append(Paragraph(", ".join(skills['programming_languages']), self.normal_style))
                self.story.append(Spacer(1, 6))

            if 'frameworks_libraries' in skills and skills['frameworks_libraries']:
                # Highlight the category "Frameworks & Libraries"
                self.story.append(Paragraph("Frameworks & Libraries:", self.bold_style))
                # Append the actual skills in normal style
                self.story.append(Paragraph(", ".join(skills['frameworks_libraries']), self.normal_style))
                self.story.append(Spacer(1, 6))

            if 'technologies' in skills and skills['technologies']:
                # Highlight the category "Technologies"
                self.story.append(Paragraph("Technologies:", self.bold_style))
                # Append the actual skills in normal style
                self.story.append(Paragraph(", ".join(skills['technologies']), self.normal_style))
                self.story.append(Spacer(1, 6))

            # Add a horizontal rule (HRFlowable) after the skills section
            self.story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor('#003366')))

    def add_achievements_section(self):
        achievements_section = self.json_data.get('achievements', None)
        if isinstance(achievements_section, dict) and isinstance(achievements_section.get('achievements_certifications', {}), dict):
            achievements = achievements_section['achievements_certifications']
            self.story.append(Paragraph("ACHIEVEMENTS & CERTIFICATIONS", self.section_style))

            if isinstance(achievements.get('achievements', []), list):
                for achievement in achievements['achievements']:
                    self.story.append(Paragraph(f"<b>{achievement.get('title', '')}</b>", self.bold_style))
                    self.story.append(Paragraph(f"{achievement.get('description', '')}", self.normal_style))
            
            if isinstance(achievements.get('certifications', []), list):
                for cert in achievements['certifications']:
                    self.story.append(Paragraph(f"<b>{cert.get('name', '')}</b> - {cert.get('issuing_organization', '')} ({cert.get('date_obtained', '')})", self.bold_style))
            
            self.story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor('#003366')))

    def add_interests_section(self):
        interests_section = self.json_data.get('interests', None)
        if isinstance(interests_section, dict) and isinstance(interests_section.get('hobbies', []), list):
            self.story.append(Paragraph("INTERESTS", self.section_style))
            for hobby in interests_section['hobbies']:
                self.story.append(Paragraph(f"<b>{hobby.get('hobby', '')}</b>", self.bold_style))
                self.story.append(Paragraph(f"{hobby.get('description', '')}", self.normal_style))
            self.story.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.HexColor('#003366')))

    def build_pdf(self):
        self.add_contact_info()
        self.add_education_section()
        self.add_projects_section()
        self.add_experience_section()
        self.add_co_curricular_section()
        self.add_skills_section()
        self.add_achievements_section()
        self.add_interests_section()
        
        # Build the PDF document
        self.doc.build(self.story)

