import re
import random

class Mapping:
    def __init__(self,map:dict) -> None:
        self.__map = map
    
    def __str__(self) -> str:
        s = "{"
        for i in range(self.size()):
            key = self.keys()[i]
            if isinstance(key,str):
                s += f"'{key}': "
            else:
                s += f"{key}: "
            value = self.__map[key]
            if isinstance(value,str):
                s += f"'{value}'"
            else:
                s += f"{value}"
            if (i+1) < self.size():
                s += ", "
        s += "}"
        return s

    def __getitem__(self,key:str):
        return self.get(key)
    
    def __setitem__(self,key:str,value):
        return self.put(key,value)
    
    def put(self,key:str,value,if_absent=False):
        if if_absent:
            if not self.contains_key(key):
                self.__map[key] = value
            else:
                return False
        else:
            self.__map[key] = value
        return True
    
    def delete(self,key:str):
        value = self.__map[key]
        del self.__map[key]
        return value

    def get(self,key:str):
        return self.__map[key]

    def keys(self):
        return tuple(self.__map.keys())
    
    def values(self):
        return tuple(self.__map.values())

    def size(self):
        return len(self.__map.keys())
    
    def contains_key(self,key:str):
        return key in self.__map.keys()
    
    def contains_value(self,value):
        return value in self.__map.values()
    
    def filter(self,func):
        keys = filter(func,self.keys())
        new_map = Mapping({key: self.__map.get(key) for key in keys})
        return new_map
    
    def is_empty(self):
        return self.size() == 0
    
    def empty(self):
        self.__map.clear()

    def choice(self):
        if not self.is_empty():
            key = random.choice(self.keys())
            return self[key]