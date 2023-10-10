from odoo import fields,models,api,_
from datetime import date



class Tailor(models.Model):

    _name = 'tailoring.tailor'
    _description = 'Tailor'
    _inherit = ['mail.thread','mail.activity.mixin']

    order_id = fields.Many2one('sale.order',string='Order Number', readonly=1, tracking=True)
    product = fields.Char()
    name = fields.Char(string="Tailor",readonly=1,tracking=True)
    assigned_date = fields.Datetime(string="Assigned Date",related='order_id.date_order',readonly=1)
    started_date = fields.Datetime(string="Started Date",readonly=1)
    finished_date = fields.Datetime(string="Finished Date",readonly=1)
    state = fields.Selection([('pending','Pending'),('in_progress','In Progress'),
                              ('finished','Finished')],default="pending", tracking=True)


    # ...........................................Tailor Work Start Datetime..........................................
    def start(self):
        self.started_date = fields.Datetime.now()
        self.write({
            'state' : 'in_progress'
        })

    # ...........................................Tailor Work Finished Datetime..........................................
    def finish(self):
        self.finished_date = fields.Datetime.now()
        self.write({
            'state' : 'finished'
        })
        if self.state == 'finished' or self.order_id.state == 'sale':

            self.order_id.state = 'ready to deliver'

    # ...........................................Specific Measrement Record Form View..........................................
    def current_measurement_record(self):
        measurement_id = self.env['tailoring.customer.measurement'].search([('order_id', '=', self.order_id.id)])
        print('**********8',measurement_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Measurement',
            'res_id': measurement_id.id,
            'res_model': 'tailoring.customer.measurement',
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref('pragtech_tailoring_management.tailor_measurment_form').id
        }
