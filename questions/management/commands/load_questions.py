import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from questions.models import Subject, Chapter, Topic,Question

class Command(BaseCommand):
    help = 'Load questions from a CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def extract_topic_name(self, topic_string):
        # Split the string by '-' and take the last part, then strip whitespace
        return topic_string.split('-')[-1].strip()
    
    
    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
    
    

        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            with transaction.atomic():  # Ensure atomicity
                for row in reader:
                    # Extract data from the row
                    question_text = row['question']
                    options = eval(row['options'])  # Convert string to list
                    answer = row['answer'].strip().upper()
                    explanation = row['explanation']
                    topic_string = row['topic']
                    difficulty = row['difficulty']
                    chapter_number = row['chapter']

                    # Extract the topic name
                    topic_name = self.extract_topic_name(topic_string)
                    

                    # Get or create Subject (assuming a single subject for simplicity)
                    subject, _ = Subject.objects.get_or_create(name="Artificial Intelligence and Neural Networks")

                    # Get or create Chapter
                    chapter, _ = Chapter.objects.get_or_create(
                        subject=subject,
                        chapter_number=chapter_number,
                        # defaults={'name': f'Chapter {chapter_number}'}
                        name= "Neural networks"
                    )

                    # Get or create Topic
                    topic, _ = Topic.objects.get_or_create(
                        chapter=chapter,
                        name=topic_name
                    )

                    # Create Question
                    Question.objects.create(
                        chapter=chapter,
                        topic=topic_name,
                        question=question_text,
                        options=options,
                        answer=answer,
                        explanation=explanation,
                        difficulty=difficulty
                    )

        self.stdout.write(self.style.SUCCESS('Successfully loaded questions from CSV'))