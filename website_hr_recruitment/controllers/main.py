# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request
import base64

class WebsiteHrRecruitment(http.Controller):
    def sitemap_jobs(env, rule, qs):
        if not qs or qs.lower() in '/jobs':
            yield {'loc': '/jobs'}

    @http.route([
        '/jobs',
        '/jobs/country/<model("res.country"):country>',
        '/jobs/department/<model("hr.department"):department>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>',
        '/jobs/office/<int:office_id>',
        '/jobs/country/<model("res.country"):country>/office/<int:office_id>',
        '/jobs/department/<model("hr.department"):department>/office/<int:office_id>',
        '/jobs/country/<model("res.country"):country>/department/<model("hr.department"):department>/office/<int:office_id>',
    ], type='http', auth="public", website=True, sitemap=sitemap_jobs)
    def jobs(self, country=None, department=None, office_id=None, **kwargs):
        env = request.env(context=dict(request.env.context, show_address=True, no_tag_br=True))

        Country = env['res.country']
        Jobs = env['hr.job']

        # List jobs available to current UID
        job_ids = Jobs.search([], order="website_published desc,no_of_recruitment desc").ids
        # Browse jobs as superuser, because address is restricted
        jobs = Jobs.sudo().browse(job_ids)

        # Default search by user country
        if not (country or department or office_id or kwargs.get('all_countries')):
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                countries_ = Country.search([('code', '=', country_code)])
                country = countries_[0] if countries_ else None
                if not any(j for j in jobs if j.address_id and j.address_id.country_id == country):
                    country = False

        # Filter job / office for country
        if country and not kwargs.get('all_countries'):
            jobs = [j for j in jobs if j.address_id is None or j.address_id.country_id and j.address_id.country_id.id == country.id]
            offices = set(j.address_id for j in jobs if j.address_id is None or j.address_id.country_id and j.address_id.country_id.id == country.id)
        else:
            offices = set(j.address_id for j in jobs if j.address_id)

        # Deduce departments and countries offices of those jobs
        departments = set(j.department_id for j in jobs if j.department_id)
        countries = set(o.country_id for o in offices if o.country_id)

        if department:
            jobs = [j for j in jobs if j.department_id and j.department_id.id == department.id]
        if office_id and office_id in [x.id for x in offices]:
            jobs = [j for j in jobs if j.address_id and j.address_id.id == office_id]
        else:
            office_id = False

        # Render page
        return request.render("website_hr_recruitment.index", {
            'jobs': jobs,
            'countries': countries,
            'departments': departments,
            'offices': offices,
            'country_id': country,
            'department_id': department,
            'office_id': office_id,
        })

    @http.route('/jobs/add', type='http', auth="user", website=True)
    def jobs_add(self, **kwargs):
        job = request.env['hr.job'].create({
            'name': _('Job Title'),
        })
        return request.redirect("/jobs/detail/%s?enable_editor=1" % slug(job))

    @http.route('/jobs/detail/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_detail(self, job, **kwargs):
        return request.render("website_hr_recruitment.detail", {
            'job': job,
            'main_object': job,
        })

    @http.route('/jobs/apply/<model("hr.job"):job>', type='http', auth="public", website=True)
    def jobs_apply(self, job, **kwargs):
        error = {}
        default = {}
        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')
        return request.render("website_hr_recruitment.apply", {
            'job': job,
            'error': error,
            'default': default,
        })
        
    #this controller is main detail form controller get some value by deafult in the web page
    @http.route(['/application',
                 ], type='http', auth="public", website=True,csrf=False)
    def application_form(self, **post):
        college_list=request.env['college.master'].sudo().search([])
        practice_area_list=request.env['practice.area.master'].sudo().search([])
        graduation_year_list=request.env['year.master'].sudo().search([])
        current_designation_list=request.env['hr.job'].sudo().search([])
        degree_list=request.env['hr.recruitment.degree'].sudo().search([])
        
        return request.render("website_hr_recruitment.application",{'college_list':college_list,'practice_area_list':practice_area_list,'graduation_year_list':graduation_year_list,'current_designation_list':current_designation_list,'degree_list':degree_list,})
    
    #this is the controller method from submit value from web from to model
    @http.route(['/application/success',
                 ], type='http', auth="public", website=True,csrf=False)
    def website_mydetail_controller_save(self,redirect=None, **post):
        if post:
            self._process(post)
            return request.redirect('/application/success')
        return request.render("website_hr_recruitment.success",{})
    
    #this method is to create value in hr.applicant object
    def _process(self, post):
        
        college_get=request.params.get('college')
        practice_area_get=request.params.get('practice')
        graduation_get=request.params.get('graduation')
        designation_get=request.params.get('designation')
        degree_get=request.params.get('degree')
        photo=request.params.get('photo')
        resume=request.params.get('resume')
        
        #this is to create value from web form to hr.applicant model
        applicant_id = request.env['hr.applicant'].create({
                                                   'name':post.get('name')+"'s"+' '+'Application',
                                                   'partner_name':post.get('name'),
                                                   'partner_surname':post.get('surname'),
                                                   'date_of_birth':post.get('date_of_birth'),
                                                   'email_from':post.get('email'),
                                                   'partner_phone':post.get('phone'),
                                                   'alternate_phone_number':post.get('alternate_phone'),
                                                   'professional_experience':post.get('professional_experince'),
                                                   'current_company':post.get('current_company'),
                                                   'current_designation':designation_get,
                                                   'current_ctc':post.get('current_ctc'),
                                                   'practice_area':practice_area_get,
                                                   'college':college_get,
                                                   'type_id':degree_get,
                                                   'graduation_year':graduation_get,
                                                   'llm':post.get('llm'),
                                                   'linkedin_profile':post.get('linkedin'),
                                                   'description':post.get('message'),
                                                   })
        #This is for create attachment from web form
        attach_id = request.env['ir.attachment'].create({
                                            'name': post.get('name')+"'s"+' '+'Resume',
                                            'res_name': applicant_id.partner_name,
                                            'res_model': 'hr.applicant',
                                            'res_id': applicant_id,
                                            'datas': base64.encodestring(post['resume'].read()),
                                            'datas_fname': post['resume'].filename,
                                            'type':'binary',
                                            'file_size':len(post['resume'].filename),
                                            'mimetype':'application/pdf',
                                            })
        #same as above
        photo_id = request.env['ir.attachment'].create({
                                            'name': post.get('name')+"'s"+' '+'Photo',
                                            'res_name': applicant_id.partner_name,
                                            'res_model': 'hr.applicant',
                                            'res_id': applicant_id,
                                            'datas': base64.encodestring(post['photo'].read()),
                                            'datas_fname': post['photo'].filename,
                                            'type':'binary',
                                            'file_size':len(post['photo'].filename),
                                            })
