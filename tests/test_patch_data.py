from wtforms import (
    BooleanField,
    FieldList,
    Form,
    FormField,
    IntegerField,
    TextField,
)
from wtforms.form import WebobInputWrapper
from wtforms.validators import Required, Optional
from wtforms_json import MultiDict


class BooleanTestForm(Form):
    is_active = BooleanField(default=False, validators=[Optional()])
    is_confirmed = BooleanField(default=True, validators=[Required()])
    is_private = BooleanField(default=False, validators=[Required()])


class TestPatchedBooleans(object):
    def test_supports_false_values(self):
        form = BooleanTestForm.from_json(
            {'is_active': False, 'is_confirmed': True}
        )
        assert form.patch_data == {
            'is_active': False,
            'is_confirmed': True,
            'is_private': False
        }


class LocationForm(Form):
    name = TextField()
    longitude = IntegerField()
    latitude = IntegerField()


class EventForm(Form):
    name = TextField()
    location = FormField(LocationForm)
    attendees = IntegerField()
    attendee_names = FieldList(TextField())


class TestFormProcessAfterMonkeyPatch(object):
    def test_supports_webob_input_wrapper(self):
        json = {
            'name': 'some patched name'
        }
        form = EventForm(formdata=WebobInputWrapper(MultiDict(json)))
        assert form.data


class TestFormPatchData(object):
    def test_patch_data_with_missing_form_fields(self):
        json = {
            'name': 'some patched name'
        }
        form = EventForm.from_json(json)
        assert form.patch_data == json

    def test_patch_data_for_form_fields(self):
        json = {
            'name': 'some name',
            'location': {
                'name': 'some location'
            }
        }
        form = EventForm.from_json(json)
        assert form.patch_data == json

    def test_supports_field_lists(self):
        json = {
            'name': 'some name',
            'attendee_names': ['Something']
        }
        form = EventForm.from_json(json)
        assert form.patch_data == json

    def test_supports_null_values_for_form_fields(self):
        json = {
            'name': 'some name',
            'location': None
        }
        form = EventForm.from_json(json)
        assert form.patch_data == json

    def test_supports_null_values_for_regular_fields(self):
        json = {
            'name': 'some name',
            'attendees': None
        }
        form = EventForm.from_json(json)
        assert form.patch_data == json
