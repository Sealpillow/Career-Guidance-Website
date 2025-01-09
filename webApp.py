#from pdf_text_extractor import PDFTextExtractor
#from resume_generator import ResumeGenerator
#from pdfgenerator import PDFGenerator
import json
from flask import Flask, render_template, request, redirect, url_for, make_response, send_from_directory,  session, flash, send_file
from flask import request
import json
from functools import wraps
from pdf_text_extractor import PDFTextExtractor
import ResumeFixing 
import BehaviouraInterview
import LeetCodeGenerator
import JobMatching
import os
import pandas as pd
from waitress import serve
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(current_dir, 'uploads/')
DOWNLOAD_FOLDER = os.path.join(current_dir, 'downloads/')
JOB_RESULTS_JSON  = os.path.join(current_dir, 'matching_jobs_results.json')
JOB_RESULTS_CSV  = os.path.join(current_dir, 'matching_jobs_results.csv')


app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JOB_RESULTS_JSON'] = JOB_RESULTS_JSON
app.config['JOB_RESULTS_CSV'] = JOB_RESULTS_CSV
app.secret_key = 'your_secret_key'  # Required for session management

# Generic/Helper function------------------------------------------------------------------------------
# Function to load users from the JSON file
def load_users():
    try:
        with open('users.json') as f:
            data = json.load(f)
        return {user['username']: user for user in data['users']}
    except FileNotFoundError:
        return {}

def get_user_session_data():
    if "username" in session:
        users = load_users()
        if session['username'] in users:
            return users[session['username']]
    return None

# Function to save a new user to the JSON file
def save_user(username, password, email, name=None, age=None, contact=None):
    try:
        with open('users.json', 'r+') as f:
            data = json.load(f)
            user_data = {'username': username, 'password': password, 'email': email}
            if name and age and contact:
                user_data.update({'name': name, 'age': age, 'contact': contact})
            else:
                user_data.update({'name': None, 'age': None, 'contact': None})
            data['users'].append(user_data)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except FileNotFoundError:
        with open('users.json', 'w') as f:
            json.dump({'users': [{'username': username, 'password': password, 'email': email, 'name': name, 'age': age, 'contact': contact}]}, f, indent=4)

def save_all_users(users):
    with open('users.json', 'w') as f:
        json.dump({'users': list(users.values())}, f, indent=4)


def read_resume_from_json(profileName):
    resume_json_path = os.path.join(current_dir, f'json/{profileName}_resume.json')
    with open(resume_json_path, 'r') as f:
        resume_data = json.load(f)
    return resume_data

def redirectLogin():
    # MAKE THIS GENERIC
    current_User = get_user_session_data()
    if(current_User is None):
        print("NON user")
        return redirect(url_for('login'))
    return None

def read_skills_from_json(resume_json_path):
    with open(resume_json_path, 'r') as f:
        resume_data = json.load(f)
    return resume_data.get("SKILLS", "")

# ROUTES------------------------------------------------------------------------------ #
# Home Route
@app.route('/', methods=['GET', 'POST'])
def landing():
    error_message = None
    current_User = get_user_session_data()
    print(current_User)
    if(current_User != None):
        return render_template('main.html', username= current_User['username'])

    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = ''
    users = load_users()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('landing')) 
        else:
            error_message = "Invalid username or password."
    
    return render_template('login.html', error_message= error_message)

# Logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('landing'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_message = ''

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        users = load_users()
        if username in users:
            error_message = "Username already exists." # ?
        else:
            save_user(username, password, email)
            session['username'] = username
            return redirect(url_for('profile')) # after sign up, user should go to profile

    return render_template('signup.html', error_message=error_message)

# Profile route
@app.route('/profile', methods=['GET'])
def profile():

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    username = session['username']
    current_User = get_user_session_data()
    
    session['currRoute'] = 'resume'
    profileName = session['username']
    new_filename = f"{profileName}_resume.pdf" 
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
    filename = None
    if os.path.isfile(file_path):
        filename = new_filename
    print(filename)

    message = request.args.get('popUpMessage')  # Retrieve the query parameter

    return render_template('profile.html', username=username, email=current_User['email'],\
        name = current_User["name"], age = current_User["age"], contact = current_User["contact"],\
        filename = filename, popUpMessage=message)

@app.route('/updateProfile', methods=['GET', 'POST'])
def updateProfile():

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    username = session['username']
    users = load_users()
    
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        contact = request.form.get('contact')

        # Update user data in the JSON
        if username in users:
            users[username].update({'name': name, 'age': age, 'contact': contact})
            save_all_users(users)

        return redirect(url_for('profile'))  # Redirect to the same profile page to show updated info

    return render_template('updateProfile.html')

# ResumeFixing
# Behavioural Interview Routes    
@app.route('/improveResume', methods=["GET", "POST"])
def improveResume():    

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    profileName = session['username']
    improvedResumeName = f'{profileName}_improved_resume.pdf'
    job_description = request.form.get('job_description')
    ResumeFixing.main(job_description, profileName)
    return redirect(url_for('generateImprovedResume', fileName = improvedResumeName))


@app.route("/generateImprovedResume", methods=["GET", "POST"])
def generateImprovedResume():

    redirectLogin()

    fileName = request.args.get('fileName')
    message = request.args.get('popUpMessage')
    session['currRoute'] = 'generateImprovedResume'
    print("Filename here: "  +fileName)
    return render_template('resume_generate.html', filename = fileName, popUpMessage=message)
    

# Job Matching Routes # required 
@app.route("/jobMatching", methods=["GET", "POST"])
def jobMatching():

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    session['currRoute'] = 'jobMatching'
    profileName = session['username']

    if request.method == 'POST':
        selected_option = request.form.get('dropdown')
        session['dropdown'] = selected_option
        if selected_option == 'confidence':
            JobMatching.main(profileName, 'confidence')
        elif selected_option == 'company':
            JobMatching.main(profileName, 'company')
        elif selected_option == 'date':   
            JobMatching.main(profileName, 'date')  
        
        jsonFilename=f'{profileName}_matching_jobs_results.json'
        csvFilename=f'{profileName}_matching_jobs_results.csv'

        session["jobs_jsonFilename"] = jsonFilename
        session["jobs_csvFilename"] = csvFilename

    # Redirect so that we can keep data when back
    return redirect(url_for('jobMatchingRedirect'))

@app.route('/jobMatch')
def jobMatchingRedirect():

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    jobs = None
    jsonFilename = None
    csvFilename = None

    dropdown_options = [
        {'value': 'confidence', 'label': 'Confidence'},
        {'value': 'company', 'label': 'Company'},
        {'value': 'date', 'label': 'Date'},
    ]
    
    profileName = session['username']
    resume_json_path = os.path.join(current_dir, f'json/{profileName}_resume.json')
    resume_exist = False
    if os.path.isfile(resume_json_path):
        resume_exist = True
        skills_input = read_skills_from_json(resume_json_path)

    if("jobs_jsonFilename" in session):

        jsonFilename = session["jobs_jsonFilename"] 
        csvFilename = session["jobs_csvFilename"]
        filePath = os.path.join(current_dir, f'downloads/{jsonFilename}') 
        with open(filePath, 'r', encoding='utf-8') as jobs_file:
            jobs = json.load(jobs_file)   
    
        return render_template('jobMatching.html', user_skills= skills_input, resume_exist = True, jobs = jobs, jsonFilename=jsonFilename,csvFilename= csvFilename,options=dropdown_options)
    
    elif(resume_exist == True):

        return render_template('jobMatching.html', user_skills= None, resume_exist = True, jobs = jobs, jsonFilename=jsonFilename,csvFilename= csvFilename,options=dropdown_options)
    
    return render_template('jobMatching.html', user_skills= None, resume_exist = False, jobs = jobs, jsonFilename=jsonFilename,csvFilename= csvFilename,options=dropdown_options)


# Behavioural Interview Routes    
@app.route('/startChat/<string:jobTitle>')
def startChat(jobTitle):
    
    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    profileName = session['username']
    
    resumeInfo = read_resume_from_json(profileName)
    infoList = list(resumeInfo.keys())
    # every time the user start chat, history refreshes
    initiate = 'Please conduct a mock interview with me with you as a professional interviewer. Focus solely on the question ONLY. Be concise and omit disclaimers or quotes.'
    backgroundInfo = f'( Background Info on User resume to generate question and response: An Interviewee applying for the role:{jobTitle}, based on resume details of interviewee:({infoList[1]}:{resumeInfo[infoList[1]]}, {infoList[2]}:{resumeInfo[infoList[2]]}, {infoList[3]}:{resumeInfo[infoList[3]]}, {infoList[4]}:{resumeInfo[infoList[4]]}, {infoList[6]}:{resumeInfo[infoList[6]]}) )'
    #InterViewerContext = f"( AI Role: )"
    session['chat_history'] = []
    session['overal_context'] = []
    session['overal_context'].append(initiate)
    session['overal_context'].append(backgroundInfo)
    session['chat_status'] = 'start'
    session.modified = True  # Mark session as modified * important
    return redirect(url_for('chat'))


@app.route('/chat', methods=['GET','POST'])
def chat():

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    # Initial setup
    session['currRoute'] = 'chat'
    if session['chat_status'] == 'start':
        user_message = ''
        aiResponse, session['overal_context'] = BehaviouraInterview.userInput(True, user_message, session['overal_context'])
        session['chat_status'] = "in progress"
    else:
        user_message = request.form.get('message')
        aiResponse, session['overal_context'] = BehaviouraInterview.userInput(False, user_message, session['overal_context'])
    session['chat_history'].append({'user': user_message, 'bot': aiResponse})
    session.modified = True  # Mark session as modified * important
    return render_template('behavioural.html', chat_history=session['chat_history']) 



# LeetCode Routes
@app.route('/leetCode', methods=['GET','POST'])
def leetCode():

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    session['currRoute'] = 'leetcode'
    # Initial setup
    inputJob = request.args.get('inputJob')

    filePath = os.path.join(current_dir, f'downloads/SelectedQns.json')
    f = open(filePath)
    baseQns = json.load(f)
    # Initialize session keys if they do not exist
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'regenerate':
            print(inputJob)
            return redirect(url_for('generateLeetCode', jobTitle= inputJob))
    # Transforming to a list of dictionaries
    
    questions_list = []
    for i in range(len(baseQns['title'])):
        question = {
            'title': baseQns['title'][str(i)],
            'titleSlug': baseQns['titleSlug'][str(i)],
            'difficulty': baseQns['difficulty'][str(i)],
            'url': baseQns['url'][str(i)],
            'topicTags': baseQns['topicTags'][str(i)].split(', ')  # Split tags into a list
        }
        questions_list.append(question)
    return render_template('leetcode.html', inputJob = inputJob, outputQns=questions_list, csvFileName='SelectedQns.csv',excelFileName = 'SelectedQns.xlsx')


@app.route('/generateLeetCode/<string:jobTitle>')
def generateLeetCode(jobTitle):

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    # Initial setup
    inputJob = jobTitle
    baseQns, categoryTags = LeetCodeGenerator.generateQuestionByJobTitle(inputJob)
    baseQns, categoryTags = LeetCodeGenerator.generateNRandomForEachDif(pd.DataFrame(json.loads(baseQns)), categoryTags, 5)
    session.modified = True  # Mark session as modified * important
    return redirect(url_for('leetCode', inputJob= inputJob))


@app.route("/uploadResume", methods=["GET", "POST"])
def uploadResume():

    redirect_response = redirectLogin()
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        profileName = session['username']
        if session['currRoute'] == 'generateImprovedResume':
            
            fileName = f"{profileName}_improved_resume.pdf"
            filePath = os.path.join(current_dir, f'downloads/{fileName}')
            file = FileStorage(open(filePath, 'rb'))

            new_filename = f"{profileName}_resume.pdf"  
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(pdf_path)
            profileName = 'nobel' # profileName
            # retrieve the uploaded PDF file path
            ResumeFixing.saveResumeJson(pdf_path, profileName)
            flash('Upload successfully!', 'success')  # Flash a message
            return redirect(url_for('generateImprovedResume', fileName = fileName, popUpMessage='Upload successfully!'))
        else:
            if 'file' not in request.files:
                return redirect(url_for('profile',  error='No file part'))

            file = request.files['file']

            if file.filename == '':
                return redirect(url_for('profile',  error='No selected file'))

            if file and file.filename.endswith('.pdf'):
                new_filename = f"{profileName}_resume.pdf"  
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                file.save(pdf_path)
                ResumeFixing.saveResumeJson(pdf_path, profileName)
                flash('Upload successfully!', 'success')  # Flash a message
                return redirect(url_for('profile', popUpMessage='Upload successfully!'))

    return redirect(url_for('profile'))

@app.route('/backToJobMatch', methods=['GET','POST'])
def backToJobMatching():
    return redirect(url_for('jobMatchingRedirect'))

@app.route('/download/<path:filename>')
def download_file(filename):
    if filename.endswith('.json'):
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True) # , as_attachment=True
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename) # , as_attachment=True


@app.route('/uploads//<path:filename>')
def upload_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename) # , as_attachment=True

if __name__ == '__main__':
    #app.run(debug=True)
    print("url: http://localhost:8080/")
    serve(app, host="0.0.0.0", port=8080, threads=7)
