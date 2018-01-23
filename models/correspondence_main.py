# -*- coding: utf-8 -*-

# 1 : imports of python lib
import calendar
import socket
import fcntl
import struct
import requests
import simplejson as json
# import json
# from json_encoder import json
import simplejson
from datetime import datetime, date
# 2 :  imports of odoo
from openerp import  api, fields,  models ,_
# 3 :  imports from odoo modules

class CorresPrototype(models.Model):
	#private attributes
	_name = "corres.corres.prototype"
	# Default methods
	# Fields declaration
	client_name    = fields.Many2one('res.partner','Client Name', required=True)
	section_no     = fields.Char('Under No ',required=True)
	section_des    = fields.Char('Section Description')
	acc_officer    = fields.Many2one('corres.acc.officer','Assessing Officer', required=True)
	date_of_notice = fields.Date('Date of Notice',required=True)
	notice_no      = fields.Char('Notice No ',required=True)
	demand_amount  = fields.Float('Demand Amount')
	assigned_to    = fields.Many2one('hr.employee','Assigned To', required=True)
	# assessing_authority = fields.Selection([
	#         ('ito', 'ITO'),
	#         ('assistant_commissioner', 'Assistant Commissioner'),
	#         ('deputy_commissioner', 'Deputy Commissioner'),
	#         ('commissioner', 'Commissioner'),
	#         ('atir', 'ATIR'),
	#         ('high_court', 'High Court'),
	#         ('supreme_court', 'Supreme Court'),
	#         ])
	assessing_authority = fields.Many2one('correspondence.accessing.officer','Tax Authority')
	rto    = fields.Many2one('rto.rto','RTO', required=True)
	corres_his = fields.One2many('correspondence.history','correspondence_his')
	tax_year = fields.Char('Tax Year')
	# compute and search fields, in the same order of fields declaration
	# Constraints and onchanges
	# CRUD methods (and name_get, name_search, ...) overrides
	# Action methods
	# Business methods


# Correspondence Class 
class Correspondence(models.Model):
	#private attributes
	_name                   = 'correspondence.correspondence'
	_description            = 'Correspondence'
	_inherit                = ['mail.thread', 'ir.needaction_mixin','corres.corres.prototype']
	# Default methods
	# Fields declaration
	stages                  = fields.Many2one('correspondence.stage','Stage Name',track_visibility='always')
	stage_name                  = fields.Selection([
								('order', 'Order'),
								('first_appeal', 'First Appeal'),
								('stay', 'Stay'),
								('sec_appeal', 'Second Appeal'),
								('ref_to_hc', 'Reference to High Court'),
								], default="order")
	type_of                 = fields.Many2one('correspondence.type','Type')
	ntn_no                  = fields.Char("NTN")
	strn_no                 = fields.Char("STRN")
	client_contact_name     = fields.Char("Client Contact Name")
	client_contact_number   = fields.Char("Client Contact Number")
	client_contact_email    = fields.Char("Client Email")
	prt_no                  = fields.Char("Provincial Tax number")
	ao_zone                 = fields.Char('Zone')
	ao_unit                 = fields.Char('Unit')
	ao_designation          = fields.Char('Designation')
	ito_name                = fields.Char("Tax Liaison Person")
	ito_contact_no          = fields.Char("ITO Contact No")
	vv                      = fields.Char()
	# Constraints and onchanges
	@api.onchange('notice_no','section_no','tax_year')
	def _onchange_vv(self):
		if self.client_name or self.notice_no or self.section_no or self.tax_year:
			self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
	_rec_name = 'vv'

	@api.onchange('client_name')
	def _onchange_client_name(self):
		if self.client_name:
			self.ntn_no  = self.client_name.regis_no
			self.strn_no = self.client_name.strn

	@api.onchange('acc_officer')
	def _onchange_acc_officer(self):
		if self.acc_officer:
			self.ao_zone  = self.acc_officer.ao_zone
			self.ao_unit = self.acc_officer.ao_unit
			self.ao_designation = self.acc_officer.ao_designation
			self.rto = self.acc_officer.rto
	# CRUD methods (and name_get, name_search, ...) overrides
	# Action methods
	# Business methods


#Correspondence Accessing Officer Class
class CorresAccOfficer(models.Model):
	#private attributes
	_name = 'corres.acc.officer'
	_description = 'CorrespondenceAssessingOfficer'
	# Fields declaration
	name                    = fields.Char("Name")
	ao_zone                 = fields.Char('Zone')
	ao_unit                 = fields.Char('Unit')
	ao_designation          = fields.Char('Designation')
	rto                     = fields.Many2one('rto.rto','RTO')


#Correspondence Type Class
class CorrespondenceType(models.Model):
	#private attributes
	_name = 'correspondence.type'
	_description = 'CorrespondenceType'
	# Fields declaration
	name  = fields.Char("Name")

#Correspondence Stages Class
class CorrespondenceStages(models.Model):
	#private attributes
	_name = 'correspondence.stage'
	_description = 'CorrespondenceStages'
	# Fields declaration
	name  = fields.Char("Name")
	sequence  = fields.Char("Sequence")


# Assessment Class 
class AssessmentCorres(models.Model):
	#private attributes
	_name = 'assessment.corres'
	_description = 'AssessmentCorres'
	_inherit = 'corres.corres.prototype'
	# Fields declaration
	vv = fields.Char(compute="_compute_rec")
	# compute and search fields, in the same order of fields declaration
	@api.multi
	def _compute_rec(self):
		self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
	_rec_name = 'vv'

# Audit Class 
class AuditCorres(models.Model):
	#private attributes
	_name = 'audit.corres'
	_description = 'AuditCorres'
	_inherit = 'corres.corres.prototype'
	# Fields declaration
	vv = fields.Char(compute="_compute_rec")
	# compute and search fields, in the same order of fields declaration
	@api.multi
	def _compute_rec(self):
		self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
	_rec_name = 'vv'

# Rectification Class 
class RectificationCorres(models.Model):
	#private attributes
	_name = 'rectification.corres'
	_description = 'RectificationCorres'
	_inherit = 'corres.corres.prototype'
	# Fields declaration
	vv = fields.Char(compute="_compute_rec")
	# compute and search fields, in the same order of fields declaration
	@api.multi
	def _compute_rec(self):
		self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
	_rec_name = 'vv'

# Recovery Class 
class RecoveryCorres(models.Model):
	#private attributes
	_name = 'recovery.corres'
	_description = 'RecoveryCorres'
	_inherit = 'corres.corres.prototype'
	# Fields declaration
	vv = fields.Char(compute="_compute_rec")
	# compute and search fields, in the same order of fields declaration
	@api.multi
	def _compute_rec(self):
		self.vv = '(%s) Notice No %s u/s %s for Tax Year %s' %(self.client_name.name,self.notice_no,self.section_no ,self.tax_year)
	_rec_name = 'vv'


# RTO Class
class RTO(models.Model):
	#private attributes
	_name = 'rto.rto'
	_description = 'RTO'
	# Fields declaration
	rto   = fields.Char('RTO')
	code  = fields.Char('Code')
	# Record name overrides
	_rec_name = 'rto'


#Correspondence History Class
class CorrespondenceHistory(models.Model):
	#private attributes
	_name = 'correspondence.history'
	_description = 'CorrespondenceHistory'
	# Fields declaration
	hearing_date            = fields.Date('Hearing Date',required=True)
	atendee_name            = fields.Many2one('hr.employee','Attendee Name')
	x_type                  = fields.Many2one('correspondence.history.type',string="Type")
	nex_hear_dat            = fields.Date('Next Hearing Date')          
	demand_due_dat            = fields.Date('Demand Due Date')          
	demand_us_dat            = fields.Date('Demand U/S')          
	remarks                 = fields.Text()
	attachment              = fields.Many2one('correspondence.attachment','Multi Attachment')
	acc_officer             = fields.Many2one('corres.acc.officer','Assessing Officer', required=True)
	cor_file_type           = fields.Many2one('correspondence.file.type','Reply')
	internal_file_no        = fields.Char("Internal File No")
	client_name             = fields.Many2one('res.partner','Client Name')
	section_no              = fields.Char('Section No ')
	notice_no               = fields.Char('Notice No ')
	assigned_to             = fields.Many2one('hr.employee','Assigned To')
	tax_year                = fields.Char('Tax Year')
	type_of                 = fields.Many2one('correspondence.type','Correspondence Type')
	status                  = fields.Char('Status')
	done_date               = fields.Datetime('Done Date')
	hearing_date_str        = fields.Char('Hearing Date')
	hearing_date_now        = fields.Integer(string="Hearing Weeknumber")
	today_date_curr         = fields.Integer(string="Current Weeknumber")
	correspondence_his      = fields.Many2one('correspondence.correspondence',
	ondelete='cascade', string="Name", required=True)
	attachment_file =  fields.Binary(string="Attachment")
	# Constraints and onchanges
	@api.onchange('remarks')
	def _onchange_remarks(self):
		self.client_name = self.correspondence_his.client_name.id
		self.section_no = self.correspondence_his.section_no
		self.notice_no = self.correspondence_his.notice_no
		self.assigned_to = self.correspondence_his.assigned_to.id
		self.tax_year = self.correspondence_his.tax_year
		self.type_of = self.correspondence_his.type_of.id

	@api.onchange('hearing_date')
	def _onchange_hearing_date(self):
		if self.hearing_date:
			hearing_date = datetime.strptime(self.hearing_date,"%Y-%m-%d")
			weeknumber = hearing_date.isocalendar()[1]
			now_date = datetime.now()
			now_weeknumber = now_date.isocalendar()[1]

			result = hearing_date.strftime("%d %b, %Y") 
			self.today_date_curr = int(now_weeknumber)
			self.hearing_date_now = int(weeknumber)
			self.hearing_date_str = result

	# Business methods
	@api.multi
	def import_attachment(self):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(attachment_file))
		return

	@api.multi
	def changeStatus(self):
		self.status = "Done"
		self.done_date = datetime.now()

#Correspondence History Type Class
class CorrespondenceHistoryType(models.Model):
	#private attributes
	_name = 'correspondence.history.type'
	_description = 'CorrespondenceHistoryType'
	# Fields declaration
	name  = fields.Char("Name")


#Correspondence Attachment Class
class CorrespondenceAttachment(models.Model):
	#private attributes
	_name = 'correspondence.attachment'
	_description = 'CorrespondenceAttachment'
	# Fields declaration
	attachment_tree_ids = fields.One2many('correspondence.attachment.tree','attachment_id')

#Correspondence Attachment Tree Class
class CorrespondenceAttachmentTree(models.Model):
	#private attributes
	_name = 'correspondence.attachment.tree'
	_description = 'CorrespondenceAttachmentTree'
	# Fields declaration
	name  = fields.Char("Description")
	attachment =  fields.Binary(string="Attachment")
	attachment_id = fields.Many2one('correspondence.attachment','Attachment')
	# Business methods
	@api.multi
	def import_attachment(self):
		fileobj = TemporaryFile('w+')
		fileobj.write(base64.decodestring(attachment))
		return



# Correspondence File Type Class
class CorrespondenceFileType(models.Model):
	#private attributes
	_name = 'correspondence.file.type'
	_description = 'CorrespondenceFileType'
	# Fields declaration
	date = fields.Date('Date')
	assessing_officer = fields.Many2one('corres.acc.officer','Assessing Officer')
	notice_no = fields.Char("Notice No")
	subject = fields.Char("Subject")
	detail = fields.Char("Detail")
	description      = fields.Text()
	customer_name    = fields.Many2one('res.partner','Client')
	state = fields.Selection([
		('draft','Draft'),
		('validate','Validated'),
		],string="Stage", default="draft")
	vv                      = fields.Char(compute="_compute_rec")
	mylink                  = fields.Char(string="Link", default=lambda self: _('http://'))
	# compute and search fields, in the same order of fields declaration
	@api.multi
	def _compute_rec(self):
		self.vv = 'Notice No %s dated %s for %s' %(self.notice_no,self.date ,self.customer_name)
	_rec_name = 'vv'
	# Action methods
	@api.multi
	def validate(self):
		self.write({'state': 'validate'})

	@api.multi
	def createFile(self):
		if self.mylink == 'http://':
			self.mylink = self.prepareFile('.docx')
		url = self.mylink
		return {
			'type': 'ir.actions.act_url',
			'target': 'new',
			'url': url,
			}

	@api.multi
	def openFile(self):
		url = self.mylink
		return {
			'type': 'ir.actions.act_url',
			'target': 'new',
			'url': url,
			}

	def get_ip_address(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		IP = s.getsockname()[0]
		s.close()
		return IP
# fileType .docx, .pptx, .xlsx
	def prepareFile(self, fileType):
		get_param = self.env['ir.config_parameter'].get_param
		api_key = get_param('api_key', default='')
		server_public_ip = get_param('server_public_ip', default='')
		headers = {'content-type': 'application/json', 'Authorization': api_key}
		ipaddress = self.get_ip_address()
		url = 'http://'+str(ipaddress)+'/api/2.0/files/@my/file?title='+str(self.vv)+str(self.id)+str(fileType)
		resp = requests.post(url, headers=headers)
		data = json.loads(resp.text)
		webUrl =  data['response']['webUrl']
		rawUrl = webUrl.split('http://')
		if "/" in rawUrl[1]:
		    param, value = rawUrl[1].split("/",1)
		requiredUrl = 'http://'+str(server_public_ip)+'/'+value
		return requiredUrl
#Correspondence Accessing OfficerClass
class CorrespondenceAccessingOfficer(models.Model):
	#private attributes
	_name = 'correspondence.accessing.officer'
	_description = 'CorrespondenceAccessingOfficer'
	# Fields declaration
	name  = fields.Char("Name")


