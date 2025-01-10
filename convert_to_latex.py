import re

def convert_to_latex(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    latex_lines = [
        r"\documentclass[a4paper,12pt]{article}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[russian]{babel}",
        r"\usepackage{geometry}",
        r"\geometry{a4paper, margin=1in}",
        r"\begin{document}",
        r"\section*{Анкета для практики}"
    ]

    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("### "):  # Раздел
            if current_section:
                latex_lines.append(r"\end{itemize}")
            current_section = line[4:]
            latex_lines.append(rf"\section*{{{current_section}}}")
            latex_lines.append(r"\begin{itemize}")
        elif line.startswith("#### "):  # Вопрос
            question = line[5:]
            match = re.match(r"(.*?)\((.*?)\)", question)
            if match:
                question_text, options = match.groups()
                latex_lines.append(rf"\item {question_text.strip()} ({options.strip()})")
            else:
                latex_lines.append(rf"\item {question}")
        elif line:  # Примечания, игнорируем
            pass

    if current_section:
        latex_lines.append(r"\end{itemize}")

    latex_lines.append(r"\end{document}")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(latex_lines))

if __name__ == "__main__":
    convert_to_latex("README.md", "output.tex")
