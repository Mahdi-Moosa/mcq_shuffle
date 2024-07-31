import json
import random
import argparse
from copy import deepcopy
from jinja2 import Environment, FileSystemLoader

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Generate randomized MCQ sets in LaTeX.")
parser.add_argument("--json", required=True, help="Path to the JSON file containing questions")
parser.add_argument("--template", required=True, help="Path to the LaTeX template file")
parser.add_argument("-n", "--repetitions", type=int, default=4, help="Number of randomized sets to generate (default: 4)")
parser.add_argument("-o", "--output", help="Output file name (default: randomized_mcq_set.tex)")
args = parser.parse_args()

# Load questions from JSON
with open(args.json, 'r') as file:
    original_questions = json.load(file)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(args.template)

# Prepare randomized questions for each repetition
question_sets = []
for _ in range(args.repetitions):
    questions = deepcopy(original_questions)
    random.shuffle(questions)
    for question in questions:
        random.shuffle(question["choices"])
    question_sets.append(questions)

# Render the template with the randomized question sets
output = template.render(question_sets=question_sets)

# Determine output filename
output_file = args.output if args.output else 'randomized_mcq_set.tex'

# Write the rendered output to file
with open(output_file, 'w') as file:
    file.write(output)
