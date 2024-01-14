from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    ALLOWED_CHARS = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя- ')

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if not all(char in self.ALLOWED_CHARS for char in title):
            raise forms.ValidationError('Должны быть только: русские символы, дефис или пробел')
        return title
