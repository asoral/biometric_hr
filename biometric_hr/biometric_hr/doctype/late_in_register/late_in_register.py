# -*- coding: utf-8 -*-
# Copyright (c) 2019, VHRS and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe,os,base64
import requests
import datetime
import json,calendar
from datetime import datetime,timedelta,date,time
import datetime as dt
from frappe.utils import cint,today,flt,date_diff,add_days,add_months,date_diff,getdate,formatdate,cint,cstr,today
from frappe.desk.notifications import delete_notification_count_for
from frappe import _
from frappe.model.document import Document

class LateINRegister(Document):
    pass





@frappe.whitelist()
def update_time_details():
    # day = add_days(today,-1)
    from_date = (datetime.strptime('2019-06-01', '%Y-%m-%d')).date()
    to_date = (datetime.strptime('2019-06-30', '%Y-%m-%d')).date()
    for day in daterange(from_date, to_date):
        print day
        att = frappe.get_all("Attendance",{'attendance_date':day})
        for a in att:
            doc= frappe.get_doc("Attendance",a)
            if doc:
                employee = frappe.get_doc("Employee",doc.employee)
                shift_type = frappe.get_doc("Shift Type", employee.shift)
                if doc.in_time:
                    in_time = datetime.strptime(doc.in_time,'%H:%M:%S')
                    deduction_hours = ""
                    in_time = timedelta(hours=in_time.hour,minutes=in_time.minute,seconds=in_time.second)
                    if in_time > shift_type.max_permission_time:
                        in_time = in_time - shift_type.max_permission_time
                        bs = frappe.get_single("Biometry Settings")
                        if bs.minimum_lateness_time:
                            min_lt = datetime.strptime(bs.minimum_lateness_time,'%H:%M:%S')
                            min_lt = timedelta(hours=min_lt.hour,minutes=min_lt.minute,seconds=min_lt.second)
                        if bs.maximum_lateness_time:
                            max_lt = datetime.strptime(bs.maximum_lateness_time,'%H:%M:%S')
                            max_lt = timedelta(hours=max_lt.hour,minutes=max_lt.minute,seconds=max_lt.second)
                        if bs.minimum_lateness_time and bs.maximum_lateness_time:
                            if in_time > min_lt and in_time < max_lt:
                                deduction_hours = bs.minimum_deduction_hours
                            elif in_time > max_lt:
                                deduction_hours = bs.maximum_deduction_hours
                        elif bs.minimum_lateness_time:
                            if in_time > min_lt:
                                deduction_hours = bs.minimum_deduction_hours
                        elif bs.maximum_lateness_time:
                            if in_time > max_lt:
                                deduction_hours = bs.maximum_deduction_hours
                        if frappe.db.exists("Late IN Register",{"employee": doc.employee,"attendance_date":doc.attendance_date}):
                            late_in = frappe.get_doc("Late IN Register",{"employee": doc.employee,"attendance_date":doc.attendance_date})
                        else:
                            late_in = frappe.new_doc("Late IN Register")
                        late_in.update({
                            "employee": doc.employee,
                            "biometric_id": employee.biometric_id,
                            "shift": employee.shift,
                            "in_time": doc.in_time,
                            "attendance_date": doc.attendance_date,
                            "late_in": in_time,
                            "deduction_hours": deduction_hours
                        })
                        late_in.save(ignore_permissions=True)

                if doc.out_time:
                    out_time = datetime.strptime(doc.out_time,'%H:%M:%S')
                    out_time = timedelta(hours=out_time.hour,minutes=out_time.minute,seconds=out_time.second)
                    deduction_hours = ""
                    if out_time < shift_type.end_time:
                        out_time = shift_type.end_time - out_time 
                        bs = frappe.get_single("Biometry Settings")
                        if bs.minimum_early_out_time:
                            min_eo = datetime.strptime(bs.minimum_early_out_time,'%H:%M:%S')
                            min_eo = timedelta(hours=min_eo.hour,minutes=min_eo.minute,seconds=min_eo.second)
                        if bs.maximum_early_out_time:
                            max_eo = datetime.strptime(bs.maximum_early_out_time,'%H:%M:%S')
                            max_eo = timedelta(hours=max_eo.hour,minutes=max_eo.minute,seconds=max_eo.second)
                        if bs.minimum_early_out_time and bs.maximum_early_out_time:
                            if out_time > min_eo and in_time < max_eo:
                                deduction_hours = bs.eo_min_deduction
                            elif out_time > max_eo:
                                deduction_hours = bs.eo_max_deduction
                        elif bs.minimum_early_out_time:
                            if out_time > min_eo:
                                deduction_hours = bs.eo_min_deduction
                        elif bs.maximum_early_out_time:
                            if out_time > max_eo:
                                deduction_hours = bs.eo_max_deduction
                        if frappe.db.exists("Early OUT Register",{"employee": doc.employee,"attendance_date":doc.attendance_date}):
                            early_out = frappe.get_doc("Early OUT Register",{"employee": doc.employee,"attendance_date":doc.attendance_date})
                        else:
                            early_out = frappe.new_doc("Early OUT Register")
                        early_out.update({
                            "employee": doc.employee,
                            "biometric_id": employee.biometric_id,
                            "shift": employee.shift,
                            "out_time": doc.out_time,
                            "attendance_date": doc.attendance_date,
                            "early_out": out_time,
                            "deduction_hours": deduction_hours
                        })
                        early_out.save(ignore_permissions=True)

            # if doc.in_time and not doc.out_time:
            #     if doc.attendance_date == today():
            #         pass
            #     else:
            #         if frappe.db.exists("Early OUT Register",{"employee": doc.employee,"attendance_date":doc.attendance_date}):
            #             early_out = frappe.get_doc("Early OUT Register",{"employee": doc.employee,"attendance_date":doc.attendance_date})
            #         else:
            #             early_out = frappe.new_doc("Early OUT Register")
            #         early_out.update({
            #             "employee": doc.employee,
            #             "biometric_id": employee.biometric_id,
            #             "shift": employee.shift,
            #             "attendance_date": doc.attendance_date,
            #             "early_out": "No Punch-Out"
            #         })
            #         early_out.save(ignore_permissions=True)

            # if doc.in_time and doc.out_time:   
            #     in_time = datetime.strptime(doc.in_time,'%H:%M:%S') 
            #     in_time = timedelta(hours=in_time.hour,minutes=in_time.minute,seconds=in_time.second)
            #     out_time = datetime.strptime(doc.out_time,'%H:%M:%S') 
            #     out_time = timedelta(hours=out_time.hour,minutes=out_time.minute,seconds=out_time.second)
            #     if in_time <= shift_type.max_permission_time and out_time >= shift_type.end_time:
            #         if frappe.db.exists("Early OUT Register",{"employee": doc.employee,"attendance_date":doc.attendance_date}):
            #             early_out = frappe.get_doc("Early OUT Register",{"employee": doc.employee,"attendance_date":doc.attendance_date})
            #             frappe.delete_doc("Early OUT Register",early_out.name)
            #         if frappe.db.exists("Late IN Register",{"employee": doc.employee,"attendance_date":doc.attendance_date}):
            #             late_in = frappe.get_doc("Late IN Register",{"employee": doc.employee,"attendance_date":doc.attendance_date})
            #             frappe.delete_doc("Late IN Register",late_in.name)    

def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


                        


