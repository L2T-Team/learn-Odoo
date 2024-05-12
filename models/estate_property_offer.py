from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"

    property_id = fields.Many2one("estate.property", required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    price = fields.Float(required=True)
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
        ("pending", "Pending"),
    ], required=True, default="pending")