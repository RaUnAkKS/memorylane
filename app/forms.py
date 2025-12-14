from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Capsule,CapsuleComment,CapsuleEntry

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
class CapsuleForm(forms.ModelForm):
    class Meta:
        model = Capsule
        fields = [
            'title',
            'message',
            'theme',
            'unlock_type',
            'unlock_date',
            'unlock_event',
            'privacy',
            'recipients',
            'collaborators',
            'image',
            'video',
            'audio',
        ]
        widgets = {
            'unlock_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            )
        }
class CapsuleCommentForm(forms.ModelForm):
    class Meta:
        model = CapsuleComment
        fields = ['text','reaction']

class CollaboratorForm(forms.ModelForm):
    class Meta:
        model = Capsule
        fields = ['collaborators']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['collaborators'].queryset = User.objects.exclude(id=user.id)

class CapsuleEntryForm(forms.ModelForm):
    class Meta:
        model = CapsuleEntry
        fields = ['text', 'image', 'video', 'audio']
