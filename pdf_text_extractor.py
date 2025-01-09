import fitz  # PyMuPDF
import re
import json

class PDFTextExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)
        self.text = self._extract_text()
        self.cleaned_text = self.clean_text(self.text)
        self.keyword_indices = {}
        self.extended_mapping = {
            "CONTACT": ["CONTACT"],
            "EDUCATION": ["EDUCATION"],
            "PROJECTS": ["PROJECTS", "ACADEMIC PROJECTS"],
            "intern_experience_section": ["INTERNSHIP EXPERIENCE", "EXPERIENCES", "INTERN EXPERIENCE", "WORK EXPERIENCE", "EXPERIENCE"],
            "CCA": ["CCA", "CO-CURRICULAR ACTIVITIES", "ACTIVITIES"],
            "SKILLS": ["SKILLS"],
            "ACHIEVEMENT": ["ACHIEVEMENT", "AWARDS AND ACHIEVEMENTS", "ACHIEVEMENTS", "CERTIFICATIONS"],
            "INTEREST": ["INTEREST", "HOBBIES & INTERESTS", "INTERESTS"]
        }
        self.keywords = [keyword for sublist in self.extended_mapping.values() for keyword in sublist]

    def _extract_text(self):
        """Extract text from all the pages in the PDF."""
        text = ""
        for page_num in range(len(self.doc)):
            page = self.doc.load_page(page_num)
            text += page.get_text()
        return text

    @staticmethod
    def clean_text(text):
        """Clean the extracted text."""
        # Remove non-ASCII characters and reduce multiple spaces/tabs/newlines
        text = text.encode('ascii', errors='ignore').decode()
        text = re.sub(r'\s+', ' ', text)
        return text

    def find_keyword_indices(self):
        """Find the indices of all keywords in the cleaned text."""
        for keyword in self.keywords:
            matches = list(re.finditer(r'\b' + re.escape(keyword) + r'\b', self.cleaned_text))
            if matches:
                self.keyword_indices[keyword] = [match.start() for match in matches]

    def extract_extended_sections(self):
        """Extract sections of the PDF based on keyword mappings."""
        extracted = {key: None for key in self.extended_mapping}  # Initialize all sections as null

        # Handle CONTACT section as everything before EDUCATION
        if "EDUCATION" in self.keyword_indices:
            education_start = self.keyword_indices["EDUCATION"][0]
            extracted["CONTACT"] = self.cleaned_text[:education_start].strip()  # Everything before EDUCATION is CONTACT

        # Process the rest of the sections
        for key, keywords in self.extended_mapping.items():
            if key == "CONTACT":
                continue  # Skip CONTACT, already handled
            
            start_index = None

            # Find the earliest occurrence of any keyword in the category
            for keyword in keywords:
                if keyword in self.keyword_indices:
                    start_index = self.keyword_indices[keyword][0]
                    break

            if start_index is None:
                continue  # Skip if no keyword is found in this category

            # Find the nearest next keyword's index to define the section's end
            end_indices = []
            for next_key, next_keywords in self.extended_mapping.items():
                if next_key != key:
                    for next_keyword in next_keywords:
                        if next_keyword in self.keyword_indices:
                            # Get all indices greater than start_index
                            next_indices = [idx for idx in self.keyword_indices[next_keyword] if idx > start_index]
                            end_indices.extend(next_indices)

            # Determine the smallest index among candidates
            end_index = min(end_indices) if end_indices else None

            # Extract the section from the current keyword to the next keyword
            section_text = self.cleaned_text[start_index:end_index].strip() if end_index else self.cleaned_text[start_index:].strip()

            if section_text:
                extracted[key] = section_text  # Only replace if non-empty content is found

        return extracted

    def extract_to_json(self):
        """Main function to run the entire extraction process and return the JSON structure."""
        self.find_keyword_indices()
        extracted_data = self.extract_extended_sections()
        return json.dumps(extracted_data, indent=4)






