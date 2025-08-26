from django.shortcuts import render, redirect

from .BaseCtl import BaseCtl
from ..models import Course
from ..service.CourseService import CourseService


class CourseListCtl(BaseCtl):

    def request_to_form(self, requestForm):
        count = 1

    def request_to_form(self, requestForm):
        self.form['name'] = requestForm.get('name', None)
        self.form['ids'] = requestForm.getlist('ids', None)

    def display(self, request, params={}):
        CourseListCtl.count = self.form['pageNo']
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list,'form': self.form})
        return res

    def next(self, request, params ={}):
        CourseListCtl.count += 1
        self.form['pageNo'] = CourseListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def previous(self, request, params = {}):
        CourseListCtl.count -= 1
        self.form['pageNo'] = CourseListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def new(self, request, params = {}):

        res = redirect('/ORS/Course/')
        return res

    def deleteRecord(self, request, params = {}):

        if not self.form['ids']:
            self.form['error'] = True
            self.form['message'] = "Please select atleast one check box"
        else:
            for id in self.form['ids']:
                id =int(id)
                course = self.get_service().get(id)
                if course:
                    self.get_service().delete(id)
                    self.form['error'] = False
                    self.form['message'] = "Data deleted successfully"

                else:
                    self.form['error'] = True
                    self.form['message'] = "Data deletion is not deleted"
        self.form['pageNo'] = 1
        records = self.get_service().search(self.form)
        self.page_list = records['data']
        self.form['lastId'] = Course.objects.last().id
        return render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})

    def submit(self, request, params={}):
        CourseListCtl.count = 1
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        if self.page_list == []:
            self.form['error'] = True
            self.form['message'] = "No record found"
        res = render(request, self.get_template(), {'pageList': self.page_list, 'form': self.form})
        return res

    def get_template(self):
        return "CourseList.html"

    def get_service(self):
        return CourseService()
