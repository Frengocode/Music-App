from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import CustomUser, CommentModel, GetPrimePluse
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'First Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'Second Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    def clean_music(self):
        music_file = self.cleaned_data.get('music')
        if music_file:
            if not music_file.name.endwith('.mp3'):
                raise forms.ValidationError('Файл не является mp3')
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'play_list', 'anonim_play_list', 'email', 'country']

    

class ProfilePhotoForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_photo']


class CommentForm(forms.ModelForm):

    text = forms.CharField(widget=forms.TextInput({'class':'Комментария'}))


    def clean_text(self):
        comment = self.cleaned_data['text']
        symbols = '~`!@#$%^&*()_++|[?<>'

        for symbol in symbols:
            if symbol in comment:
                raise forms.ValidationError('Вы не можете использовать символы в комментарии')
        return comment
        

    class Meta:
        model = CommentModel
        fields = ['text']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, label='Search...')


class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'play_list', 'anonim_play_list', 'country']


class PrimePluseForm(ModelForm):
    class Meta:
        model = GetPrimePluse
        fields = '__all__'  # Исправлена опечатка в атрибуте fields
        exclude = ('user',)

    def clean_age(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')  # Получение значения поля 'age' из очищенных данных

        if age is not None and age < 10:  # Проверка наличия значения и его корректности
            raise forms.ValidationError('Вы Ещё Не Совершено Летний Для Этого Сайта')

        return age  # Возвращаем значение, если оно прошло проверку
