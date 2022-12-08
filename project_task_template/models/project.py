#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class ProjectTasks(models.Model):
    _inherit = "project.task"

    task_template_id = fields.Many2one(
        comodel_name='project.task.template', 
        string='Task Template'
    )

    predecessors_id = fields.Many2one(
        comodel_name = 'project.task', 
        string='Predecessors', 
        index=True, 
        ondelete='cascade'
    )

    @api.onchange('stage_id')
    def get_stage_id(self):
        if self.predecessors_id.kanban_state != 'done':
            raise ValidationError('Please Done Predecessors Task')
    
class Project(models.Model):
    _inherit = "project.project"

    task_template_id = fields.Many2one(
        comodel_name = 'project.task.template.master', 
        string='Task Template'
    )

    def generator_task_line(self):
        for rec in self:
            if not rec.task_template_id or not rec.date_start:
               raise ValidationError('Please Insert Task Template and Planned Date')

            for task in rec.task_template_id.task_line_ids:
                task_template_obj = self.env['project.task.template']
                filter_task_template = [('parent_id','child_of', task.id)]
                order="master_id,parent_id,sequence ASC"
                task_template = task_template_obj.search(filter_task_template, order=order)

                for template in task_template:
                    task_obj = self.env['project.task']
                    task_parent = False
                    task_predecessors = False
                    if template.parent_id:
                        filter_task = [('task_template_id','=',template.parent_id.id)]
                        task_parent = task_obj.search(filter_task, limit=1)
                    if template.predecessors_id:
                        filter_task_predecessors = [('task_template_id','=',template.predecessors_id.id)]
                        task_predecessors = task_obj.search(filter_task_predecessors, limit=1)
                    record = {
                        'name': template.name,
                        'description':template.description,
                        'project_id':rec.id,
                        'display_project_id':rec.id,
                        'task_template_id':template.id,
                        'predecessors_id':task_predecessors.id if task_predecessors else False,
                        'priority':template.priority,
                        'sequence':template.sequence,
                        'user_ids':[(6, 0, [x.id for x in template.user_ids])],
                        'parent_id': task_parent.id if task_parent else False
                    }
                    task_obj.create(record)
    
    
    @api.model
    def create(self, values):
        result = super(Project, self).create(values)
        result.generator_task_line()
        return result
    