# AI-Driven Customer Support System: Moderation, Classification, Checkout and Evaluation

## Introduction

This system utilizes OpenAI's APIs within a framework designed to streamline customer support for businesses. It generates, moderates, classifies, and evaluates customer interactions, aiming to improve response quality and operational efficiency. Targeted at customer service departments, the system automates the handling of inquiries, making support more effective and accurate.

## Presentation

View presentation [PDF file](https://drive.google.com/file/d/1mTQpQhrG-iT35RVRBwxtkWtRl1tc-Ms7/view?usp=sharing)

## Features

- Automated Moderation: Utilizes OpenAI's Moderation API to filter inappropriate content from customer comments, ensuring a respectful communication environment.
- Prompt Injection Prevention: Safeguards against malicious inputs that could disrupt customer support, maintaining the integrity of interactions.
- Intelligent Classification: Automatically categorizes service requests into relevant departments for efficient query handling and response.
- Chain of Thought Reasoning: Employs advanced reasoning to provide detailed, step-by-step answers to complex customer questions.
- Comprehensive Output Checks: Includes checks for moderation and relevance of responses, guaranteeing high-quality support.
- Thorough Evaluation Process: Evaluates responses to ensure they meet customer needs, with specific mechanisms for both single and multiple-answer inquiries.

## Tech Stack

- Python
- OpenAI API

## Environment

Developed and tested for Linux.

## Installation and Setup

1. Check Python Version
   Ensure you have Python 3 installed by running:
   `python3 --version`
   If Python is not installed, follow the instructions here: [Install Python on Ubuntu](https://www.makeuseof.com/install-python-ubuntu/).

2. Update your package list and install pip:
   `sudo apt update`
   `sudo apt install python3-pip`

3. Install virtual environment tools:
   `sudo apt install virtualenv virtualenvwrapper`

4. Configure the virtual environment:

   - Open file:
     `nano ~/.bashrc`
   - Add the following lines to the end of the file:
     `WORKON_HOME=$HOME/.virtualenvs`
     `VIRTUAL_ENVWRAPPER_PYTHON=/usr/bin/python3`
     `source /usr/share/virtualenvwrapper/virtualenvwrapper.sh`

5. Create a new virtual environment:
   `mkvirtualenv example`

6. Work on virtual environment:
   `workon example`

7. Clone this repository.

8. Navigate into the project directory:
   `cd ai-ecommerce-email-assistant`

9. Install the requirements:
   `pip install -r requirements.txt`

10. [OpenAI Migration](https://github.com/openai/openai-python/discussions/742):
    `openai migrate`

11. [Get your API key](https://beta.openai.com/account/api-keys)

12. Add OpenAI API Key to the Virtual Environment`s Environment Variables

    - Open or create an .env file within your virtual environment:
      `nano .env`
    - In the .env file, enter the following line, replacing your_api_key_here with your actual OpenAI API key:
      `OPENAI_API_KEY=your_api_key_here`
    - Activate the environment variables in your current session:
      `source .env`
    - Test if the OpenAI API Key was successfully added by printing it:
      `echo $OPENAI_API_KEY`
      If the command prints your API key, it has been successfully added to the environment variables.

13. Running the Application

- For generating comments: `python3 generate_comment.py`
- For OpenAI's default moderation: `python3 moderation.py`
- For intelligent classification: `python3 classification.py`
- For chain of thoughts reasoning: `python3 chain_of_thoughts.py`
- For preventing injection: `python3 prevent_injection.py`
- For evluating single answer query: `python3 evaluation_1.py`
- For evluating multi answer query: `python3 evaluation_2.py`
