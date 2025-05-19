from flask import Flask, render_template, request, redirect, url_for, session
import csv
import random

app = Flask(__name__)
app.secret_key = 'une-cle-secrete-pour-la-session'

def charger_questions():
    questions = []
    with open('questions.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            options = [
                row['option1'],
                row['option2'],
                row['option3'],
                row['option4']
            ]
            random.shuffle(options)
            questions.append({
                'question': row['question'],
                'options': options,
                'answer': row['answer']  # on garde la bonne réponse
            })
    random.shuffle(questions)
    return questions

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        questions = session.get('questions', [])
        bonnes = 0
        corrections = []

        for i, q in enumerate(questions):
            user_answer = request.form.get(f'q{i}')
            correct_answer = q['answer']
            is_correct = user_answer == correct_answer
            if is_correct:
                bonnes += 1
            corrections.append({
                'question': q['question'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct
            })

        score = round((bonnes / len(questions)) * 20)

        return render_template(
            'resultat.html',
            score=score,
            bonnes=bonnes,
            total=len(questions),
            corrections=corrections
        )
    else:
        questions = charger_questions()
        session['questions'] = questions  # on garde les questions mélangées avec bonnes réponses
        return render_template('index.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)
