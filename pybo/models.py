from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# 질문 모델
class Question(models.Model):
    # cascade 설정이 되어 있으므로 계정이 삭제되면 계정과 연결된 Question 모델 데이터가
    # 모두 삭제된다
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_question')
    # 글자 수를 제한하려면 charfield()를 이용한다
    subject = models.CharField(max_length=200)
    # 글자 수를 제한하지 않으려면 textfield()를 이용한다
    content = models.TextField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')

    # method 가 추가된 경우에는 makemigrations, migrate 명령은 수행하지 않아도 된다
    def __str__(self):
        return self.subject


# 답변 모델
class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


# 답변 모델
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modified_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
