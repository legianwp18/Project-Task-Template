#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TaskTemplateMaster(models.Model):
    _name = "project.task.template.master"
    _description = "Project Template Master"
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']

    name = fields.Char('Name Template')
    task_template_ids = fields.One2many('project.task.template', 'master_id', string='Task Template')

class TaskTemplate(models.Model):
    _name = "project.task.template"
    _description = "Task Template"
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']

    name = fields.Char(string='Title', tracking=True, required=True, index='trigram')
    master_id = fields.Many2one('project.task.template.master', string='Master')
    description = fields.Html(string='Description')
    parent_id = fields.Many2one('project.task.template', string='Parent Task', index=True)
    predecessors_id = fields.Many2one('project.task.template', string='Predecessors', index=True, domain=[('parent_id', '=', parent_id)])
    successors_id = fields.Many2one('project.task.template', string='Successors', index=True, domain=[('parent_id', '=', parent_id)])
    child_ids = fields.One2many('project.task.template', 'parent_id', string="Sub-tasks")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'High'),
    ], default='0', index=True, string="Priority", tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
    tag_ids = fields.Many2many('project.tags', string='Tags',)
    user_ids = fields.Many2many('res.users', 
        relation='project_task_template_user_rel', 
        column1='task_id', 
        column2='user_id', 
        string='Assignees', 
        context={'active_test': False}, 
        tracking=True
    )
    work_days = fields.Integer('Work Days', default=1)

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