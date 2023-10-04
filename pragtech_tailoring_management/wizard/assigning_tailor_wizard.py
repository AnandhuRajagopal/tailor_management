from odoo import models, fields, api

class assigningTailorWizard(models.TransientModel):
    _name = 'tailoring.assign.tailors'
    _description = 'tailoring_assign_tailors'

    tailor_id = fields.Many2one('res.users', string='Select Tailor')
    order_id = fields.Many2one('sale.order', string="Order Number",default=lambda self: self.get_active_id())



    @api.model
    def get_active_id(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            return self.env['sale.order'].browse(active_id)


    def assign(self):
        active_id = self.env.context.get("active_id")
        sale_order = self.env['sale.order'].browse(self._context.get('active_id'))
        re = self.env['tailoring.tailor'].browse([active_id])
        if re or (sale_order and sale_order.state != 'tailor assigned'):
            self.env['tailoring.tailor'].create({
                'name':self.tailor_id.name,
                'order_id':self.order_id.id,
                'product' : sale_order,
            })

            sale_order.write({
                'state' : 'tailor assigned'
            })

