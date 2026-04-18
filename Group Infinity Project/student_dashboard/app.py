from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import random
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-in-production'

# Initialize session data
@app.before_request
def before_request():
    if 'results' not in session:
        session['results'] = []
    if 'college_timings' not in session:
        session['college_timings'] = {
            'start': '09:00',
            'end': '16:00',
            'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        }
    if 'tuition_timings' not in session:
        session['tuition_timings'] = {'subjects': []}

# Sample data
motivational_messages = [
    "Believe in yourself! You can achieve anything.",
    "Every expert was once a beginner.",
    "Small progress is still progress.",
    "Your attitude determines your direction.",
    "Stay positive, work hard, make it happen.",
    "The only way to do great work is to love what you do.",
    "Don't watch the clock; do what it does. Keep going.",
    "Success is not final, failure is not fatal."
]

breathing_exercises = [
    "Take a deep breath in for 4 seconds, hold for 4, exhale for 4.",
    "Close your eyes and take 5 deep breaths.",
    "Try box breathing: 4-4-4-4 pattern.",
    "Breathe in slowly through your nose for 4 counts, hold for 2, exhale for 6.",
    "Practice 5-5-5 breathing: Inhale for 5, hold for 5, exhale for 5.",
    "Take 3 deep belly breaths, feeling your stomach expand and contract."
]

# Quiz questions
quiz_questions = [
    {
        "id": 1,
        "question": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "correct": "Paris"
    },
    {
        "id": 2,
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": "Mars"
    },
    {
        "id": 3,
        "question": "What is 5 + 7?",
        "options": ["10", "11", "12", "13"],
        "correct": "12"
    },
    {
        "id": 4,
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"],
        "correct": "William Shakespeare"
    },
    {
        "id": 5,
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct": "Pacific Ocean"
    }
]

puzzles = [
    {"question": "I speak without a mouth and hear without ears. What am I?", "answer": "echo"},
    {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
    {"question": "What has keys but can't open locks?", "answer": "piano"},
    {"question": "What has to be broken before you can use it?", "answer": "egg"},
    {"question": "I'm tall when I'm young, and short when I'm old. What am I?", "answer": "candle"}
]

# Routes
@app.route('/')
def landing():
    """Landing page"""
    return render_template('landing.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard page with cards"""
    results = session.get('results', [])
    results_count = len(results)
    weak_subjects_count = sum(1 for r in results if float(r.get('marks', 0)) < 60)
    
    return render_template('dashboard.html', 
                         username="Student",
                         results_count=results_count,
                         weak_subjects_count=weak_subjects_count)

@app.route('/enter-results')
def enter_results():
    """Page for entering student results"""
    recent_results = session.get('results', [])
    print(f"Enter results page - Number of results: {len(recent_results)}")
    return render_template('enter_results.html', recent_results=recent_results)

@app.route('/submit-result', methods=['POST'])
def submit_result():
    """Handle result submission"""
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        subject = request.form.get('subject')
        marks = request.form.get('marks')
        
        print(f"Submitting result - Student: {student_name}, Subject: {subject}, Marks: {marks}")
        
        if student_name and subject and marks:
            try:
                marks_float = float(marks)
                if marks_float < 0 or marks_float > 100:
                    print("Marks out of range")
                    return redirect(url_for('enter_results'))
                
                results = session.get('results', [])
                new_id = len(results)
                
                result = {
                    'id': new_id,
                    'student_name': student_name,
                    'subject': subject,
                    'marks': marks_float,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                
                results.append(result)
                session['results'] = results
                session.modified = True
                print(f"Result added successfully. Total results: {len(results)}")
                
            except ValueError as e:
                print(f"ValueError: {e}")
                pass
    
    return redirect(url_for('enter_results'))

@app.route('/update-result', methods=['POST'])
def update_result():
    """Update a specific result"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        result_id = int(data.get('id'))
        subject = data.get('subject', '').strip()
        marks = float(data.get('marks'))
        
        if not subject:
            return jsonify({'success': False, 'error': 'Subject cannot be empty'})
        
        if marks < 0 or marks > 100:
            return jsonify({'success': False, 'error': 'Marks must be between 0 and 100'})
        
        results = session.get('results', [])
        for i, result in enumerate(results):
            if result.get('id') == result_id:
                results[i]['subject'] = subject
                results[i]['marks'] = marks
                session['results'] = results
                session.modified = True
                print(f"Result updated: ID {result_id}")
                return jsonify({'success': True})
        
        return jsonify({'success': False, 'error': 'Result not found'})
        
    except ValueError as e:
        return jsonify({'success': False, 'error': 'Invalid data format'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete-result', methods=['POST'])
def delete_result():
    """Delete a specific result"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'})
        
        result_id = int(data.get('id'))
        
        results = session.get('results', [])
        results = [r for r in results if r.get('id') != result_id]
        
        # Reassign IDs
        for i, result in enumerate(results):
            result['id'] = i
        
        session['results'] = results
        session.modified = True
        print(f"Result deleted: ID {result_id}")
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/clear-results', methods=['POST'])
def clear_results():
    """Clear all results from session"""
    try:
        session['results'] = []
        session.modified = True
        print("All results cleared")
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/timetable')
def timetable():
    """Timetable page with AI analysis"""
    results = session.get('results', [])
    print(f"Timetable page - Number of results: {len(results)}")
    
    # Analyze results
    weak_subjects = []
    strong_subjects = []
    subject_analysis = []
    
    for result in results:
        marks = float(result['marks'])
        subject = result['subject']
        
        if marks < 60:
            weak_subjects.append({
                'subject': subject,
                'marks': marks,
                'priority': 'High' if marks < 50 else 'Medium'
            })
        else:
            strong_subjects.append({
                'subject': subject,
                'marks': marks
            })
        
        subject_analysis.append({
            'subject': subject,
            'marks': marks,
            'status': 'Weak' if marks < 60 else 'Average' if marks < 75 else 'Strong'
        })
    
    weak_subjects.sort(key=lambda x: x['marks'])
    
    college_timings = session.get('college_timings')
    tuition_timings = session.get('tuition_timings')
    
    study_plan = generate_study_plan(weak_subjects, strong_subjects, college_timings, tuition_timings)
    
    return render_template('timetable.html', 
                         subject_analysis=subject_analysis,
                         weak_subjects=weak_subjects,
                         strong_subjects=strong_subjects,
                         study_plan=study_plan,
                         college_timings=college_timings,
                         tuition_timings=tuition_timings,
                         recent_results=results)

def generate_study_plan(weak_subjects, strong_subjects, college_timings, tuition_timings):
    """Generate personalized study timetable"""
    
    try:
        college_start = datetime.strptime(college_timings['start'], '%H:%M')
        college_end = datetime.strptime(college_timings['end'], '%H:%M')
    except:
        college_start = datetime.strptime('09:00', '%H:%M')
        college_end = datetime.strptime('16:00', '%H:%M')
    
    study_plan_items = []
    
    # Morning study (before college)
    morning_start = datetime.strptime('06:00', '%H:%M')
    morning_end = college_start - timedelta(hours=1)
    
    if morning_start < morning_end:
        study_plan_items.append({
            'time': f"{morning_start.strftime('%I:%M %p')} - {morning_end.strftime('%I:%M %p')}",
            'subject': 'Morning Review',
            'focus': 'Quick revision of previous day\'s topics',
            'priority': 'Medium'
        })
    
    # College hours
    college_duration = (college_end - college_start).seconds // 3600
    study_plan_items.append({
        'time': f"{college_start.strftime('%I:%M %p')} - {college_end.strftime('%I:%M %p')}",
        'subject': 'College Hours',
        'focus': f'Attend classes ({college_duration} hours)',
        'priority': 'Required'
    })
    
    # Short break after college
    break_start = college_end
    break_end = college_end + timedelta(minutes=30)
    study_plan_items.append({
        'time': f"{break_start.strftime('%I:%M %p')} - {break_end.strftime('%I:%M %p')}",
        'subject': 'Break',
        'focus': 'Rest and refresh',
        'priority': 'Low'
    })
    
    # Evening study (focus on weak subjects)
    evening_start = college_end + timedelta(hours=1)
    evening_end = datetime.strptime('21:00', '%H:%M')
    
    if evening_start < evening_end and weak_subjects:
        total_minutes = (evening_end - evening_start).seconds // 60
        slots_count = len(weak_subjects) + 1  # +1 for break
        minutes_per_slot = max(30, total_minutes // slots_count)
        
        current_time = evening_start
        
        # Study slots for weak subjects
        for subject in weak_subjects[:3]:  # Limit to top 3 weakest
            slot_end = current_time + timedelta(minutes=minutes_per_slot)
            if slot_end <= evening_end:
                study_plan_items.append({
                    'time': f"{current_time.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}",
                    'subject': subject['subject'],
                    'focus': f"Focus on weak areas - {subject['priority']} priority",
                    'priority': subject['priority']
                })
                current_time = slot_end
        
        # Add break
        if current_time < evening_end:
            break_end = min(current_time + timedelta(minutes=15), evening_end)
            study_plan_items.append({
                'time': f"{current_time.strftime('%I:%M %p')} - {break_end.strftime('%I:%M %p')}",
                'subject': 'Break',
                'focus': 'Short break - stretch and relax',
                'priority': 'Low'
            })
            current_time = break_end
        
        # Review session
        if current_time < evening_end:
            review_end = current_time + timedelta(minutes=30)
            if review_end <= evening_end:
                study_plan_items.append({
                    'time': f"{current_time.strftime('%I:%M %p')} - {review_end.strftime('%I:%M %p')}",
                    'subject': 'Review Session',
                    'focus': 'Quick revision of today\'s learning',
                    'priority': 'Medium'
                })
    
    # Add weekend special plan if weak subjects exist
    if weak_subjects:
        study_plan_items.append({
            'time': 'Weekends (Saturday)',
            'subject': 'Deep Dive Session',
            'focus': f"Focus on: {', '.join([s['subject'] for s in weak_subjects[:2]])}",
            'priority': 'High'
        })
        study_plan_items.append({
            'time': 'Weekends (Sunday)',
            'subject': 'Practice & Revision',
            'focus': 'Mock tests and concept revision',
            'priority': 'High'
        })
    
    return study_plan_items

@app.route('/update-timings', methods=['POST'])
def update_timings():
    """Update college and tuition timings"""
    try:
        data = request.get_json()
        
        if 'college' in data:
            session['college_timings'] = data['college']
        if 'tuition' in data:
            session['tuition_timings'] = data['tuition']
        
        session.modified = True
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/stress-manager')
def stress_manager():
    """Stress management page"""
    motivation = random.choice(motivational_messages)
    exercise = random.choice(breathing_exercises)
    return render_template('stress_manager.html', 
                         motivation=motivation, 
                         exercise=exercise)

@app.route('/get-new-exercise')
def get_new_exercise():
    """AJAX endpoint for new breathing exercise"""
    return jsonify({'exercise': random.choice(breathing_exercises)})

@app.route('/get-new-motivation')
def get_new_motivation():
    """AJAX endpoint for new motivation message"""
    return jsonify({'motivation': random.choice(motivational_messages)})

@app.route('/fun-games')
def fun_games():
    """Fun games page"""
    return render_template('fun_games.html')

@app.route('/get-quiz-question')
def get_quiz_question():
    """Get random quiz question"""
    question = random.choice(quiz_questions)
    return jsonify({
        'question': question['question'],
        'options': question['options'],
        'correct': question['correct']
    })

@app.route('/check-quiz-answer', methods=['POST'])
def check_quiz_answer():
    """Check quiz answer"""
    try:
        data = request.get_json()
        question = data.get('question')
        answer = data.get('answer')
        
        for q in quiz_questions:
            if q['question'] == question:
                return jsonify({'correct': q['correct'] == answer})
        return jsonify({'correct': False})
    except:
        return jsonify({'correct': False})

@app.route('/get-puzzle')
def get_puzzle():
    """Get random puzzle"""
    puzzle = random.choice(puzzles)
    return jsonify({
        'question': puzzle['question'],
        'answer': puzzle['answer']
    })

@app.route('/check-puzzle-answer', methods=['POST'])
def check_puzzle_answer():
    """Check puzzle answer"""
    try:
        data = request.get_json()
        user_answer = data.get('answer', '').lower().strip()
        correct_answer = data.get('correct_answer', '').lower().strip()
        return jsonify({'correct': user_answer == correct_answer})
    except:
        return jsonify({'correct': False})

@app.route('/resume-builder')
def resume_builder():
    """Resume builder page"""
    return render_template('resume_builder.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)