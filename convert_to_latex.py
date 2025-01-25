import re

def convert_to_latex(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    latex_lines = [
        r"\documentclass[a4paper,10pt]{article}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[russian]{babel}",
        r"\usepackage{geometry}",
        r"\geometry{a4paper, margin=0.125in}",  # Уменьшен padding в 4 раза
        r"\usepackage{multicol}",
        r"\usepackage{graphicx}",
        r"\usepackage{amssymb}",  # Для использования квадратных чекбоксов
        r"\renewcommand{\baselinestretch}{0.5}",  # Уменьшен межстрочный интервал
        r"\setlength{\itemsep}{0pt}",  # Убираем отступы между элементами списка
        r"\pagestyle{empty}",
#        r"\setlength\parindent{0pt}",
        r"\begin{document}"
    ]

    # Generate the content for one quarter
    quarter_content = [
        r"\section*{\scriptsize Анкета для практики}"  # Уменьшен шрифт
    ]

    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("### "):  # Раздел
            if current_section:
                quarter_content.append(r"\vskip 0.2cm")  # Уменьшен отступ между разделами
            current_section = line[4:]
            quarter_content.append(rf"\section*{{\scriptsize {current_section}}}")  # Уменьшен шрифт
            quarter_content.append(r"\vskip 0.1cm")  # Дополнительный отступ после названия раздела
        elif line.startswith("#### "):  # Вопрос
            question = line[5:]
            match = re.match(r"(.*?)\((.*?)\)", question)
            if match:
                question_text, options = match.groups()
                # Просто добавляем текст без разбивки
                quarter_content.append(rf"\scriptsize \noindent {question_text.strip()} ({options.strip()})")  # Уменьшен шрифт
            else:
                # Просто добавляем текст без разбивки
                quarter_content.append(rf"\scriptsize \noindent {question}")  # Уменьшен шрифт

            # Размещение чекбоксов справа с уменьшенным расстоянием между ними
            quarter_content.append(r"\noindent \hfill \scriptsize $\square$ Да \hspace{0.1cm} $\square$ Нет")  # Уменьшено расстояние
            quarter_content.append(r"\\")  # Явный переход на новую строку
            quarter_content.append(r"\vskip 0.1cm")  # Уменьшен отступ между вопросом и следующей строкой
        elif line:  # Примечания, игнорируем
            pass

    # Combine the quarters on a single page in two columns
    latex_lines.append(r"\begin{multicols}{2}")  # Использование двух колонок

    latex_lines.append(r"\noindent\begin{minipage}{0.5\textwidth}\centering")
    latex_lines.append(r"\vskip 0.5cm")  # Уменьшен вертикальный отступ перед секцией
    latex_lines.extend(quarter_content)
    latex_lines.append(r"\end{minipage}%")

    latex_lines.append(r"\hspace{0.5cm}")  # Уменьшен горизонтальный отступ между секциями

    latex_lines.append(r"\begin{minipage}{0.5\textwidth}\centering")
    latex_lines.append(r"\vskip 0.5cm")  # Уменьшен вертикальный отступ перед секцией
    latex_lines.extend(quarter_content)
    latex_lines.append(r"\end{minipage}")

    latex_lines.append(r"\vskip 1cm")  # Уменьшен отступ между секциями

    latex_lines.append(r"\noindent\begin{minipage}{0.5\textwidth}\centering")
    latex_lines.append(r"\vskip 0.5cm")  # Уменьшен вертикальный отступ перед секцией
    latex_lines.extend(quarter_content)
    latex_lines.append(r"\end{minipage}%")

    latex_lines.append(r"\hspace{0.5cm}")  # Уменьшен горизонтальный отступ между секциями

    latex_lines.append(r"\begin{minipage}{0.5\textwidth}\centering")
    latex_lines.append(r"\vskip 0.5cm")  # Уменьшен вертикальный отступ перед секцией
    latex_lines.extend(quarter_content)
    latex_lines.append(r"\end{minipage}")

    latex_lines.append(r"\end{multicols}")  # Закрытие многоколоночного окружения

    latex_lines.append(r"\end{document}")

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(latex_lines))

if __name__ == "__main__":
    convert_to_latex("README.md", "output.tex")
