import json
from groq import Groq 
class LLM_Skills:
    
    def __init__(self, api_key):
        # Initialize Groq client with the provided API key
        self.client = Groq(api_key=api_key)

    def generate_response(self, content):
        attempts = 0
        max_attempts = 5
        
        while attempts < max_attempts:
            try:
                # Use the Groq client to make a chat completion request
                chat_completion = self.client.chat.completions.create(
                    model="llama3-8b-8192",  # Specify the correct model
                    messages=[
                        {
                            "role": "user",
                            "content": f"Using the following JSON: {content}, generate three technical skills and three soft skills. Return only the following JSON and nothing else: {{ \"SKILLS\": {{ \"Soft Skills\": [\"soft skill 1\", \"soft skill 2\", \"soft skill 3\"], \"Technical Skills\": [\"technical skill 1\", \"technical skill 2\", \"technical skill 3\"] }} }}. Do not provide any explanations, comments, or additional text outside the JSON structure."
                        }
                    ]
                )
                
                # Parse the response
                parsed_response = chat_completion.choices[0].message.content
                
                # Attempt to load and validate the JSON structure
                json_response = json.loads(parsed_response)
                
                # Validate that the required keys are present
                if "SKILLS" in json_response and "Soft Skills" in json_response["SKILLS"] and "Technical Skills" in json_response["SKILLS"]:
                    # If the JSON structure is valid, return it
                    return json_response
                else:
                    raise ValueError("Invalid JSON structure")
            
            except (json.JSONDecodeError, ValueError):
                # If parsing fails, increment the attempt counter
                attempts += 1
                print(f"Attempt {attempts} failed. Retrying...")
        
        # If all attempts fail, raise an exception or return a default response
        raise Exception("Failed to generate valid JSON after 5 attempts")

    def update_json_with_skills(self, original_json, new_skills_json):
        try:
            # Ensure original JSON is properly loaded
            if isinstance(original_json, str):
                original_json = json.loads(original_json)
            
            # Update the SKILLS section of the original JSON
            original_json['SKILLS'] = new_skills_json['SKILLS']
            
            # Return the updated JSON
            return original_json
        
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error updating JSON: {e}")
            return None

    def export_to_json(self, updated_json, filename):
        try:
            # Save the updated JSON to a file
            with open(filename, 'w') as json_file:
                json.dump(updated_json, json_file, indent=4)
            print(f"Updated resume exported to {filename}")
        except IOError as e:
            print(f"Error saving JSON to file: {e}")