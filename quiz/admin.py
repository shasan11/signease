from django.contrib import admin
from .models import Chapter, Quiz, Question, Option, QuizAttempt, QuestionResponse

# Bottom level inlines first
class OptionInline(admin.TabularInline):
    model = Option
    extra = 0
    min_num = 2
    fields = ('text', 'is_correct',)
    verbose_name = "Answer Option"
    verbose_name_plural = "Answer Options"

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    min_num = 1
    fields = ('text', 'explanation', 'marks',)
    verbose_name = "Quiz Question"
    verbose_name_plural = "Quiz Questions"

class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 0
    fields = ('title', 'description', 'is_published',)
    show_change_link = True
    verbose_name = "Chapter Quiz"
    verbose_name_plural = "Chapter Quizzes"

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('number', 'title')
    search_fields = ('title',)
    inlines = [QuizInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'title', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'chapter__title')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text_truncated', 'marks')
    list_filter = ('quiz__chapter',)
    search_fields = ('text', 'quiz__title')
    inlines = [OptionInline]

    def text_truncated(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_truncated.short_description = "Question Text"

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'text_truncated', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text', 'question__text')

    def text_truncated(self, obj):
        return obj.text[:30] + '...' if len(obj.text) > 30 else obj.text
    text_truncated.short_description = "Option Text"

# User attempt tracking admins
class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse
    extra = 0
    readonly_fields = ('question', 'selected_option', 'is_correct')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'started_at', 'completed_at')
    list_filter = ('quiz__chapter',)
    search_fields = ('user__username', 'quiz__title')
    readonly_fields = ('user', 'quiz', 'started_at')
    inlines = [QuestionResponseInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct')
    list_filter = ('is_correct',)
    readonly_fields = ('attempt', 'question', 'selected_option', 'is_correct')

    def has_add_permission(self, request):
        return False
