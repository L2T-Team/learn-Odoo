from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"

    name = fields.Char(required=True)
    # property_ids = fields.One2many("estate.property", "property_type_id")
    # property_count = fields.Integer(compute="_compute_property_count")

    # def _compute_property_count(self):
    #     for record in self:
    #         record.property_count = len(record.property_ids)