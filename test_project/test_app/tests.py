from os import unlink, rmdir
from os.path import join
from glob import glob
import json
import unittest

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.forms import ModelForm

from jsonate import jsonate

from .models import MyModel, MyModelWithJsonateField, WithJsonateFieldExpectingList

def destroy_media_folder(folder):
    path = join(settings.MEDIA_ROOT, folder)
    [unlink(f) for f in glob(join(path, "*"))]
    try: rmdir(path)
    except: pass
            
class JsonateTests(TestCase):        
    maxDiff = 10**4
    def setUp(self):
        destroy_media_folder("files")
        destroy_media_folder("images")
        
        self.user = User.objects.create_user("asdf", 'asdf@example.com', "password")
        self.model = MyModel(
                             foreign_key=self.user
                             )
        self.model.file_field.save("text_file.txt", ContentFile("Any Old Content"))
        self.model.image_field.save("image_file.wbm", ContentFile('\x00\x00\x01\x01\x80'))
        self.model.save()
    
    def tearDown(self):
        destroy_media_folder("files")
        destroy_media_folder("images")
    
    def assertJsonEqual(self, obj1, obj2, *args, **kwargs):
        obj1 = json.loads(obj1)
        
        if isinstance(obj2, basestring):
            obj2 = json.loads(obj2)
        
        self.assertEqual(obj1, obj2, *args, **kwargs)

    def test_jsonate_field(self):
        def assertJSONField(to_write):
            obj.some_json_data = to_write
            obj.save()

            expected = json.loads(to_write) if isinstance(to_write, basestring) else to_write

            self.assertEqual(
                MyModelWithJsonateField.objects.first().some_json_data,
                expected
            )

        obj = MyModelWithJsonateField(some_name="test row with json data")

        test_data = [
            None,
            {"red":3, "orange":451},
            [{"red":3, "orange":451}, {"green":"dark", "white":"bright"}, None, ["A", "B"]],
            '["house", "mouse", "strauss"]'
        ]

        for td in test_data:
            assertJSONField(td)

        # all together
        assertJSONField(test_data)

    def assertJsonateFieldForm(self, model_class, data_to_store):
        class JsonateFieldForm(ModelForm):
            class Meta:
                model = model_class
                fields = '__all__'

        f = JsonateFieldForm({
            "some_json_data": json.dumps(data_to_store),
            "some_name": "testing form"
        })

        self.assertTrue(f.is_valid())
        f.save()

        self.assertEqual(
            model_class.objects.first().some_json_data,
            data_to_store
        )

    def test_jsonate_field_clean_form(self):
        dict_to_store = {"red":3, "orange":451}
        self.assertJsonateFieldForm(MyModelWithJsonateField, dict_to_store)

    def test_jsonate_field_clean_form_with_validation(self):
        list_to_store = ["house", "mouse", "strauss"]
        self.assertJsonateFieldForm(WithJsonateFieldExpectingList, list_to_store)

    def test_jsonate_field_in_values_list_gets_deserialized(self):
        # works this way since django 1.8
        expected = []
        for i in range(0, 5):
            to_create = {"some_name": u"name{}".format(i), "some_json_data":{u"item_{}".format(i): i}}
            MyModelWithJsonateField.objects.create(**to_create)
            expected.append((to_create["some_name"], to_create["some_json_data"]))

        vl = MyModelWithJsonateField.objects.order_by("id").values_list("some_name", "some_json_data")
        for (index, elem) in enumerate(vl):
            self.assertEqual(elem, expected[index])

    def test_basic_serialization(self):
        mymodel_data = {
            u"float_field": 32.25,
            u"normal_field1": u"field1",
            u"normal_field2": u"field2",
            u"boolean_field": True,
            u"null_field": None,
            u"decimal_field": 32.25,
            u"foreign_key": 1,
            u"datetime_field": u"2011-01-11T11:11:11",
            u"image_field": u"images/image_file.wbm",
            u"date_field": u"2011-01-11",
            u"id": 1,
            u"file_field": u"files/text_file.txt"
        }

        self.assertJsonEqual(jsonate(self.model), mymodel_data)
        self.assertJsonEqual(jsonate(MyModel.objects.all()), [mymodel_data])
        
        user_data_values = [{
            "username": 'asdf',
            "password": self.user.password
        }]
        self.assertJsonEqual(
            jsonate(User.objects.values("username", "password")),
            user_data_values
        )

        user_data_values_list = [['asdf']]
        self.assertJsonEqual(
            jsonate(User.objects.values_list("username")),
            user_data_values_list
        )

        user_data_values_list_flat = ['asdf']
        self.assertJsonEqual(
            jsonate(User.objects.values_list("username", flat=True)),
            user_data_values_list_flat
        )

from django.core import management

if __name__ == "__main__":
    management.call_command("migrate")

    unittest.main()