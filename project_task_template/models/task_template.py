#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TaskTemplate(models.Model):
    _name = "project.task.template"
    _description = "Task Template"
    _inherit = [
        'portal.mixin', 
        'mail.thread.cc', 
        'mail.activity.mixin', 
        'rating.mixin'
    ]

    PRIORITY_SELECTION = [
        ('0', 'Low'),
        ('1', 'High'),
    ]

    name = fields.Char(
        string='Title', 
        tracking=True, 
        required=True, 
        index='trigram'
    )
    description = fields.Html(
        string='Description'
    )
    parent_id = fields.Many2one(
        comodel_name ='project.task.template', 
        string='Parent Task', 
        index=True, 
        ondelete='cascade'
    )
    predecessors_id = fields.Many2one(
        comodel_name = 'project.task.template', 
        string='Predecessors', 
        index=True, 
        ondelete='cascade'
    )
    successors_id = fields.Many2one(
        comodel_name = 'project.task.template', 
        string='Successors', 
        index=True, 
        ondelete='cascade'
    )
    child_ids = fields.One2many(
        comodel_name = 'project.task.template', 
        inverse_name='parent_id', 
        string="Sub-tasks"
    )
    priority = fields.Selection(
        selection = PRIORITY_SELECTION, 
        default='0', 
        index=True, 
        string="Priority", 
        tracking=True
    )
    sequence = fields.Integer(
        string='Sequence', 
        default=10
    )
    tag_ids = fields.Many2many(
        comodel_name = 'project.tags', 
        string='Tags'
    )
    user_ids = fields.Many2many(
        comodel_name = 'res.users', 
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
    work_days_line = fields.Integer(
        string = 'Work Days Line',
        compute='get_work_days',
    )
    @api.depends('work_days')
    def get_work_days(self):
        filter_child = [('parent_id','=',self.parent_id.id)]
        work_days_obj = self.env['project.task.template']
        work_days_parent = work_days_obj.browse(self.parent_id.id)
        sum_work_days_child = sum(work_days_obj.search(filter_child).mapped(work_days_obj))
        work_days_parent.write({'work_days': sum_work_days_child})
        self.work_days_line = sum_work_days_child
