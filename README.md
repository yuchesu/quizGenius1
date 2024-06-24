# Quiz Application

## Overview

This project is a web-based quiz application developed using the Django framework. The application allows users to take quizzes and view their results. The quizzes are generated randomly from a pool of questions in a chosen category.

## Project Requirements

- Use Django and Django ORM to develop the project.
- The backend and frontend are integrated into a single project.
- Follow the Django MVT (Model-View-Template) design pattern.
- Utilize Django's built-in authentication system.
- Employ Django class-based views and generic views.
- Do not use JavaScript for this project.
- Ensure a Global Navigation Bar is present on every page.

## Project Description

The quiz application allows users to take quizzes and view their results. The following functionalities are implemented:

- Users can only take one quiz at a time.
- Users choose a quiz category and start the quiz.
- The quiz is randomly generated from the questions in the chosen category.
- Upon completion, the system displays the result of the quiz and the result of each question.
- Users can view the results of all the quizzes they have taken.

### Specific Features

- Questions are randomly assigned to each quiz.
- Each quiz contains 5 multiple choice questions.
- Only one quiz can be taken at a time.
- If the correct answer of a question is changed, the corresponding quiz results will also be updated accordingly.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Apply migrations:**

   ```bash
   python manage.py migrate

5. **Run the development server:**

   ```bash
   python manage.py runserver

## Usage
- Navigate to the homepage.
- Register or login to start taking quizzes.
- Choose a quiz category and start the quiz.
- Answer the questions and submit the quiz to view the results.
- View the result of all quizzes taken from the user dashboard.
