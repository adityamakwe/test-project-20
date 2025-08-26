from django.shortcuts import render

from .BaseCtl import BaseCtl
from ..models import College
from ..service.CollegeService import CollegeService
from ..utility.DataValidator import DataValidator


class CollegeCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['name'] = requestForm['name']
        self.form['address'] = requestForm['address']
        self.form['state'] = requestForm['state']
        self.form['city'] = requestForm['city']
        self.form['phoneNumber'] = requestForm['phoneNumber']

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.address = self.form['address']
        obj.state = self.form['state']
        obj.city = self.form['city']
        obj.phoneNumber = self.form['phoneNumber']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['address'] = obj.address
        self.form['state'] = obj.state
        self.form['city'] = obj.city
        self.form['phoneNumber'] = obj.phoneNumber

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form["name"])):
            inputError["name"] = "College Name is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["state"])):
            inputError["state"] = "state is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["city"])):
            inputError["city"] = "city is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["phoneNumber"])):
            inputError["phoneNumber"] = "Phone Number is required"
            self.form["error"] = True


        return self.form['error']

    def display(self, request, params={}):
        res = render(request, self.get_template(), {'form': self.form})
        return res

    def submit(self, request, params={}):
        if (params['id'] > 0):
            pk = params['id']
            duplicate = self.get_service().get_model().objects.exclude(id=pk).filter(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "College Name already exists"
                res = render(request, self.get_template(), {"form": self.form})
            else:
                college = self.form_to_model(College())
                self.get_service().save(college)
                self.form['id'] = college.id
                self.form['error'] = False
                self.form['message'] = "College updated successfully"
                res = render(request, self.get_template(), {'form': self.form})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(name=self.form['name'])
            if duplicate.count() > 0:
                self.form['error'] = True
                self.form['message'] = "College Name already exists"
                res = render(request, self.get_template(), {'form': self.form})
            else:
                college = self.form_to_model(College())
                self.get_service().save(college)
                self.form['message'] = False
                self.form['message'] = "College saved successfully"
                res = render(request, self.get_template(), {'form': self.form})
            return res

    def get_template(self):
        return "College.html"

    def get_service(self):
        return CollegeService()

