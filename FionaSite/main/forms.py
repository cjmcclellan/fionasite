from django import forms


# forms for the relationships and task classes
class ContactForm(forms.Form):

    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True, max_length=200)
    message = forms.CharField(required=True)
