#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProjectTemplate(models.Model):
    _name = "project.template"
    _description = "Project Template"
    _inherit = ['portal.mixin', 'mail.alias.mixin', 'mail.thread', 'mail.activity.mixin', 'rating.parent.mixin']

    @api.model
    def _default_company_id(self):
        if self._context.get('default_project_id'):
            return self.env['project.project'].browse(self._context['default_project_id']).company_id
        return self.env.company

    name = fields.Char("Name", index='trigram', required=True, tracking=True)
    task_template_id = fields.Many2one('project.task.template', string='Task Template')
    start_date = fields.Date('Start Date')
    partner_id = fields.Many2one('res.partner',
        string='Customer', recursive=True, tracking=True,
        compute='_compute_partner_id', store=True, readonly=False,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    company_id = fields.Many2one(
        'res.company', string='Company', compute='_compute_company_id', store=True, readonly=False,
        required=True, copy=True, default=_default_company_id)

    def generator_task(self):
        pass