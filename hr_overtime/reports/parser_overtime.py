# -*- coding: utf-8 -*-
from report import report_sxw
from report.report_sxw import rml_parse
from datetime import time
from datetime import datetime, timedelta
from odoo import pooler
import copy

def lengthmonth(year, month):
    if month == 2 and ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0))):
        return 29
    return [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month]

