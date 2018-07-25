from django import forms
from .models import Contact

# class ContactForm(forms.Form):
#     name = forms.CharField(max_length=50, help_text='Enter Full Name',
#                            widget=forms.TextInput(attrs={
#                                'class': 'form-control'
#                            }))
#     email = forms.EmailField()
#     message = forms.CharField()
#     subcribe = forms.BooleanField()
#
#     email.widget.attrs.update({'class': 'form-control'})
#     message.widget.attrs.update({'class': 'form-control'})


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact

        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'})
        }
