# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from flask import make_response
from flask import jsonify
from pymongo import MongoClient


def connectcloud(address,port,database,user,password,collection_id):
    connection = MongoClient(address,port)
    db = connection[database]
    db.authenticate(user, password)
    collection = db[collection_id]
    return collection

def timetableDealing(data):
    Timetable = {}
    Timetable['Doctor_name'] = data['Doctor_name']
    Timetable['Date'] = data['Date']
    Timetable['Time'] = data['Time']
    Timetable['_id'] = data['_id']
    return Timetable

class Getdoctortimetable(Resource):
    def get(self):
        try:
            dbconnection = connectcloud('ds263089.mlab.com',63089,
                          'dentalclinic','admin','LIjiachen0717','DentalClinicTimetable')
            data = dbconnection.find({'Doctor_name' : g.args["Doctor"],'Status':'N','Date':g.args["Date"]})
            DoctorTimetable = []
            for item in data:
                DoctorTimetable.append(timetableDealing(item))
            if len(DoctorTimetable) == 0:
                return make_response(jsonify(message="Doctor Timetable Getting Fail"),404)
            return make_response(jsonify(message="OK",entities=DoctorTimetable),200)
        except:
            return make_response(jsonify(message="Interval Error"),500)
