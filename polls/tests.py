from django.test import TestCase, Client
import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Question


# Create your tests here.

def creat_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    client = Client()
    
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no polls are availble.')
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_past_question(self):
        creat_question(question_text='past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'], ['<Question: past question>'])

    def test_further_question(self):
        creat_question(question_text='further question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'no polls are availble.')
        self.assertQuerysetEqual(response.context['lastest_question_list'], [])

    def test_further_question_and_past_question(self):
        creat_question(question_text='past question', days=-30)
        creat_question(question_text='further question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'], ['<Question: past question>'])

    def test_two_past_question(self):
        creat_question(question_text='past question 1', days=-30)
        creat_question(question_text='past question 2', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['lastest_question_list'], ['<Question: past question 1>', '<Question: past question 2>'])

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = creat_question(question_text='future question', days=5)
        url = reverse('poll:detail', args=future_question.id,)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = creat_question(question_text='past question', days=-5)
        url = reverse('poll:detail', args=past_question.id,)
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
    

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_older_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        older_question = Question(pub_date=time)
        self.assertIs(older_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
