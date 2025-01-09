from django_recaptcha.widgets import ReCaptchaBase


class CssStyleFormMixin:
    fields = {}

    def _init_css_style_form_controls(self):
        for _, field in self.fields.items():
            # Skip ReCaptcha widget since it doesn't support custom attributes
            if isinstance(field.widget, ReCaptchaBase):
                continue
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += 'sign__input'
