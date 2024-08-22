from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Path to the lectures folder
LECTURES_FOLDER = 'lectures'

# Lecture structure
LECTURES = {
    "Semester 1": {
        "Anatomy": ["Lec1", "Carbohydrate, Lipid Disorders, Liver Disease"],
        "BioChemistry": ["Spine, CNS", "MSK", "Git2"],
       # "Simulation": ["Pneumonia", "TB, Respiratory Failure", "Lung Cancer", "Basics of Bronchoscopy", "Pleural Diseases"],
        "CBG": ["Postoperative Care & Complications", "Basic Life Support", "Acute Postoperative Pain Management", "Obstetric Anesthesia"],
        "PMD": ["Tendom Entrapment", "Bone & Joints Infection", "Spinal Injury"],
        "TSF": ["Papulasquamous Disorders", "Hair Disorders & Acne", "Sweat Glands Disorders", "Pigmentation Disorders", "CTD [Lupus Erythematosus]", "Introduction to STDs", "Erectile Dysfunction"],
        "ECX": ["ALI"]
    },
    "Semester 2": {
        "IMM": ["Immunology", "Carbohydrate, Lipid Disorders, Liver Disease"],
        "IPP": ["Spine, CNS", "MSK", "Git2"],
        "MIC": ["Pneumonia", "TB, Respiratory Failure", "Lung Cancer", "Basics of Bronchoscopy", "Pleural Diseases"],
        "PAT": ["Postoperative Care & Complications", "Basic Life Support", "Acute Postoperative Pain Management", "Obstetric Anesthesia"],
        "PHE": ["Tendom Entrapment", "Bone & Joints Infection", "Spinal Injury"],
        "SBS": ["Papulasquamous Disorders", "Hair Disorders & Acne", "Sweat Glands Disorders", "Pigmentation Disorders", "CTD [Lupus Erythematosus]", "Introduction to STDs", "Erectile Dysfunction"],
       # "SIM": ["Tendom Entrapment", "Bone & Joints Infection", "Spinal Injury"]
    }
}

# Subfolders
SUBFOLDERS = ["videos", "recordings", "pdfs"]

# Function to create lecture folders if they do not exist
def create_lecture_folders():
    if not os.path.exists(LECTURES_FOLDER):
        os.makedirs(LECTURES_FOLDER)
    
    for semester, subjects in LECTURES.items():
        semester_path = os.path.join(LECTURES_FOLDER, semester)
        if not os.path.exists(semester_path):
            os.makedirs(semester_path)
        
        for subject, lectures in subjects.items():
            subject_path = os.path.join(semester_path, subject)
            if not os.path.exists(subject_path):
                os.makedirs(subject_path)
            
            for lecture in lectures:
                lecture_path = os.path.join(subject_path, lecture)
                if not os.path.exists(lecture_path):
                    os.makedirs(lecture_path)
                
                # Create subfolders (videos, recordings, pdfs) for each lecture
                for subfolder in SUBFOLDERS:
                    folder_path = os.path.join(lecture_path, subfolder)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

# Call the function to create folders
create_lecture_folders()

@app.route('/')
def home():
    return render_template('home.html', categories=LECTURES.keys())

@app.route('/category/<category>')
def show_category(category):
    subjects = LECTURES.get(category, {})
    return render_template('subjects.html', category=category, subjects=subjects)

@app.route('/subject/<category>/<subject>')
def show_subject(category, subject):
    lectures = LECTURES.get(category, {}).get(subject, [])
    return render_template('lectures.html', category=category, subject=subject, lectures=lectures)

@app.route('/lecture/<category>/<subject>/<lecture>')
def show_lecture(category, subject, lecture):
    # Dictionary to store files for each subfolder
    files = {subfolder: [] for subfolder in SUBFOLDERS}
    
    for subfolder in SUBFOLDERS:
        folder_path = os.path.join(LECTURES_FOLDER, category, subject, lecture, subfolder)
        
        # Check if the subfolder exists and list the files
        if os.path.exists(folder_path):
            files[subfolder] = os.listdir(folder_path)

    return render_template('lecture.html', category=category, subject=subject, lecture=lecture, files=files)

@app.route('/download/<category>/<subject>/<lecture>/<subfolder>/<filename>')
def download_file(category, subject, lecture, subfolder, filename):
    folder_path = os.path.join(LECTURES_FOLDER, category, subject, lecture, subfolder)
    return send_from_directory(folder_path, filename)

if __name__ == '__main__':
    app.run(debug=True)
