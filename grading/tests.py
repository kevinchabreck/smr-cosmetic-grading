from django.test import TestCase
from django.urls import reverse

from .models import Test, Question, Choice

class TestModelTests(TestCase):
  def test_first_question_with_no_questions(self):
    """
    first_question() returns None when Test has no questions
    """
    test = Test.objects.create(title="my test", description="my test description")
    self.assertIsNone(test.first_question())

  def test_first_question_with_one_parent_question(self):
    """
    first_question() returns a Question when Test has a single parent question
    """
    test = Test.objects.create(title="my test", description="my test description")
    question = Question.objects.create(test=test,question_text="my question")
    self.assertIs(test.first_question().id, question.id)

  def test_first_question_with_multiple_parent_questions(self):
    """
    first_question() returns the first created Question when Test has multiple parent questions
    """
    test = Test.objects.create(title="my test", description="my test description")
    question1 = Question.objects.create(test=test,question_text="my question 1")
    Question.objects.create(test=test, question_text="my question 2")
    Question.objects.create(test=test, question_text="my question 3")
    self.assertIs(test.first_question().id, question1.id)

class QuestionModelTests(TestCase):
  def test_next_question_with_one_question(self):
    """
    next_question() returns None when there is only one question
    """
    test = Test.objects.create(title="my test", description="my test description")
    question = Question.objects.create(test=test, question_text="my question")
    self.assertIsNone(question.next_question())

  def test_next_question_with_one_question_and_subquestions(self):
    """
    next_question() returns None when there is only one parent question with subquestions
    """
    test = Test.objects.create(title="my test", description="my test description")
    question = Question.objects.create(test=test, question_text="my question")
    choice = Choice.objects.create(choice_text="choice", question=question)
    subquestion = Question.objects.create(test=test, question_text="my subquestion", parent=choice)
    self.assertIsNone(question.next_question())
    self.assertIsNone(subquestion.next_question())

  def test_next_question_with_multiple_questions(self):
    """
    next_question() returns the next parent question in order of creation with multiple questions, and none for the
    last created parent question
    """
    test = Test.objects.create(title="my test", description="my test description")
    question1 = Question.objects.create(test=test, question_text="my question 1")
    question2 = Question.objects.create(test=test, question_text="my question 2")
    question3 = Question.objects.create(test=test, question_text="my question 3")
    self.assertIs(question1.next_question().id, question2.id)
    self.assertIs(question2.next_question().id, question3.id)
    self.assertIsNone(question3.next_question())

  def test_next_question_with_multiple_questions_and_subquestions(self):
    """
    next_question() returns the next parent question in order of creation with multiple questions and multiple
    subquestions, and none for the last created parent question
    """
    test = Test.objects.create(title="my test", description="my test description")
    question1 = Question.objects.create(test=test, question_text="my question 1")
    question2 = Question.objects.create(test=test, question_text="my question 2")
    choice1 = Choice.objects.create(choice_text="choice", question=question1)
    subquestion1 = Question.objects.create(test=test, question_text="my subquestion 1", parent=choice1)
    choice2 = Choice.objects.create(choice_text="choice", question=subquestion1)
    subquestion2 = Question.objects.create(test=test, question_text="my subquestion 2", parent=choice2)
    self.assertIs(question1.next_question().id, question2.id)
    self.assertIs(subquestion1.next_question().id, question2.id)
    self.assertIs(subquestion2.next_question().id, question2.id)
    self.assertIsNone(question2.next_question())

class ChoiceModelTests(TestCase):
  def test_followup_question_no_subquestions(self):
    """
    followup_question() returns None when there are no subquestions
    """
    test = Test.objects.create(title="my test", description="my test description")
    question = Question.objects.create(test=test, question_text="my question")
    choice = Choice.objects.create(choice_text="choice", question=question)
    self.assertIsNone(choice.followup_question())

  def test_followup_question_one_choice_one_subquestion(self):
    """
    followup_question() returns the subquestion of the choice when there is one choice and one subquestion
    """
    test = Test.objects.create(title="my test", description="my test description")
    question = Question.objects.create(test=test, question_text="my question")
    choice = Choice.objects.create(choice_text="choice", question=question)
    subquestion = Question.objects.create(test=test, question_text="my subquestion", parent=choice)
    self.assertIs(choice.followup_question().id, subquestion.id)

  def test_followup_question_multiple_choices_one_subquestion(self):
    """
    followup_question() returns the subquestion of the choice when there are multiple choices and one subquestion
    """
    test = Test.objects.create(title="my test", description="my test description")
    question = Question.objects.create(test=test, question_text="my question")
    choice1 = Choice.objects.create(choice_text="choice1", question=question)
    choice2 = Choice.objects.create(choice_text="choice2", question=question)
    subquestion = Question.objects.create(test=test, question_text="my subquestion", parent=choice1)
    self.assertIs(choice1.followup_question().id, subquestion.id)
    self.assertIsNone(choice2.followup_question())

  def test_followup_question_multiple_choices_multiple_subquestion(self):
    """
    followup_question() returns the subquestion of the choice when there are multiple choices and multiple subquestions
    """
    test = Test.objects.create(title="my test", description="my test description")
    question = Question.objects.create(test=test, question_text="my question")
    choice1 = Choice.objects.create(choice_text="choice", question=question)
    choice2 = Choice.objects.create(choice_text="choice", question=question)
    subquestion1 = Question.objects.create(test=test, question_text="my subquestion", parent=choice1)
    choice3 = Choice.objects.create(choice_text="choice", question=question)
    choice4 = Choice.objects.create(choice_text="choice", question=question)
    subquestion2 = Question.objects.create(test=test, question_text="my subquestion", parent=choice4)
    self.assertIs(choice1.followup_question().id, subquestion1.id)
    self.assertIsNone(choice2.followup_question())
    self.assertIsNone(choice3.followup_question())
    self.assertIs(choice4.followup_question().id, subquestion2.id)

class TestIndexViewTests(TestCase):
  def test_no_tests(self):
    """
    If no tests exist, an appropriate message is displayed.
    """
    response = self.client.get(reverse('grading:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No tests are available.")
    self.assertQuerysetEqual(response.context['test_list'], [])

  def test_tests_exist(self):
    """
    Tests (and links to them) are displayed on the index page.
    """
    test = Test.objects.create(title="my test", description="my test description")
    Question.objects.create(test=test, question_text="my question")
    response = self.client.get(reverse('grading:index'))
    self.assertQuerysetEqual(response.context['test_list'], ['<Test: my test>'])

class QuestionDetailViewTests(TestCase):
  def test_single_question(self):
    """
    Question and choices are displayed
    """
    test = Test.objects.create(title="my test", description="my test description")
    question = Question.objects.create(test=test, question_text="screen broken?")
    choice1 = Choice.objects.create(choice_text="yes", question=question)
    choice2 = Choice.objects.create(choice_text="no", question=question)
    response = self.client.get(reverse('grading:question', args=(question.test.id, question.id,)))
    self.assertContains(response, question.question_text)
    self.assertContains(response, choice1.choice_text)
    self.assertContains(response, choice2.choice_text)
