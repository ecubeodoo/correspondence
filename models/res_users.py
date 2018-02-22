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
from openerp.exceptions import ValidationError
# 3 :  imports from odoo modules

class CorresResUsers(models.Model):
	#private attributes
	_inherit = "res.users"
	# Default methods
	# Fields declaration
	onlyoffice_user = fields.Char("Only Office User ID")
	office_password = fields.Char("OnlyOffice Password")


	@api.multi
	def addOnlyOfficeUser(self):
		get_param = self.env['ir.config_parameter'].get_param
		api_key = get_param('api_key', default='')
		headers = {'content-type': 'application/json', 'Authorization': api_key}
		ipaddress = self.get_ip_address()
		url = 'http://'+str(ipaddress)+'/api/2.0/people'
		email = self.login
		firstname = 'odooUser'+str(self.id)
		lastname = 'Tagm'
		data =  {"email":email,"firstname":firstname,"lastname":lastname}
		if not self.office_password:
			raise ValidationError('Onlyoffice Password is required create OnlyOffice user.') 
		UserPassword = self.office_password or 'odoo12'
		response = requests.post(url, headers=headers, data=json.dumps(data))
		user_id =  json.loads(response.content)
		# user_id =  response.json()
		print user_id
		if 'response' in user_id:
			self.onlyoffice_user = str(user_id['response']['id'])
			password_url = 'http://localhost/api/2.0/people/'+str(user_id['response']['id'])+'/password.json'
			payload = {"userName":firstname+email,"password":UserPassword}
			req = requests.put(password_url, headers=headers, data=json.dumps(payload))
			print req

	def get_ip_address(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		IP = s.getsockname()[0]
		s.close()
		return IP
# # Correspondence File Type Class
# class CorrespondenceFileType(models.Model):
# 	#private attributes
# 	_name = 'correspondence.file.type'
# 	_description = 'CorrespondenceFileType'
# 	# Fields declaration
# 	date = fields.Date('Date', required=True)
# 	assessing_officer = fields.Many2one('corres.acc.officer','Assessing Officer', required=True)
# 	notice_no = fields.Char("Notice No", required=True)
# 	subject = fields.Char("Subject")
# 	detail = fields.Char("Detail")
# 	description      = fields.Text()
# 	customer_name    = fields.Many2one('res.partner','Client', required=True)
# 	state = fields.Selection([
# 		('draft','Draft'),
# 		('validate','Validated'),
# 		],string="Stage", default="draft")
# 	vv                      = fields.Char(compute="_compute_rec")
# 	mylink                  = fields.Char(string="Link", default=lambda self: _('http://'))
# 	internal_link           = fields.Char(string="Internal Link", default=lambda self: _('http://'))
# 	# compute and search fields, in the same order of fields declaration
# 	@api.one
# 	def _compute_rec(self):
# 		self.vv = 'Notice No %s dated %s for %s' %(self.notice_no,self.date ,self.customer_name.name)
# 	_rec_name = 'vv'
# 	# Action methods
# 	@api.multi
# 	def validate(self):
# 		get_param = self.env['ir.config_parameter'].get_param
# 		api_key = get_param('api_key', default='')
# 		headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': api_key}
# 		ipaddress = self.get_ip_address()
# 		rawFileId = self.mylink.split('=')
# 		fileId = rawFileId[1]
# 		data = 'share[0].ShareTo=42e1e431-3bf4-4e62-a528-97a7df754fc1&share[0].Access=2'
# 		url = 'http://'+str(ipaddress)+'/api/2.0/files/file/'+str(fileId)+'/share'
# 		requests.put(url,data=data,headers=headers)
# 		self.write({'state': 'validate'})
# 	#Set To Draft
# 	@api.multi
# 	def settoDraft(self):
# 		get_param = self.env['ir.config_parameter'].get_param
# 		api_key = get_param('api_key', default='')
# 		headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': api_key}
# 		ipaddress = self.get_ip_address()
# 		rawFileId = self.mylink.split('=')
# 		fileId = rawFileId[1]
# 		data = 'share[0].ShareTo=42e1e431-3bf4-4e62-a528-97a7df754fc1&share[0].Access=1'
# 		url = 'http://'+str(ipaddress)+'/api/2.0/files/file/'+str(fileId)+'/share'
# 		requests.put(url,data=data,headers=headers)
# 		self.write({'state': 'draft'})
# 	@api.multi
# 	def createFile(self):
# 		get_param = self.env['ir.config_parameter'].get_param
# 		server_public_ip = get_param('server_public_ip', default='')
# 		server_internal_ip = get_param('server_internal_ip', default='')

# 		if self.mylink == 'http://':
# 			RequriedLink= self.prepareFile('.docx')
# 			self.mylink = 'http://'+str(server_public_ip)+str(RequriedLink)
# 			self.internal_link = 'http://'+str(server_internal_ip)+str(RequriedLink)
# 			self.settoDraft()


# 		# url = self.mylink

# 		# return {
# 		# 	'type': 'ir.actions.act_url',
# 		# 	'target': 'new',
# 		# 	'url': url,
# 		# 	}

# 	@api.multi
# 	def openFile(self):
# 		url = self.mylink
# 		return {
# 			'type': 'ir.actions.act_url',
# 			'target': 'new',
# 			'url': url,
# 			}

# 	@api.multi
# 	def openFileInternal(self):
# 		url = self.internal_link
# 		return {
# 			'type': 'ir.actions.act_url',
# 			'target': 'new',
# 			'url': url,
# 			}


# 	def get_ip_address(self):
# 		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 		s.connect(("8.8.8.8", 80))
# 		IP = s.getsockname()[0]
# 		s.close()
# 		return IP
# # fileType .docx, .pptx, .xlsx
# 	def prepareFile(self, fileType):
# 		get_param = self.env['ir.config_parameter'].get_param
# 		api_key = get_param('api_key', default='')
# 		headers = {'content-type': 'application/json', 'Authorization': api_key}
# 		ipaddress = self.get_ip_address()
# 		url = 'http://'+str(ipaddress)+'/api/2.0/files/@my/file?title='+str(self.vv)+str(self.id)+str(fileType)
# 		resp = requests.post(url, headers=headers)
# 		data = json.loads(resp.text)
# 		webUrl =  data['response']['webUrl']
# 		rawUrl = webUrl.split('http://')
# 		if "/" in rawUrl[1]:
# 		    param, value = rawUrl[1].split("/",1)
# 		requiredUrl = '/'+value
# 		return requiredUrl
# #Correspondence Accessing OfficerClass
# class CorrespondenceAccessingOfficer(models.Model):
# 	#private attributes
# 	_name = 'correspondence.accessing.officer'
# 	_description = 'CorrespondenceAccessingOfficer'
# 	# Fields declaration
# 	name  = fields.Char("Name")


