import datetime

from reportlab.graphics.shapes import inverse

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
	_name = "estate.property"
	_description = "Real Estate Property for Testing"
	_sql_constraints = [
		('expected_price', 'CHECK(expected_price >= 0)', 'Expected_price must be strictly positive'),
	]

	name = fields.Char(required=True)
	property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
	description = fields.Text()
	postcode = fields.Char()
	date_availability = fields.Date(
		copy=False, default=lambda x: fields.Date.today() + datetime.timedelta(days=90)
	)
	expected_price = fields.Float(required=True)
	selling_price = fields.Float(readonly=True, copy=False)
	buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
	salesman_id = fields.Many2one(
		"res.users",
		string="Salesperson",
		index=True,
		tracking=True,
		default=lambda self: self.env.user,
	)
	property_type_id = fields.Many2one("estate.property.type", string="Property Type")
	state = fields.Selection(
		[
			("new", "New"),
			("offer_received", "Offer Received"),
			("offer_accepted", "Offer Accepted"),
			("sold", "Sold"),
			("canceled", "Canceled"),
		],
		default="new",
		required=True,
	)
	bedrooms = fields.Integer(default=2)
	living_area = fields.Integer()
	facades = fields.Integer()
	garage = fields.Boolean()
	garden = fields.Boolean()
	garden_area = fields.Integer()
	garden_orientation = fields.Selection(
		[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
	)
	property_offer_ids = fields.One2many(
		"estate.property.offer", "property_id", string="Offers"
	)
	total_area = fields.Integer(compute="_compute_total_area", store=True)
	best_price = fields.Float(
		compute="_compute_best_price", store=True, depends=["property_offer_ids"]
	)
	validity = fields.Integer(default=7)
	date_deadline = fields.Date(
		compute="_compute_date_deadline", inverse="_inverse_date_dateline", store=True
	)
	active = fields.Boolean(default=True)

	@api.depends("living_area", "garden_area")
	def _compute_total_area(self):
		for record in self:
			record.total_area = record.living_area + record.garden_area

	# @api.depends("property_offer_ids.price")
	def _compute_best_price(self):
		for record in self:
			recordset = record.property_offer_ids.mapped("price")
			if len(recordset) == 0:
				record.best_price = 0
			else:
				record.best_price = max(recordset)

	@api.depends("create_date", "validity")
	def _compute_date_deadline(self):
		for record in self:
			record.date_deadline = (
				fields.Date.today() + datetime.timedelta(days=record.validity)
			)

	def _inverse_date_dateline(self):
		for record in self:
			record.validity = (record.date_deadline - fields.Date.today()).days

	@api.onchange("garden")
	def _onchange_garden(self):
		if self.garden:
			self.garden_orientation = 'north'
			self.garden_area = 10
		else:
			self.garden_orientation = False
			self.garden_area = 0

	def estate_sold(self):
		for record in self:  # why for here?
			if record.state == "canceled":
				raise UserError("A canceled property can not be sold!")
			else:
				record.state = "sold"
		return "sold"

	def estate_cancel(self):
		for record in self:  # why for here?
			if record.state == "sold":
				raise UserError("A sold property can not be canceled!")
			else:
				record.state = "canceled"
		return "canceled"
