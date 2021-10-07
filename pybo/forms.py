from django import forms
from pybo.models import Question, Answer, Comment


# ModelForm 을 상속받아 모델폼을 만듬
# 모델과 연결된 폼이며, 연결된 모델의 데이터를 저장할 수 있다.
# 모델폼은 반드시 내부 클래스로 Meta 클래스를 가져야 한다.
# 그리고 Meta 클래스에는 모델폼이 사용할 model 과 field 를 적어야 한다
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        """
        widgets = {
            'subject': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'rows': 10}),
        }
        """
        labels = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
        