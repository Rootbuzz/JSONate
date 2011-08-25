from os import unlink, rmdir
from os.path import join
from glob import glob
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from test_app.models import MyModel
from jsonate import jsonate
import json

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
    
    def test_basic_serialization(self):
        mymodel_data = {
            "float_field": 32.25, 
            "normal_field1": "field1", 
            "normal_field2": "field2", 
            "boolean_field": True, 
            "null_field": None, 
            "decimal_field": 32.25,
            "foreign_key": 1, 
            "datetime_field": "2011-01-11T11:11:11", 
            "image_field": "images/image_file.wbm", 
            "date_field": "2011-01-11", 
            "id": 1, 
            "file_field": "files/text_file.txt"
        }
        self.assertJsonEqual(jsonate(self.model), mymodel_data)
        self.assertJsonEqual(jsonate(MyModel.objects.all()), [mymodel_data])
        
        user_data = [{
            "username": 'asdf',
            "password": self.user.password
        }]
        self.assertJsonEqual(jsonate(User.objects.values("username", "password")), user_data)
    