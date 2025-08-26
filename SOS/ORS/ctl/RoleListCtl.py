from django.shortcuts import render, redirect

from .BaseCtl import BaseCtl
from ..service.RoleService import RoleService


class RoleListCtl(BaseCtl):

    count = 1

    def request_to_form(self, requestForm):
        self.form['ids'] = requestForm.getlist('ids', None)
        self.form['name'] = requestForm['name']

    def display(self, request, params={}):
        RoleListCtl.count = self.form['pageNo']
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {'pageList':self.page_list, 'form':self.form})
        return res

    def next(self, request, params ={}):
        RoleListCtl.count += 1
        self.form['pageNo'] = RoleListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {"pageList": self.page_list, 'form': self.form})
        return res

    def previous(self,request, params = {}):
        RoleListCtl.count -= 1
        self.form['pageNo'] = RoleListCtl.count
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        res = render(request, self.get_template(), {'pagelist': self.page_list, 'form': self.form})
        return res

    def new(self, request, params ={}):

        res = redirect("/ORS/RoleList/")
        return res

    def delete(self, request, params ={}):
        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select at least one checkbox"
        else:
            for id in self.form['ids']:
                id = int(id)
                record = self.get_service().get(id)
                if record:
                    self.get_service().delete(id)
                    self.form['message'] = "Data has been deleted successfully"
                else:
                    self.form['error'] = True
                    self.form['message'] = "Data was not deleted"

        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def submit(self, request, params={}):
        RoleListCtl.count = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        if self.page_list == []:
            self.form['message'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_service(self):
        return RoleService()

    def get_template(self):
        return "Rolelist.html"




