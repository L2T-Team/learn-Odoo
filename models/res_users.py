from odoo import fields, models, api


class ResUsers(models.Model):
	_inherit = "res.users"

	property_ids = fields.One2many("estate.property", "salesman_id")
	hehe = fields.Char("Hehe", default="hehe")
