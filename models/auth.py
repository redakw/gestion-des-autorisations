# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError, ValidationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class User_emp(models.Model):
    _inherit = 'res.users'
    employee_id =fields.Many2one('hr.employee', 'Employee')
    leave_approvals_emp_ids = fields.One2many('leave.validation.status',
                                      'holiday_status_emp_id',
                                      string='Leave Validators')
class autorisation(models.Model):
    _name = 'autorisation.autorisation'
    _description = 'autorisation.autorisation'

    user_id = fields.Many2one('res.users', default=lambda self: self.env.user,readonly=True)
    name = fields.Many2one('hr.employee', 'Employee')
    motif_autorisation = fields.Text()
    date_sortie = fields.Datetime(required=False)
    date_retour = fields.Datetime(required=False)
    days_number = fields.Float()
    days_rest = fields.Float()
    days_recovery = fields.Float()
    leave_approvals_autorisation = fields.One2many('leave.validation.status',
                                      'holiday_status_autorisation', related='name.leave_approvals_emp',
                                      string='Leave Validators')

    leave_approvals_autorisation_ids = fields.One2many('leave.validation.status',
                                      'holiday_status_autorisation', related='user_id.leave_approvals_emp_ids',
                                      string='Leave Validators')

    state = fields.Selection([
        ('a_approver', 'A Approuver'),
        ('confirm', 'Cofirmé par Responsable'),
        ('refuser', 'Refuser')], string='Status', default='a_approver')
    type_autorisation = fields.Selection([
        ('autorisation_sortie', 'Autorisation de sortie'), 
        ('autorisation_absence', 'Autorisation d absence'),        
        ('att_travail', 'Attestation de travail'),
        ('att_salaire', 'Attestation de salaire'),
        ('att_domiciliation', 'Attestation de domiciliation'),
        ('bord_cnss', 'Bordereau de cnss'),
        ('autorisation_demplacement', 'Autorisation d emplacement')], string='Type d Autorisation', default='autorisation_sortie')

    # calcule de nombre de jours prie
    #@api.onchange('date_retour')
    #def jours_reste(self):
     #   if self.date_retour != False:
      #      self.days_number = (self.date_retour - self.date_sortie).days



    @api.onchange('type_autorisation')
    def _onchange_name(self):
      for line in self.leave_approvals_autorisation_ids:
        line.validation_status = False

    def action_confirm(self):
        for line in self.leave_approvals_autorisation_ids:
            if line.validating_users.id == self.env.uid:                                        
                line.validation_status = True

        if all(line.validation_status for line in self.leave_approvals_autorisation_ids):
            self.state = 'confirm'
            msg = MIMEMultipart()
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
            server.login('noreply@alphagroup.ma', 'Alpha2023!')
            msg['Subject'] = 'Demande'
            message = "Vous avez une demande"
            msg.attach(MIMEText(message))
            server.sendmail('noreply@alphagroup.ma',self.user_id.login, msg.as_string())
            server.quit()


    def action_refuser(self):
        self.state = 'refuser'

    @api.model
    def create(self, vals):
        rec = super(autorisation, self).create(vals)
        rec.send()
        return rec

    def send(self):
        msg = MIMEMultipart()
        server = smtplib.SMTP('smtp.office365.com',587)
        server.starttls()
        server.login('noreply@alphagroup.ma', 'Alpha2023!')
        msg['Subject'] = 'Demande'
        message = "Vous avez une demande"
        msg.attach(MIMEText(message))
        for line in self.leave_approvals_autorisation_ids:
            server.sendmail('noreply@alphagroup.ma', line.validating_users.login, msg.as_string())
        server.quit()
        
# essaie avec un champ de selection (yes,no)
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    leave_approvals_emp = fields.One2many('leave.validation.status',
                                      'holiday_status_emp',
                                      string='Leave Validators')
                                      

class LeaveValidationStatus(models.Model):
    """ Model for leave validators and their status for each leave request """
    _name = 'leave.validation.status'
    _rec_name ='validating_users'
    holiday_status_autorisation = fields.Many2one('autorisation.autorisation')
    holiday_status_autorisation_id = fields.Many2one('autorisation.autorisation')
    holiday_status_emp = fields.Many2one('hr.employee')
    holiday_status_emp_id = fields.Many2one('res.users')
    name = fields.Char()
    validating_users = fields.Many2one('res.users', string='Leave Validators', help="Leave validators")
    validation_status = fields.Boolean(string='Approve Status')
    
