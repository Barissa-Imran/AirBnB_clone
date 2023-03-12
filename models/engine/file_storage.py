#!/usr/bin/python3
''' FileStorage module '''
import json
from models.base_model import BaseModel
import models
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    '''FileStorage class'''

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects.

        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if type(v) == cls:
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
        '''
        sets in objects with key classname.id
        Args:
            object
        '''
        self.__objects["{}.{}".format(obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        objdict = {o: self.__objects[o].to_dict() for o in
                   self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as JsonFile:
            json.dump(objdict, JsonFile)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for o in json.load(f).values():
                    name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(name)(**o))
        except FileNotFoundError:
            pass
