from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CreateUser(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
        "username", 
        "email",
        "password1",
        "password2",
        "press", 
        "weight", 
        "array",
        "sound",
        "connect",
        ]
        labels = {
            'username' : '아이디',
            'email' : '이메일 ',
            'press' : '키압',
            'weight': '무게',
            'array': '배열',
            'sound': '소리',
            'connect': '연결',
            }
class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'press', 'weight', 'array', 'sound','connect',]
        labels = {
                'username' : '아이디',
                'email' : '이메일 ',
                'press' : '키압',
                'weight': '무게',
                'array': '배열',
                'sound': '소리',
                'connect': '연결',
                }