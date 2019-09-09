from __future__ import unicode_literals
import frappe,os,base64
import requests
import datetime
import json,calendar
from datetime import datetime,timedelta,date,time
import datetime as dt
from frappe.utils import cint,today,flt,date_diff,add_days,get_first_day,get_last_day,add_months,date_diff,getdate,formatdate,cint,cstr
from frappe.desk.notifications import delete_notification_count_for
from frappe import _



@frappe.whitelist()
def calcute_latein_earlyout():
    cur_date = today()
    pre_mnth = add_months(cur_date,-1)
    first_day = get_first_day(pre_mnth)
    last_day = get_last_day(pre_mnth)
    employees = frappe.get_list("Employee", {'status':"Active"},['name','holiday_list'])
    for emp in employees:
        disciplinary_measure= ""
        late_in_count = 0
        early_out_count = 0
        monthly_occ_count = 0
        late_in_count_for_3month = 0
        early_out_count_for_3month = 0
        occ_count_for_3month = 0
        total_late_in_deduction_hours = 0
        total_early_out_deduction_hours = 0.0
        total_deduction_hours = 0.0
        total_deduction_amount = 0
        cum_late_in = "00:00:0"
        cum_late_in = cum_late_in.split(":")
        cum_late_in = timedelta(hours =cint(cum_late_in[0]),minutes=cint(cum_late_in[1])).total_seconds()
        cum_early_out = "00:00:0"
        cum_early_out = cum_early_out.split(":")
        cum_early_out = timedelta(hours =cint(cum_early_out[0]),minutes=cint(cum_early_out[1])).total_seconds()
        late_in_list = frappe.db.sql("""select late_in,deduction_hours from `tabLate IN Register`
            where employee = %s and is_approved != 1 and attendance_date between %s and %s  """, (emp.name, first_day, last_day), as_dict=True)
        if late_in_list:
            for l in late_in_list:
                late_in = l.late_in
                late_in = late_in.split(":")
                late_in = timedelta(hours =cint(late_in[0]),minutes=cint(late_in[1])).total_seconds()
                cum_late_in += late_in
                late_in_count += 1
                # print l.deduction_hours
                total_late_in_deduction_hours += l.deduction_hours
        early_out_list = frappe.db.sql("""select early_out,deduction_hours from `tabEarly OUT Register`
            where employee = %s and is_approved != 1 and attendance_date between %s and %s  """, (emp.name, first_day, last_day), as_dict=True)
        if early_out_list:
            for e in early_out_list:
                early_out = e.early_out
                early_out = early_out.split(":")
                early_out = timedelta(hours =cint(early_out[0]),minutes=cint(early_out[1])).total_seconds()
                cum_early_out += early_out
                early_out_count += 1
                total_early_out_deduction_hours += e.deduction_hours
        monthly_occ_count = late_in_count + early_out_count
        bs = frappe.get_single("Biometry Settings")
        if monthly_occ_count >= int(bs.lateness_count_for_a_month):
            disciplinary_measure = "Probation for 60 Days"
        before_3month_first_day = add_days(first_day, -90)
        late_in_list_for_3month = frappe.db.sql("""select late_in from `tabLate IN Register`
            where employee = %s and attendance_date between %s and %s  """, (emp.name, before_3month_first_day, last_day), as_dict=True)        
        if late_in_list_for_3month:
            for l in late_in_list_for_3month:
                late_in_count_for_3month += 1
        early_out_list_for_3month = frappe.db.sql("""select early_out from `tabEarly OUT Register`
            where employee = %s and attendance_date between %s and %s  """, (emp.name, before_3month_first_day, last_day), as_dict=True)
        if early_out_list_for_3month:
            for l in early_out_list_for_3month:
                early_out_count_for_3month += 1
        occ_count_for_3month = late_in_count_for_3month + early_out_count_for_3month
        if occ_count_for_3month >= int(bs.lateness_count_for_90_days):
            disciplinary_measure = "Termination"
        ssa = frappe.db.get_value("Salary Structure Assignment",{"employee":emp.name},"salary_structure")
        if ssa:
            holiday_count = 0
            pay_per_hour = ""
            if emp.holiday_list:
                holiday_list = frappe.get_doc("Holiday List",{"name":emp.holiday_list})
                if holiday_list:
                    for h in holiday_list.holidays:
                        if h.holiday_date >= first_day and h.holiday_date <= last_day:
                            holiday_count += 1
            actual_days_count = date_diff(last_day, first_day) + 1
            pay_days = actual_days_count - holiday_count
            salary_structure = frappe.get_doc("Salary Structure",ssa)
            pay_per_hour = round(salary_structure.net_pay/pay_days/9.5,2)
        if cum_late_in or cum_early_out:
            total_deduction_hours = total_late_in_deduction_hours + total_early_out_deduction_hours
            total_deduction_amount = total_deduction_hours * pay_per_hour
        emp_details = frappe.get_doc("Employee", emp.name)
        emp_details.update({
            "current_month_late_in_count": late_in_count,
            "late_in_hours": round(cum_late_in /3600, 1),
            "current_month_early_out_count": early_out_count,
            "early_out_hours": round(cum_early_out /3600,1),
            "disciplinary_measure": disciplinary_measure,
            "net_pay_per_hour": pay_per_hour,
            "total_deduction_amount": total_deduction_amount,
            "late_in_deduction_hours": total_late_in_deduction_hours,
            "early_out_deduction_hours": total_early_out_deduction_hours
        })   
        emp_details.save(ignore_permissions=True)
        frappe.db.commit()
        




def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)  
