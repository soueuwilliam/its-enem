# ITS-ENEM

## Overview

The `ITS-ENEM` project is an Intelligent Tutoring System (ITS) designed to assist students in preparing for the ENEM (Exame Nacional do Ensino Médio) exam, with a specific focus on the "Ciências da Natureza" (Natural Sciences) section. This system leverages a rule-based approach to deliver personalized learning experiences, adapting to each student's knowledge, performance, and progress. It covers key disciplines—Biology, Chemistry, and Physics—through a detailed ontology of topics, tracks learner metrics, and applies pedagogical rules to guide instruction.

`ITS-ENEM` helps learners to prepare for future exams and tailor their learning to their needs by providing recommendations of topics and areas to review based on the learner's performance in the Enem 2024 dataset. 

More specifically, this is a template implementation of a classic Intelligent Tutoring System (ITS) using Python. Classic architectures of ITS apply knowledge representation and decision-making techniques to personalize and support learning. The ITS implemented here is based on a pedagogy.yml file that defines the rules for the ITS's actions based on the Self-Determination Theory (SDT) for providing adaptive feedback.

### Why this approach?
- The Enem 2024 dataset is a large dataset with a lot of information about the questions and answers.
- The pedagogy.yml file is a simple file that defines the rules for the ITS's actions.
- The domain.yml file is a simple file that defines the structure of the knowledge domain given topics and areas.
- The learner.yml file is a simple file that defines the performance metrics for providing adaptive feedback.
- The controller.py file is a simple file that implements the ITS.
- Plus, it is a good template for future implementations of ITS in different tasks and feedback types.

## Project Structure

The repository is organized as follows:

- **`app/`**
  - `controller.py`: Manages the core logic, coordinating interactions between the model, view, and learner inputs.
  - `view.py`: Handles the user interface, displaying tasks, feedback, and progress to the learner.
- **`model/`**
  - `domain.yml`: Defines a hierarchical ontology of topics within "Ciências da Natureza."
  - `learner.yml`: Specifies the variables and their types/ranges for tracking learner profiles and performance.
  - `pedagogy.yml`: Contains the boolean logic rule base for task selection and feedback.
  - `model.py`: Provides functions or classes to load and manipulate the YAML models.
- **`ITS.ipynb`**: A Jupyter notebook demonstrating the system’s functionality with example data.
- **`README.md`**: This file, offering an overview and instructions.


## Setup

To set up the project locally, follow these steps:

1. **Clone the Repository**:

  git clone https://github.com/yourusername/its-enem.git

2. **Navigate to the Directory**:

   cd its-enem

3. **Install Dependencies** (assumes a `requirements.txt` file exists):

   pip install -r requirements.txt

4. **Verify YAML Files**: Ensure that `domain.yml`, `learner.yml`, and `pedagogy.yml` in the `model/` directory are properly formatted and populated with data.


## Usage

To run the ITS, execute the main controller script:

python app/controller.py

Alternatively, open `ITS.ipynb` in Jupyter Notebook to explore a step-by-step demonstration of the system, including sample learner interactions and rule applications.


## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature or bugfix branch.
3. Make changes with clear, descriptive commit messages.
4. Push your branch to your fork.
5. Submit a pull request to the main repository.


## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

