#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TaskTemplate(models.Model):
    _name = "project.task.template"
    _description = "Task Template"
    _inherit = ['portal.mixin', 'mail.thread.cc', 'mail.activity.mixin', 'rating.mixin']

    name = fields.Char(string='Title', tracking=True, required=True, index='trigram')
    description = fields.Html(string='Description')
    parent_id = fields.Many2one('project.task.template', string='Parent Task', index=True, ondelete='cascade')
    predecessors_id = fields.Many2one('project.task.template', string='Predecessors', index=True, ondelete='cascade')
    successors_id = fields.Many2one('project.task.template', string='Successors', index=True, ondelete='cascade')
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
    work_days = fields.Integer(
        string = 'Work Days',
        default=1
    )

    ### Predoseso dan susesor blm
    
