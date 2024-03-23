#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Represent an abstracted storage engine
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return the list of objects of one type of class.
        """
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            class_dict = {}
            for keys, value in self.__objects.items():
                if type(value) == cls:
                    class_dict[keys] = value
            return class_dict
        return self.__objects

    def new(self, obj):
        """Set in __objects obj"""
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        odict = {o: self.__objects[o].to_dict() for o in self.__objects.keys()}
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(odict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for value in json.load(f).values():
                    name = value["__class__"]
                    del value["__class__"]
                    self.new(eval(name)(**value))
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects, if it inside."""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """Call the reload method."""
        self.reload()
