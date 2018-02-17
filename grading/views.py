from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Test, Question, Choice

class IndexView(generic.ListView):
  template_name = 'grading/index.html'
  model = Test
  def get_context_data(self, **kwargs):

    for test in Test.objects.all():
      self.request.session['test'+str(test.id)] = {}
    return super().get_context_data(**kwargs)

class QuestionView(generic.DetailView):
  model = Question
  template_name = 'grading/question.html'

def submit(request, test_id, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    # Redisplay the question form.
    return render(request, 'grading/question.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    # save response to session
    request.session['test' + str(question.test.id)][str(question.id)] = str(selected_choice.id)
    # attempt to get followup (child) question
    followup_question = selected_choice.followup_question()
    if followup_question is not None:
      return HttpResponseRedirect(reverse('grading:question', args=(question.test.id, followup_question.id,)))
    elif question.next_question() is not None:
      # if no followup question, get next parent question in test
      return HttpResponseRedirect(reverse('grading:question', args=(question.test.id, question.next_question().id,)))
    else:
      # otherwise, test is complete
      return HttpResponseRedirect(reverse('grading:result', args=(question.test.id,)))

class ResultView(generic.DetailView):
  model = Test
  template_name = 'grading/result.html'

  def get_context_data(self, **kwargs):
    # pull responses out of session, put in context
    context = super().get_context_data(**kwargs)
    context['results'] = {}
    for question_id, choice_id in self.request.session['test'+str(self.object.id)].items():
      context['results'][Question.objects.get(id=question_id)] = Choice.objects.get(id=choice_id)
    return context
