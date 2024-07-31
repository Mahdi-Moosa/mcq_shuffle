import json
import re
from TexSoup import TexSoup
import argparse  # For handling command-line arguments


def extract_questions_and_choices(latex_text):
    """
    Extracts questions and their choices from LaTeX text (unchanged from your provided code).
    Args:
        latex_text (str): The raw LaTeX text containing the questions and choices.

    Returns:
        list[dict]: A list of dictionaries, each representing a question. Each dictionary has:
            * "question" (str): The question text.
            * "choices" (list[str]): A list of answer choices for the question.
    """

    questions = []  

    # Regex to find individual question blocks (from \question to \end{oneparchoices})
    question_block_pattern = re.compile(r"\\question((?:.|\n)*?)\\end{oneparchoices}", re.DOTALL)
    question_blocks = question_block_pattern.findall(latex_text)

    for block in question_blocks:
        # Split the block to separate question text and choices
        question_parts = block.strip().split("\\begin{oneparchoices}")
        question_text = question_parts[0].strip()

        # Extract choices using a regex that handles both \choice and \CorrectChoice
        choice_pattern = r"(?<!^)\\(?:choice|CorrectChoice)\s+((?:.|\n)*?)(?=\\(?:choice|CorrectChoice)|$)"  # Negative lookbehind ensures no empty matches
        choices = re.findall(choice_pattern, question_parts[-1], re.DOTALL)  
        choices = [choice.strip() for choice in choices]  # Trim any extra whitespace

        questions.append({
            "question": question_text,
            "choices": choices
        })

    return questions


def process_tex_file(input_filename):
    with open(input_filename, 'r') as f:
        tex_content = f.read()

    soup_question = TexSoup(tex_content)
    question_choice_list = extract_questions_and_choices(str(soup_question.questions))

    jinja_string = '''{% for questions in question_sets %}
\\begin{questions}
{% for item in questions %}
    \question {{ item.question }}
    
        \\begin{oneparchoices}
        {% for choice in item.choices %}
            \choice {{ choice }}
        {% endfor %}
        \end{oneparchoices}
{% endfor %}
\end{questions}
\pagebreak
{% endfor %}'''

    tex_template = tex_content.replace(str(soup_question.questions), jinja_string)

    # Save outputs
    base_filename = input_filename.rsplit(".", 1)[0]  # Remove .tex extension

    with open(f"{base_filename}_questions.json", 'w') as json_file:
        json.dump(question_choice_list, json_file, indent=4)

    with open(f"{base_filename}_template.tex", 'w') as tex_file:
        tex_file.write(tex_template)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract questions and choices from LaTeX file.")
    parser.add_argument("input_file", help="Path to the input LaTeX file.")
    args = parser.parse_args()

    process_tex_file(args.input_file)
