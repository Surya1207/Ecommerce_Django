from django import forms

from store import models


class ReviewForm(forms.ModelForm):
    class Meta:
        fields = ["rating", "comment"]
        model = models.Review