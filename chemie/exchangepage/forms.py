from django import forms
class IndexForm(forms.Form):
    OPTIONS = (
        (1, 'Solfaktor'),
        (2, 'Levekostnader'),
        (3, 'Tilgjengelighet'),
        (4, 'Natur'),
        (5, 'Gjestfrihet'),
        (6, 'Arbeidsmengde')
    )
    Indexfiltering = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS, required=False)