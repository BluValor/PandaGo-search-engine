from django import forms


class QueryForm(forms.Form):
    query_text = forms.CharField(label='query text', max_length=200)
