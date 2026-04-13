from django import forms

class SpinWheelForm(forms.Form):
    alternativer = forms.CharField(
        label="Skriv inn alternativer, ett per linje",
        widget=forms.Textarea(
            attrs={
                "rows": 12,
                "placeholder": "Matte\nKjemi\nKlesvask\nTrene\nHandle",
                "style": "width: 100%; font-size: 1.1em;"
            }
        )
    )

    