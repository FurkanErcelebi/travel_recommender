import os
import csv
import re

from .models import Host
from utils.models import Property
from django.db.models.fields import IntegerField, FloatField, CharField, BooleanField, DateField
from django.db.models import ForeignKey
from dateutil.parser import parse
import datetime


def is_date(value):
    try: 
        parse(value, fuzzy=False)
        return True
    except ValueError:
        return False


def get_as_float(value):
        if re.search("^(-)*\d+\.\d+$", value):
            return float(value)
        elif re.search("^(-)*\d+$", value):
            return float(int(value))
        return 0.0

    
def get_as_int(value):
        if re.search("^(-)*\d+$", value):
            return int(value)
        elif re.search("^(-)*\d+\.\d+$", value):
            return int(float(value))
        return 0


def create_new_host(row, field_list):
    new_host = Host()
    model_field_list = [ field for field in Host._meta.get_fields() ]
    for i in range(len(field_list)):
        the_field = [ model_field for model_field in model_field_list if model_field.name == field_list[i] ][0]
        #print(f'set {the_field.name} value')
        if the_field.__class__ == IntegerField:
            setattr(new_host, the_field.name, get_as_int(row[i]))
        elif the_field.__class__ == FloatField:
            setattr(new_host, the_field.name, get_as_float(row[i]))
        elif the_field.__class__ == CharField:
            setattr(new_host, the_field.name, row[i])
        elif the_field.__class__ == BooleanField:
            setattr(new_host, the_field.name, True if row[i] == 't' else False)
        elif the_field.__class__ == DateField:
            dates = row[i].split('-')
            if len(dates) == 3:
                setattr(new_host, the_field.name, datetime.date(int(dates[0]), int(dates[1]), int(dates[2])))
        elif the_field.__class__ == ForeignKey:
            properties = Property.objects.filter(label__iexact = row[i].strip())
            setattr(new_host, the_field.name, properties[0])
            
        else:
            print(f'{the_field.name} have not type of values')
    
    new_host.save()
    print(f'host {new_host.id} is created')


def import_datas_to_host():
    # 13062l rows imported , look after the others 
    with open('{}/static/host_info/host.csv'.format(os.getcwd().replace('\\', '/')), encoding='ISO-8859-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        field_list = []
        try:
            for row in csv_reader:
                if line_count == 0:
                    field_list = row
                else:
                    create_new_host(row, field_list)

                
                line_count += 1
                

        except Exception as e:
            print('import_datas_to_host error: ', e)
        
        print(f'Processed {line_count - 1} lines.')
        
def import_datas_to_host_for_string_size():
    with open('../static/host_info/host.csv', encoding='ISO-8859-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        string_fields = { 'name' : 0,'host_location': 0, 'host_response_time': 0, 'neighborhood': 0, 'district': 0, 'city': 0, 'room_type': 0,'amenities': 0,}
        string_field_keys = list(string_fields.keys())
        string_field_positions = []
        try:
            for row in csv_reader:
                if line_count == 0:
                  for i in range(len(row)):
                      if row[i] in string_field_keys:
                          string_field_positions.append(i)
                else:
                  for i in range(len(row)):
                      pst = [ j for j in range(len(string_field_positions)) if string_field_positions[j] == i]
                      if len(pst) == 1:
                          if string_fields[string_field_keys[pst[0]]] < len(row[i]):
                              string_fields[string_field_keys[pst[0]]] = len(row[i])

                
                line_count += 1
                

        except Exception as e:
            print("Max Length Exception")
            print(e)
        
        print(line_count)
        print(string_fields)