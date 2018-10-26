from odoo import models,fields,api,_

class HrApplicantInherit(models.Model):
    _inherit='hr.applicant'
    
    partner_surname=fields.Char("Applicant's SurName")
    date_of_birth=fields.Date("Appilcant's Date Of Birth")
    alternate_phone_number=fields.Char("Alternate Phone Number")
    professional_experience=fields.Char("Years of Professional Experience")
    current_company=fields.Char("Current Company")
    current_designation=fields.Char("Current Designation")
    current_ctc=fields.Char("Current CTC")
    practice_area=fields.Many2one('practice.area.master',"Practice Area")
    college=fields.Many2one('college.master',"College")
    graduation_year=fields.Many2one('year.master',"Graduation Year")
    llm=fields.Char('LLM')
    linkedin_profile=fields.Text("LinkedIn profile")
#     resume=fields.Binary('Resume')
    
#     photo=fields.Binary('Photo')

#this is Class For Practice Area Master
class PracticeAreaMaster(models.Model):
    _name='practice.area.master'
    
    name=fields.Char('Name')
    
#this is Class For College Master
class CollegeMaster(models.Model):
    _name='college.master'
    
    name=fields.Char('Name')

#this is Class For Year Master 
class YearMaster(models.Model):
    _name='year.master'
    
    name=fields.Char('Year')