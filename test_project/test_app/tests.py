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


class JsonateTests(TestCase):        
    maxDiff = 10**4
    def setUp(self):
        def destroy_media_folder(folder):
            path = join(settings.MEDIA_ROOT, folder)
            [unlink(f) for f in glob(join(path, "*"))]
            try: rmdir(path)
            except: pass
        
        destroy_media_folder("files")
        destroy_media_folder("images")
        
        self.user = User.objects.create_user("asdf", 'asdf@example.com', "password")
        self.model = MyModel(
                             foreign_key=self.user
                             )
        self.model.file_field.save("text_file.txt", ContentFile("Any Old Content"))
        self.model.image_field.save("image_file.wbm", ContentFile('\x00\x00\x01\x01\x80'))
        self.model.save()
    
    def assertJsonEqual(self, obj1, obj2, *args, **kwargs):
        obj1 = json.loads(obj1)
        
        if isinstance(obj2, basestring):
            obj2 = json.loads(obj2)
        
        self.assertEqual(obj1, obj2, *args, **kwargs)
    
    def test_basic_serialization(self):
        model_data = {
            u"float_field": 32.25, 
            u"normal_field1": u"field1", 
            u"normal_field2": u"field2", 
            u"boolean_field": True, 
            u"null_field": None, 
            u"decimal_field": 32.25,
            u"foreign_key": 1, 
            u"datetime_field": u"2011-01-11T11:11:11", 
            u"image_field": u"/media/images/image_file.wbm", 
            u"date_field": u"2011-01-11", 
            u"id": 1, 
            u"file_field": u"/media/files/text_file.txt"
        }
        print jsonate(self.model)
        #self.assertJsonEqual(jsonate(self.model), model_data)
        #self.assertJsonEqual(jsonate(MyModel.objects.all()), [model_data])
    