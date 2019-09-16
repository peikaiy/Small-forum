from django import forms

from user.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["nickname", "password", "icon", "age", "sex"]

    password2 = forms.CharField(max_length=128, min_length=6)

    def clean_password2(self):
        """二次密码验证"""
        cleaned_data = super().clean()
        print(cleaned_data)
        password2 = cleaned_data.get("password2")
        password = cleaned_data.get("password")
        if password != password2:
            raise forms.ValidationError("两次密码不一致")
