from django import forms
import material as M
from .models import AbstractWord, Word, Category, Noun, Verb, Adjective


class WordInput(forms.ModelForm):
    layout = M.Layout(
        M.Row("word"),
        M.Row("explanations"),
        M.Row("picture"),
        M.Row("secret"),
        M.Row("category"),
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False, label = "Kategori", widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Word
        fields = ("word", "explanations", "picture", "secret", "category")


class NounInput(forms.ModelForm):
    layout = M.Layout(
        M.Row("word"),
        M.Row("definite_singular"),
        M.Row("indefinite_plural"),
        M.Row("definite_plural"),
        M.Row("explanations"),
        M.Row("picture"),
        M.Row("secret"),
        M.Row("category"),
    )

    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False, label = "Kategori", widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Noun
        fields = (
            "word",
            "explanations",
            "picture",
            "secret",
            "category",
            "indefinite_plural",
            "definite_singular",
            "definite_plural",
        )


class VerbInput(forms.ModelForm):
    layout = M.Layout(
        M.Row("word"),
        M.Row("present"),
        M.Row("past"),
        M.Row("future"),
        M.Row("explanations"),
        M.Row("picture"),
        M.Row("secret"),
        M.Row("category"),
        
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False, label = "Kategori", widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Verb
        fields = (
            "word",
            "explanations",
            "picture",
            "secret",
            "category",
            "present",
            "past",
            "future",
        )


class AdjectiveInput(forms.ModelForm):
    layout = M.Layout(
        M.Row("word"),
        M.Row("comparative"),
        M.Row("superlative"),
        M.Row("explanations"),
        M.Row("picture"),
        M.Row("secret"),
        M.Row("category"),
        
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), required=False, label = "Kategori", widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Adjective
        fields = (
            "word",
            "explanations",
            "picture",
            "secret",
            "category",
            "comparative",
            "superlative",
        )


class WordSearchMainPage(forms.Form):
    the_word = forms.CharField(max_length=120, required=False)


class CategorySortingMainPage(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False, label=" "
    )


class CategoryInput(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"


class CheckWhatFormForm(forms.Form):
    choice = forms.ChoiceField(
        choices=(
            (0, "Ikke valgt"),
            (1, "Et annet type ord"),
            (2, "Verb"),
            (3, "Substantiv"),
            (4, "Adjektiv"),
        ),
        label="",
        required=True,
    )
