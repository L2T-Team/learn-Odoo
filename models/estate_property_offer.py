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

    def estate_offer_accept(self):
        self.status = "accepted"
        for offer in self.property_id.property_offer_ids:
            if offer.id != self.id:
                offer.status = "refused"

        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"
        self.property_id.buyer_id = self.partner_id.id
        return "accepted"

    def estate_offer_refuse(self):
        self.status = "refused"
        return True
