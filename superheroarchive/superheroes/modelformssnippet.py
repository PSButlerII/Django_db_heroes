from django.utils.safestring import mark_safe
from django.db import models
from django.template.defaultfilters import yesno, linebreaksbr, urlize
from django.utils.translation import get_date_formats
from django.utils.text import capfirst
from django.utils import dateformat

class ModelInfo(object):
    class _Meta:
        model = None
        fields = ()
        exclude = ()
        sections = None
        row_template = '<tr><th>%s</th><td>%s</td></tr>'
        show_if_none = False
        auto_urlize = True
        auto_linebreaks = True

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance

        self._meta = self.Meta()
        _meta = self._Meta()

        for attr in ('model','fields','exclude','sections','row_template','show_if_none',
                'auto_urlize','auto_linebreaks',):
            if not hasattr(self._meta, attr):
                setattr(self._meta, attr, getattr(_meta, attr))

    def get_model_fields(self):
        return [f.name for f in self._meta.model._meta.fields \
                if f.name != 'id' and \
                (f.name in self._meta.fields or \
                not f.name in self._meta.exclude)\
                ]

    def get_field(self, f_name):
        return [f for f in self._meta.model._meta.fields if f.name == f_name][0]

    def get_field_display_text(self, f_name):
        return self.get_field(f_name).verbose_name

    def get_field_display_value(self, f_name):
        field = self.get_field(f_name)

        try:
            return getattr(self, 'get_%s_value'%f_name)
        except:
            pass

        f_value = getattr(self.instance, f_name)

        if f_value is None:
            return None

        if callable(f_value):
            return f_value()
        
        if isinstance(f_value, models.Model):
            if self._meta.auto_urlize and hasattr(f_value, 'get_absolute_url'):
                return '<a href="%s">%s</a>'%(f_value.get_absolute_url(), f_value)
            else:
                return unicode(f_value)

        if field.choices:
            return dict(field.choices).get(f_value, None)

        if isinstance(field, models.BooleanField):
            return yesno(f_value)

        date_format, datetime_format, time_format = get_date_formats()

        if isinstance(field, models.DateTimeField):
            return capfirst(dateformat.format(f_value, datetime_format))

        if isinstance(field, models.TimeField):
            return capfirst(dateformat.time_format(f_value, time_format))

        if isinstance(field, models.DateField):
            return capfirst(dateformat.format(f_value, date_format))

        if isinstance(field, models.TextField):
            if self._meta.auto_urlize: f_value = urlize(f_value)
            if self._meta.auto_linebreaks: f_value = linebreaksbr(f_value)

        return f_value

    def as_string(self):
        ret = []

        sections = self._meta.sections or ((None, self._meta.fields or self.get_model_fields()),)

        for s_name, s_fields in sections:
            if s_name:
                ret.append(self._meta.row_template%('&nbsp;', '<h3>%s</h3>'%s_name))
                
            for f_name in s_fields:
                f_display = self.get_field_display_text(f_name)
                f_display = f_display[0] == f_display[0].lower() and f_display.capitalize() or f_display

                f_value = self.get_field_display_value(f_name)

                if self._meta.show_if_none or f_value is not None:
                    ret.append(self._meta.row_template%(f_display, f_value))

        return mark_safe('\n'.join(ret))

    def __unicode__(self):
        return self.as_string()

