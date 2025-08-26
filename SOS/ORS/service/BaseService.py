from abc import ABC, abstractmethod


class BaseService(ABC):
    def __init__(self):
        self.pageSize = 5

    def save(self, obj):
        if (obj.id == 0):
            obj.id == None
        obj.save()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        obj.delete()

    def get(self, obj_id):
        try:
            obj = self.get_model().objects.get(id=obj_id)  # we want to runmethod of a class whose object is creating, so here the get_method of present abstract class get overridden
            return obj
        except self.get_model().DoesNotExist:
            return None

    def search(self):
        try:
            obj = self.get_model().objects.all()
            return obj
        except self.get_model().DoesNotExist:
            return None

    @abstractmethod
    def get_model(self):
        pass

    def preload(self):
        try:
            obj = self.get_model().objects.all()
            return obj
        except self.get_model().DoesNotExist:
            return None

