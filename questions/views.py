
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Subject, Chapter, Topic,Question, ModelTestAttempt
from django.shortcuts import render, get_object_or_404
from django.db import models



from django.utils import timezone
# Create your views here.

@login_required
def questions(request):
    
    
    selected_subject = None
    selected_chapter = None
    questions = []
    
    # Get selected subject and chapter from URL parameters
    subject_id = request.GET.get('subject_id')
    chapter_id = request.GET.get('chapter_id')
    
    if subject_id:
        selected_subject = get_object_or_404(Subject, id=subject_id)
        if chapter_id:
            selected_chapter = get_object_or_404(Chapter, id=chapter_id)
            questions = Question.objects.filter(chapter=selected_chapter)
    
    subjects = Subject.objects.all()
    chapters = Chapter.objects.filter(subject=selected_subject) if selected_subject else []
    
    total_completed = ModelTestAttempt.objects.filter(user=request.user).count()
    avg_score = ModelTestAttempt.objects.filter(user=request.user).aggregate(
        avg_score=models.Avg('score')
    )['avg_score'] or 0
    
    return render(request, 'questions.html', {
        'username': request.user.username,
        'subjects': subjects,
        'chapters': chapters,
        'selected_subject': selected_subject,
        'selected_chapter': selected_chapter,
        'questions': questions,
        'test_started': request.session.get('test_started', False),
        'total_completed': total_completed,
        'avg_score': avg_score
    })


@login_required
def practice_chapter(request, chapter_id):
    """Display all questions for a chapter in a new window with navigation."""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    questions = Question.objects.filter(chapter=chapter).values(
        'id', 'question', 'options', 'answer', 'explanation'
    )
    return render(request, 'practice_chapter.html', {
        'chapter': chapter,
        'questions': list(questions),
    })

def subject_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    chapters = Chapter.objects.filter(subject=subject)
    return render(request, 'subject_detail.html', {
        'selected_subject': subject,
        'chapters': chapters,
    })

def chapter_view(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    questions = Question.objects.filter(chapter=chapter)
    return render(request, 'chapter_detail.html', {
        'selected_chapter': chapter,
        'questions': questions,
    })

def model_test(request):
    
    # Check if test is already in progress
    if request.session.get('test_started', False):
       
        # Calculate remaining time
        start_time = timezone.datetime.fromisoformat(request.session['test_start_time'])
        elapsed_time = timezone.now() - start_time
        remaining_time = max(7200 - elapsed_time.total_seconds(), 0)  # 2 hours in seconds

        # Reload the test with remaining time
        easy_questions = Question.objects.filter(id__in=request.session['test_questions']['section_a'])
        medium_questions = Question.objects.filter(id__in=request.session['test_questions']['section_b'])
        return render(request, 'model_test.html', {
            'section_a': easy_questions,
            'section_b': medium_questions,
            'remaining_time': remaining_time
        })
    
    # Start new test
    easy_questions = list(Question.objects.filter(difficulty='Easy').order_by('?')[:60])
    medium_questions = list(Question.objects.filter(difficulty='Medium').order_by('?')[:20])
    
     # Get progress data
    total_completed = ModelTestAttempt.objects.filter(user=request.user).count()
    avg_score = ModelTestAttempt.objects.filter(user=request.user).aggregate(
        avg_score=models.Avg('score')
    )['avg_score'] or 0
    
    return render(request, 'model_test.html', {
        'section_a': easy_questions,
        'section_b': medium_questions,
        'remaining_time': 7200, # 2 hours in seconds
        'total_completed': total_completed,
        'avg_score': avg_score
    })

def submit_model_test(request):
    if request.method == 'POST':
        

        # Calculate scores
        correct = 0
        wrong = 0
        for q_id, answer in request.POST.items():
            if q_id.startswith('q_'):
                question = Question.objects.get(id=int(q_id[2:]))
                if answer == question.answer:
                    correct += 1
                else:
                    wrong += 1
        
        unattempted = 80 - (correct + wrong)
        score = (correct * 1) + (wrong * 0)  # Adjust based on your marking scheme
        
        # Store attempt in database
        ModelTestAttempt.objects.create(
            user=request.user,
            correct=correct,
            wrong=wrong,
            unattempted=unattempted,
            score=score
        )

        
        return render(request, 'test_result.html', {
            'correct': correct,
            'wrong': wrong,
            'unattempted': unattempted,
            'total_tests': ModelTestAttempt.objects.filter(user=request.user).count()
        })
    else:
        # Handle auto-submit case
        ModelTestAttempt.objects.create(
            user=request.user,
            correct=0,
            wrong=0,
            unattempted=80,
            score=0
        )
        return render(request, 'test_result.html', {
            'correct': 0,
            'wrong': 0,
            'unattempted': 80,
            'total_tests': ModelTestAttempt.objects.filter(user=request.user).count()
        })

def LogoutView(request):
    logout(request)
    return redirect('login')

