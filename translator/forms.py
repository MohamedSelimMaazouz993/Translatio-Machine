from django import forms

class TranslationForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    target_language = forms.ChoiceField(choices=[('fr', 'French'), ('ar', 'Arabic')])
    pdf_file = forms.FileField(label='Upload PDF', required=False)
