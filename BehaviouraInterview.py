import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
API_Key = os.getenv('API_Key')


client = Groq(
    api_key=API_Key,
)


def query_ollama(userResponse, prompt, conversationHistory):
    #Append the new prompt to the conversation history
    if userResponse not in ["","grade","feedback"]:
        conversationHistory.append(f"User response: {userResponse}\n")
    
    # Prepare the full prompt with history
    full_prompt = "".join(conversationHistory) + "AI:" + prompt

    # Define the command to call the ollama CLI
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": full_prompt ,
            }
        ],
        model="llama3-8b-8192",
    )
    
    # Capture and append the model's response to the conversation history
    airesponse = chat_completion.choices[0].message.content
    conversationHistory.append(f"AI response: {airesponse}\n")
    #print(conversationHistory)
    return airesponse, conversationHistory



def userInput(start, userResponse, conversationHistory): 
    gradeFormat = "overall score for interview: , reason for score: , strengths for interview: , weaknesses for interview: "
    feedbackFormat = "feedback for interview: , overall interview impression: , specific interview feedback: , actionable interview advice:"
    if userResponse is not None:
        userResponse = userResponse.strip()
    if start: # This will be executed when button is press, to generate a question -> once
        # prompt = f"Context: as an interviewer, generate 1 behavioural job interview question in JSON format. Just give me the content that is inside the triple backticks. In the format of: {airesponseFormat}. No further inner keys needed. No futher description needed."
        prompt = "(Provide a behavioural job interview question. Be concise and omit disclaimers, intro, quotes, any prefacing. Output solely the question. )"
        response, conversationHistory = query_ollama(userResponse, prompt, conversationHistory)
    else:
        # history use case
        if  userResponse == "grade": 
            if len(conversationHistory) > 5:
                prompt = f'(Please grade the interview and never consider resume or background. Be concise and omit disclaimers, intro, quotes, any prefacing. Output solely in the format of: {gradeFormat}'
                response, conversationHistory = query_ollama(userResponse,prompt, conversationHistory)
            else:
                response = "Please answer more questions before prompting grade.\nTo continue answer the previous question:\n" + conversationHistory[-1][13:]
        else:
            # userRespose = 'im unsure how to answer it'
            prompt = "(Generate a follow-up response based on the user's answer. If the response is less than a sentence, prompt for more detail. Be concise and omit disclaimers, intro, quotes, any prefacing. Acknowledge the user response and Output solely the question.)"
            response, conversationHistory = query_ollama(userResponse, prompt, conversationHistory)
        '''
        elif userResponse == "feedback":  
            if len(conversationHistory) > 5:
                prompt = f'(Please provide feedback on the interview and never consider  resume or background. Be concise and omit disclaimers, intro, quotes, any prefacing. Output solely in the format of: {feedbackFormat}'
                response, conversationHistory = query_ollama(userResponse, prompt, conversationHistory)    
            else:
                response = "Please answer more questions before prompting grade.\nTo continue answer the previous question:\n" + conversationHistory[-1][13:]
            # for any other respose
        '''
        
        
    return response, conversationHistory     

def main(jobTitle, resumeInfo):
    
    infoList = list(resumeInfo.keys())
    # Initial setup
    conversationHistory = []
    buttonPressed = True  # Assume the button is initially pressed
    inputAllowed = False   # Initially, input is not allowed
    initiate = 'Please conduct a mock interview with me with you as a professional interviewer. Focus solely on the question ONLY. Be concise and omit disclaimers or quotes.'
    backgroundInfo = f'( Background Info on User resume to generate question and response: An Interviewee applying for the role:{jobTitle}, based on resume details of interviewee:({infoList[1]}:{resumeInfo[infoList[1]]}, {infoList[2]}:{resumeInfo[infoList[2]]}, {infoList[3]}:{resumeInfo[infoList[3]]}, {infoList[4]}:{resumeInfo[infoList[4]]}, {infoList[6]}:{resumeInfo[infoList[6]]}) )'
    #InterViewerContext = f"( AI Role: )"
    conversationHistory.append(initiate)
    conversationHistory.append(backgroundInfo)
    #conversationHistory.append(InterViewerContext)

    userResponse = ''
    while True:
        if buttonPressed:
            aiResponse, conversationHistory = userInput(buttonPressed, userResponse, conversationHistory)
            buttonPressed = False  # Reset buttonPressed after handling
            inputAllowed = True     # Allow input after the first button press
        elif inputAllowed:
            userResponse = input("Enter your response: ")
            
            # Check for exit condition
            if userResponse.lower() in ['exit', 'quit']:
                print("Exiting...")
                break
            
            aiResponse, conversationHistory = userInput(buttonPressed, userResponse, conversationHistory)
   
        print(aiResponse)
        #i created an ai bot that does behavioural interview 1 on 1

if __name__ == "__main__":
    jobTitle = 'Full Stack Engineer'
    resumeInfo = {  
        "CONTACT": "Nobel Chua +65 9721 7297 | nobelchua@yahoo.com.sg | https://www.linkedin.com/in/nobelchua/",  
        "EDUCATION": "Nanyang Technological University, Singapore Aug 2021 â May 2025 Bachelor of Business (Business Analytics) and Bachelor of Engineering (Computer Science) â¢ CGPA Business: 3.95 â¢ CGPA Computer Science: 3.84 University of Groningen, Netherlands Jan 2024 â July 2024 Student Exchange Programme",  
        "ACADEMIC PROJECTS": "Rio Tinto, MSC Maritime Case Summit 2023 â 1st Runner Up Jan 2023 â Apr 2023 â¢ Invented a gamified approach to seafaring to foster interests in the field â¢ Engineered an innovative wearable device for open reporting, safeguarding seafarers' mental and physical well-being â¢ Developed an AR-based training program to facilitate the upskilling of seafarers â¢ Implemented a strategic, 3-pronged approach to attract and retain the next generation of maritime talent BHP, MSC Maritime Case Summit 2022 â 1st Runner Up Jan 2022 â Apr 2022 â¢ Conducted comprehensive analysis of leading decarbonization technologies and alternative fuels â¢ Engineered the design and retrofit plan for an electric-powered engine for maritime vessels â¢ Developed a long-term project plan with a 30-year forecast, accounting for technological advancements and market trends â¢ Performed cost estimation and profitability analysis to assess the financial viability of the implementation strategy",  
        "INTERN EXPERIENCE": "Goodie Technology, Business Development May 2022 â Aug 2022 â¢ Conducted thorough market research and identified 2 new product categories, driving innovation for the company â¢ Successfully launched the new categories, resulting in an 80% sales increase within 3 months â¢ Streamlined daily operations, boosting efficiency by 50% â¢ Established distribution partnerships with 3 companies, expanding both local and international market reach",  
        "WORK EXPERIENCE": "The Urban Hideout CafÃ©, Co-Founder May 2021 â Present â¢ Developed and standardized operating procedures (SOPs) for key business functions â¢ Analysed business operations to identify bottlenecks, leading to a 30% increase in efficiency â¢ Implemented SOPs improved daily operations and reduced manpower cost by 20% â¢ Establish and grew brand which achieved 100% ROI in 2 years Miyuki Izakaya, Co-Founder June 2022 â Present â¢ Developed a brand now operating in 2 locations across Singapore â¢ Led the hiring and training of a management team to effectively oversee on-ground staff â¢ Built a successful business achieving a 20% annual ROI â¢ Conducted market basket analysis to uncover consumer purchase patterns and drive sales â¢ Formulated a comprehensive business strategy to deliver high-quality Japanese cuisine to Singaporeâs heartland communities",  
        "CO-CURRICULAR ACTIVITIES": "NTU Hall of Residence 19 (Binjai Hall) Business Manager, Freshman Orientation Programme 2022 Aug 2021 â Aug 2022 â¢ Negotiated sponsorship deals with various companies, securing cash and product sponsors for over 200 freshmen â¢ Successfully obtained sponsorships to support freshmen events and activities â¢ Led and delegated tasks to committee members, ensuring smooth execution of responsibilities â¢ Volunteered to facilitate games and activities for incoming freshmen during a 3-day event NTU School of Computer Science and Engineering Chief Programmer, Freshmen Transition Orientation Program 2022 Aug 2021 â Aug 2022 â¢ Planned and organized games for approximately 800 incoming freshmen, creating an engaging orientation experience â¢ Facilitated a smooth transition into university life for new students â¢ Collaborated with key stakeholders to structure and execute the event effectively â¢ Optimised logistics and equipment management for a 3-day event, ensuring seamless operations",  
        "SKILLS": "Languages: English (Native), Mandarin (Fluent) Software Skills: Python, R, C, Java, HTML, Flask, SQL, MongoDB, PowerBI"  
    }
    main(jobTitle, resumeInfo)