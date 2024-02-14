import math

REGISTERED_OBJECTS = {}

class RegisterManager:
    @staticmethod
    def regist(classname, object, create_on_start=True):
        if classname in REGISTERED_OBJECTS.keys():
            return
        
        REGISTERED_OBJECTS[classname] = (object, create_on_start)
    
    @staticmethod
    def initialize_all(game):
        created_objects = []
        
        for object_classname in REGISTERED_OBJECTS.keys():
            options = REGISTERED_OBJECTS[object_classname]
            if not options[1]:
                continue
            
            object = options[0](game, object_classname)
            object.start()
            created_objects.append(object)
        
        return created_objects
    
    @staticmethod
    def initialize_object(game, classname):
        if not classname in REGISTERED_OBJECTS:
            return
        
        object = REGISTERED_OBJECTS[classname][0](game, classname)
        
        return object 


class Vector:
    @staticmethod
    def dist(pos1, pos2):
        x = pos2[0] - pos1[0]
        y = pos2[1] - pos1[1]
        
        return math.sqrt(x**2 + y**2)