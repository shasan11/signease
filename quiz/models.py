from django.db import models
from django.contrib.auth.models import User

class Chapter(models.Model):
     
    title = models.CharField(
        max_length=100,
        verbose_name="Chapter Title"
    )
    number = models.PositiveIntegerField(
        help_text="Chapter number",
        verbose_name="Chapter Number"
    )

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
         
        ordering = ['number']

    def __str__(self):
        return self.title

class Quiz(models.Model):
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='quizzes',
        verbose_name="Chapter"
    )
    title = models.CharField(
        max_length=100,
        verbose_name="Quiz Title"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Is Published"
    )

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"

class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Quiz"
    )
    text = models.TextField(verbose_name="Question Text")
    explanation = models.TextField(
        blank=True,
        help_text="Optional explanation for the correct answer",
        verbose_name="Explanation"
    )
    marks = models.PositiveIntegerField(
        default=1,
        verbose_name="Marks"
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"Question: {self.text[:50]}"

class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name="Question"
    )
    text = models.CharField(
        max_length=255,
        verbose_name="Option Text"
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Is Correct Answer"
    )

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='quiz_attempts',
        verbose_name="User"
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name="Quiz"
    )
    score = models.PositiveIntegerField(
        default=0,
        verbose_name="Score"
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Started At"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Completed At"
    )

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

class QuestionResponse(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name="Quiz Attempt"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Question"
    )
    selected_option = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Selected Option"
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Is Correct"
    )

    class Meta:
        verbose_name = "Question Response"
        verbose_name_plural = "Question Responses"
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"Response by {self.attempt.user.username} to Q{self.question.id}"

