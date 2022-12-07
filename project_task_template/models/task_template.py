#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TaskTemplateMaster(models.Model):
    _name = "project.task.template.master"
    _description = "Project Template Master"
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']

    name = fields.Char('Name Template')
    description = fields.Char('Description')
    task_template_ids = fields.One2many('project.task.template', 'master_id', string='Task Template')

class TaskTemplate(models.Model):
    _name = "project.task.template"
    _description = "Task Template"
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']

    name = fields.Char(string='Title', tracking=True, required=True, index='trigram')
    master_id = fields.Many2one('project.task.template.master', string='Master')
    description = fields.Html(string='Description')
    parent_id = fields.Many2one('project.task.template', string='Parent Task', index=True)
    predecessors_id = fields.Many2one('project.task.template', string='Predecessors', index=True)
    successors_id = fields.Many2one('project.task.template', string='Successors', index=True)
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


    ## Belum Work
    @api.onchange('parent_id')
    def get_price(self):
        if self.parent_id:
            self.write({'master_id' : False})

    ## Auto Parent Belum Jalan

    ### Predoseso dan susesor blm
    
