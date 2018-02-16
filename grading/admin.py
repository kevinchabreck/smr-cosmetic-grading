from django.contrib import admin

from .models import Test, Question, Choice

# Register your models here.

class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 0

class QuestionAdmin(admin.ModelAdmin):
  inlines = [ChoiceInline]

admin.site.register(Test)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
