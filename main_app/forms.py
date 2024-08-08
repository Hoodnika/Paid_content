from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget

from main_app.models import Publication


class PublicationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autofocus': ''})

        self.fields['content'].widget = CKEditor5Widget(
            attrs={"class": "django_ckeditor_5"}, config_name="extends"
        )
        self.fields["content"].required = False

    class Meta:
        model = Publication
        fields = ('title', 'preview', 'description', 'slug', 'content')
