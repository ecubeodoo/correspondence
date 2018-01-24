import requests
import json
from openerp import models, fields, api

class OnlyOfficeConfigAPI(models.TransientModel):
	_inherit = 'base.config.settings'
	_name = 'onlyoffice.config.api'

	user = fields.Char()
	password = fields.Char()
	url = fields.Char()
	api_key = fields.Char()
	server_public_ip = fields.Char()
	server_internal_ip = fields.Char()

	@api.multi
	def set_api_user(self):
		user = self[0].user or ''
		self.env['ir.config_parameter'].set_param('user', user)

	@api.multi
	def set_api_password(self):
		password = self[0].password or ''
		self.env['ir.config_parameter'].set_param('password', password)

	@api.multi
	def set_api_url(self):
		url = self[0].url or ''
		self.env['ir.config_parameter'].set_param('url', url)

	@api.multi
	def set_api_key(self):
		api_key = self[0].api_key or ''
		self.env['ir.config_parameter'].set_param('api_key', api_key)

	@api.multi
	def set_server_public_ip(self):
		server_public_ip = self[0].server_public_ip or ''
		self.env['ir.config_parameter'].set_param('server_public_ip', server_public_ip)

	@api.multi
	def set_server_internal_ip(self):
		server_internal_ip = self[0].server_internal_ip or ''
		self.env['ir.config_parameter'].set_param('server_internal_ip', server_internal_ip)


	@api.multi
	def getApiToken(self):
		headers = {'content-type': 'application/json'}
		url = self.url
		params = {'username': self.user, 'password': self.password}
		response = requests.post(url, params=params, headers=headers)
		data =  response.json()
		self.api_key =  data['response']['token']

			
	@api.multi
	def get_default_credentials(self, fields=None):
		get_param = self.env['ir.config_parameter'].get_param
		user = get_param('user', default='')
		password = get_param('password', default='')
		url = get_param('url', default='')
		api_key = get_param('api_key', default='')
		server_public_ip = get_param('server_public_ip', default='')
		server_internal_ip = get_param('server_internal_ip', default='')
		return {
			'user': user,
			'password': password,
			'url' : url,
			'api_key' : api_key,
			'server_public_ip':server_public_ip,
			'server_internal_ip':server_internal_ip
		}