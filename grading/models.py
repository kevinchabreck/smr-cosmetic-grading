from django.db import models
from django.contrib.contenttypes.models import ContentType

class Test(models.Model):
  title = models.CharField(max_length=200)
  description = models.CharField(max_length=200)

  def __str__(self):
    return self.title

  def first_question(self):
    return self.question_set.order_by('id').first()


class Question(models.Model):
  test = models.ForeignKey(Test, on_delete=models.CASCADE)
  # if a question is a subquestion, it will have a choice fk
  parent = models.ForeignKey('Choice', on_delete=models.CASCADE, blank=True, null=True, related_name='followupquestion')
  question_text = models.CharField(max_length=200)

  def __str__(self):
    return self.question_text

  def root_question(self):
    if self.parent is None:
      return self
    else:
      return self.parent.question.root_question()

  def next_question(self):
    next_questions = Question.objects.filter(test_id=self.test.id).filter(parent__isnull=True).filter(
      id__gt=self.root_question().id).order_by('id')[0:1]
    return next_questions[0] if next_questions else None


class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)

  def followup_question(self):
    followup_questions = Question.objects.filter(parent_id=self.id)
    return followup_questions[0] if followup_questions else None

  def __str__(self):
    return self.question.question_text+' '+self.choice_text
