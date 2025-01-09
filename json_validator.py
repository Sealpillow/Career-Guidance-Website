import json

class JSONValidator:

    @staticmethod
    def is_valid_education_format(data):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            if 'education' not in data or not isinstance(data['education'], list):
                return False
            for entry in data['education']:
                if not isinstance(entry, dict):
                    return False
                if 'university' not in entry or not isinstance(entry['university'], str):
                    return False
                if 'details' not in entry or not isinstance(entry['details'], list):
                    return False
                if not all(isinstance(detail, str) for detail in entry['details']):
                    return False
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_valid_projects_format(data):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            if 'projects' not in data or not isinstance(data['projects'], list):
                return False
            for entry in data['projects']:
                if not isinstance(entry, dict):
                    return False
                if 'project_title' not in entry or not isinstance(entry['project_title'], str):
                    return False
                if 'details' not in entry or not isinstance(entry['details'], list):
                    return False
                if not all(isinstance(detail, str) for detail in entry['details']):
                    return False
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_valid_experience_format(data):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            if 'experience' not in data or not isinstance(data['experience'], list):
                return False
            for entry in data['experience']:
                if not isinstance(entry, dict):
                    return False
                if 'position_title' not in entry or not isinstance(entry['position_title'], str):
                    return False
                if 'company' not in entry or not isinstance(entry['company'], str):
                    return False
                if 'details' not in entry or not isinstance(entry['details'], list):
                    return False
                if not all(isinstance(detail, str) for detail in entry['details']):
                    return False
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_valid_co_curricular_activities_format(data):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            if 'co_curricular_activities' not in data or not isinstance(data['co_curricular_activities'], list):
                return False
            for entry in data['co_curricular_activities']:
                if not isinstance(entry, dict):
                    return False
                if 'activity_name' not in entry or not isinstance(entry['activity_name'], str):
                    return False
                if 'details' not in entry or not isinstance(entry['details'], list):
                    return False
                if not all(isinstance(detail, str) for detail in entry['details']):
                    return False
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_valid_skills_format(data):
        try:
            if isinstance(data, str):
                data = json.loads(data)

            # Check for 'skills' key and ensure it is a dictionary
            if 'skills' not in data or not isinstance(data['skills'], dict):
                return False

            # Validate 'languages' field (should be a list of strings)
            if 'languages' not in data['skills'] or not isinstance(data['skills']['languages'], list):
                return False
            if not all(isinstance(lang, str) and ' ' in lang for lang in data['skills']['languages']):
                return False
        
            # Validate 'programming_languages' field (should be a list of strings)
            if 'programming_languages' not in data['skills'] or not isinstance(data['skills']['programming_languages'], list):
                return False
            if not all(isinstance(lang, str) for lang in data['skills']['programming_languages']):
                return False
        
            # Validate 'frameworks_libraries' field (should be a list of strings)
            if 'frameworks_libraries' not in data['skills'] or not isinstance(data['skills']['frameworks_libraries'], list):
                return False
            if not all(isinstance(framework, str) for framework in data['skills']['frameworks_libraries']):
                return False
        
            # Validate 'technologies' field (should be a list of strings)
            if 'technologies' not in data['skills'] or not isinstance(data['skills']['technologies'], list):
                return False
            if not all(isinstance(tech, str) for tech in data['skills']['technologies']):
                return False
        
            return True
        except (json.JSONDecodeError, TypeError):
           return False


    @staticmethod
    def is_valid_achievements_certifications_format(data):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            
            if 'achievements_certifications' not in data or not isinstance(data['achievements_certifications'], dict):
                return False
            
            if 'achievements' not in data['achievements_certifications'] or not isinstance(data['achievements_certifications']['achievements'], list):
                return False
            for achievement in data['achievements_certifications']['achievements']:
                if not isinstance(achievement, dict):
                    return False
                if 'title' not in achievement or not isinstance(achievement['title'], str):
                    return False
                if 'description' not in achievement or not isinstance(achievement['description'], str):
                    return False
            
            if 'certifications' not in data['achievements_certifications'] or not isinstance(data['achievements_certifications']['certifications'], list):
                return False
            for certification in data['achievements_certifications']['certifications']:
                if not isinstance(certification, dict):
                    return False
                if 'name' not in certification or not isinstance(certification['name'], str):
                    return False
                if 'issuing_organization' not in certification or not isinstance(certification['issuing_organization'], str):
                    return False
                if 'date_obtained' not in certification or not isinstance(certification['date_obtained'], str):
                    return False
            
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def is_valid_hobbies_format(data):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            
            if 'hobbies' not in data or not isinstance(data['hobbies'], list):
                return False
            
            for hobby in data['hobbies']:
                if not isinstance(hobby, dict):
                    return False
                if 'hobby' not in hobby or not isinstance(hobby['hobby'], str):
                    return False
                if 'description' not in hobby or not isinstance(hobby['description'], str):
                    return False
            
            return True
        except (json.JSONDecodeError, TypeError):
            return False


