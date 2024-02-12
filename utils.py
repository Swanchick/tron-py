import math

REGISTERED_OBJECTS = {}

class RegisterManager:
    @staticmethod
    def regist(classname, object):
        if classname in REGISTERED_OBJECTS.keys():
            return
        
        REGISTERED_OBJECTS[classname] = object
    
    @staticmethod
    def initialize_all(game):
        created_objects = []
        
        for object_classname in REGISTERED_OBJECTS.keys():
            object = REGISTERED_OBJECTS[object_classname](game, object_classname)
            object.start()
            created_objects.append(object)
        
        return created_objects


class Vector:
    @staticmethod
    def dist(pos1, pos2):
        x = pos2[0] - pos1[0]
        y = pos2[1] - pos1[1]
        
        return math.sqrt(x**2 + y**2)