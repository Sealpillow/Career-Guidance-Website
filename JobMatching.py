import os
import json
import csv
from vectordb_manager import VectorDBManager
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

# Set up Groq API key
API_Key = os.getenv('API_Key')
# Initialize ChatGroq model
model = ChatGroq(model="llama3-8b-8192", api_key= API_Key)
current_dir = os.path.dirname(os.path.abspath(__file__))



def init_vectordb():
    return VectorDBManager()

vectordb_manager = init_vectordb()

def load_skills_json(skillPath):
    if os.path.exists(skillPath):
        with open(skillPath, 'r') as f:
            return json.load(f)
    return {}

def save_skills_json(skills_dict, skillPath):
    with open(skillPath, 'w') as f:
        json.dump(skills_dict, f)

def get_job_skills(job_id, job_description, skillPath):
    skills_dict = load_skills_json(skillPath)
    
    if job_id in skills_dict:
        print("READING FROM CACHE")
        return skills_dict[job_id]
    else:
        print("PROMPTING LLM")
        prompt = f"Extract key words or soft/hard skills needed for this job description. Limit to maximum 10 skills with a mixture of soft and hard skills. Please provide a comma-separated list of skills. DO NOT output anything else other than the list of skills:\n\n{job_description}"
        response = model.invoke([HumanMessage(content=prompt)])
        
        skills_text = response.content.split(':')[-1].strip()
        skills = [skill.strip() for skill in skills_text.split(',')][:10]
        
        skills_dict[job_id] = skills
        save_skills_json(skills_dict, skillPath)
        
        return skills

def sort_jobs(results, sort_by='confidence'):
    if sort_by == 'confidence':
        return sorted(results, key=lambda x: x[1], reverse=True)
    elif sort_by == 'company':
        return sorted(results, key=lambda x: x[0].metadata['company_name'].lower())
    elif sort_by == 'date':
        return sorted(results, key=lambda x: int(x[0].metadata['job_id']), reverse=True)
    else:
        return results

def read_skills_from_json(resume_json_path):
    with open(resume_json_path, 'r') as f:
        resume_data = json.load(f)
    return resume_data.get("SKILLS", "")

def save_results_to_json(results, jsonPath, skillPath):
    output = []
    for doc, score in results:
        metadata = doc.metadata
        job_id = metadata['job_id']
        skills_required = get_job_skills(job_id, doc.page_content, skillPath)
        output.append({
            "company_name": metadata['company_name'],
            "job_title": metadata['title'],
            "location": metadata['location'],
            "job_posting_url": metadata['job_posting_url'],
            "description": doc.page_content,
            "skills_required": skills_required,
            "job_id": job_id,
            "confidence_score": f"{score:.4f}"
        })
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(jsonPath), exist_ok=True)
        
        # Write the JSON file, overwriting any existing content
        with open(jsonPath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Results successfully saved to {jsonPath}")
        return output
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def save_results_to_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ["company_name", "job_title", "location", "job_posting_url", "description", "skills_required", "job_id", "confidence_score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        try:
            writer.writeheader()
            for result in results:
                result['skills_required'] = ', '.join(result['skills_required'])
                writer.writerow(result)
        except Exception as e:
            print(f"Error while writing CSV data: {str(e)}")

def main(profileName, sort_order):
    print(sort_order)
    confidence_threshold = 0.8
    # Path to the JSON file storing job skills
    resume_json_path = os.path.join(current_dir, f'json/{profileName}_resume.json')
    skills_json_path = os.path.join(current_dir, f'downloads/{profileName}_job_skills.json')
    results_json_path = os.path.join(current_dir, f'downloads/{profileName}_matching_jobs_results.json')
    results_csv_path = os.path.join(current_dir, f'downloads/{profileName}_matching_jobs_results.csv')
    skills_input = read_skills_from_json(resume_json_path)
    if skills_input:
        results = vectordb_manager.similarity_search(query=skills_input, score_threshold=confidence_threshold)
        sorted_results = sort_jobs(results, sort_order)
        json_results = save_results_to_json(sorted_results, results_json_path, skills_json_path)
        save_results_to_csv(json_results, results_csv_path)
        print(f"Results saved to {results_json_path} and {results_csv_path}")
    else:
        print(f"No skills found in the resume JSON file: {resume_json_path}")

if __name__ == "__main__":
    # Example usage with default parameters
    name = 'nobel'
    sort_order = 'confidence'
    main(name, sort_order)
    
    # Example usage with custom parameters
    # main(confidence_threshold=0.7, resume_json_path="./custom_resume.json", sort_order='company')