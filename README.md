# 📸 Camera Basics: An Interactive Learning Platform
### **Learn the basics of camera settings and take your photography to the next level!**

This is a web-based educational tool designed to teach beginners the core concepts of photography — including exposure, ISO, aperture, shutter speed, and the exposure triangle — through a mix of concise lessons and interactive quizzes.

Developed as the final project for our UI Design course (Spring 2025), this site combines structured visual learning with responsive, hands-on assessments to support deeper understanding.

## 🚀 Features
- 🧠 Modular learning sections explaining each core concept with visual examples

- 🧪 Interactive quizzes using drag-and-drop, true/false, and toggles

- 📊 Progress tracking through a clean, dynamic progress bar

- 💡 Designed for clarity, accessibility, and user-centered experience

## 🛠️ Tech Stack
Flask (Python) for backend routing and data handling

HTML / CSS / Bootstrap for frontend structure and styling

JavaScript / jQuery for dynamic interactions

Jinja2 templates for layout inheritance and data-driven rendering

## 📁 Project Structure
```bash .
    ├── static/
    │   ├── css/                     # Stylesheets (main.css, quiz.css, etc.)
    │   ├── js/                      # JavaScript logic (quiz_core.js, drag_drop.js, etc.)
    │   └── images/                  # Learning and quiz images
    ├── templates/
    ├── ├── aperture_step.html etc.  # Learning pages
    │   ├── quiz_1.html etc.         # Quiz pages
    │   ├── quiz_answer.html         # Feedback and result display
    │   ├── layout.html              # Shared navbar & base layout
    │   └── homepage.html            # Landing overview page
    ├── app.py                       # Flask server and routing logic
    └── README.md
```

## 💻 Getting Started (Local Setup)

1. Clone the repo:
    ```bash
    git clone https://github.com/popi-x/UI-final-project.git
    cd UI-final-project
    ```

2. Install Flask:
    ```bash
    pip install Flask
    ```

3. Run the app:
    ```bash
    python app.py
    ```

4. Visit `http://localhost:5001` in your browser
*⚠ This is a development setup using Flask's built-in server.*


## 👥 Team & Responsibilities
- Shanshan Wu – Learning content and interactivity design, data architecture, instructional structure

- Rosie Rao – Learning section frontend interactions, data routing, design implementation

- Caroline Zhang – Quiz UI implementation and frontend logic; Graphic design templates

- Natalie Kim – Quiz backend structure, data routing, feedback, and scoring logic

- Shanshan also handled repository management, Git workflows, and main branch integration.


## 🎓 Course Info
This project was completed as a final project for COMS W4170: User Interface Design at Columbia University, Spring 2025.


