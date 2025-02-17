from tortoise.fields import ManyToManyRelation
from tortoise import fields

from .utils import BaseModel

"""
  @description: Aft 许可
  @param {*}
  @return {*}
"""


class Aft(BaseModel):
    id = fields.IntField(pk=True, unique=True, description='Aft 许可ID')
    apply_number = fields.CharField(max_length=500, unique=True, description='申请编号')
    TIS_code = fields.CharField(max_length=500, null=True, description='TIS编码')
    standard_name = fields.CharField(max_length=500, null=True, description='标准名称')
    update_status = fields.CharField(max_length=500, null=True, description='更新状态')
    apply_license = fields.CharField(max_length=500, null=True, description='申请许可证')
    apply_date = fields.CharField(max_length=500, null=True, description='申请日期')
    apply_status = fields.CharField(max_length=500, null=True, description='申请状态')
    aft_type = fields.CharField(max_length=500, null=True, description='aft类型')
    sort = fields.CharField(max_length=50, null=True, description='排序字段')
    remark = fields.CharField(max_length=500, null=True, description='备注')
    ctime = fields.DatetimeField(description='创建时间', auto_now_add=True)
    mtime = fields.DatetimeField(description='修改时间', auto_now_add=True)
    create_by = fields.CharField(max_length=500, null=True, description='创建人')
    update_by = fields.CharField(max_length=500, null=True, description='修改人')
    by_aft_account: fields.ManyToManyRelation['Account'] = fields.ManyToManyField("app_system.Account",
                                                                                  related_name='by_aft_account')
    by_account_aft: fields.ReverseRelation['Account']

    class Meta:
        table = "sys_aft"
        table_description = "Aft Affa 监控表"
        indexes = [
            ("apply_number",),
            ("sort",),
            ("aft_type",),
        ]
        ordering = ["ctime", "update_status", "sort"]


class Mor(BaseModel):
    id = fields.IntField(pk=True, unique=True, description='Aft 许可ID')
    apply_number = fields.CharField(max_length=500, unique=True, description='申请编号')
    TIS_code = fields.CharField(max_length=500, null=True, description='TIS编码')
    standard_name = fields.CharField(max_length=500, null=True, description='标准名称')
    apply_license = fields.CharField(max_length=500, null=True, description='申请许可证')
    apply_date = fields.CharField(max_length=500, null=True, description='申请日期')
    update_status = fields.CharField(max_length=500, null=True, description='更新状态')
    apply_tax = fields.CharField(max_length=500, null=True, description='申请税号')
    apply_status = fields.CharField(max_length=500, null=True, description='申请状态')
    mor_type = fields.CharField(max_length=500, null=True, description='mor类型')
    sort = fields.CharField(max_length=500, null=True, description='排序')
    remark = fields.CharField(max_length=500, null=True, description='备注')
    operation_name = fields.CharField(max_length=500, null=True, description='操作人')
    ctime = fields.DatetimeField(description='创建时间', auto_now_add=True)
    mtime = fields.DatetimeField(description='修改时间', auto_now_add=True)
    create_by = fields.CharField(max_length=500, null=True, description='创建人')
    update_by = fields.CharField(max_length=500, null=True, description='修改人')

    by_mor_account: fields.ManyToManyRelation['Account'] = fields.ManyToManyField("app_system.Account",
                                                                                  related_name='by_mor_account')
    by_account_mor: fields.ReverseRelation['Account']

    class Meta:
        table = "sys_mor"
        table_description = "Mor5 Mor9 监控表"
        indexes = [
            ("apply_number",),
            ("sort",),
            ("mor_type",),
        ]
        ordering = ["ctime", "update_status", "sort"]


class Nsw(BaseModel):
    id = fields.IntField(pk=True, unique=True, description='Nsw 许可ID')
    apply_number = fields.CharField(max_length=500, unique=True, description='申请编号')
    invoice = fields.CharField(max_length=500, null=True, description='发票号')
    invoice_date = fields.CharField(max_length=500, null=True, description='发票日期')
    product_number = fields.CharField(max_length=500, null=True, description='产品数量')
    update_status = fields.CharField(max_length=500, null=True, description='更新状态')
    rpg_group = fields.CharField(max_length=500, null=True, description='责任小组')
    apply_date = fields.CharField(max_length=500, null=True, description='申请日期')
    apply_status = fields.CharField(max_length=500, null=True, description='申请状态')
    pass_date = fields.CharField(max_length=500, null=True, description='通过日期')
    sort = fields.CharField(max_length=50, null=True, description='排序字段')
    remark = fields.CharField(max_length=500, null=True, description='备注')
    ctime = fields.DatetimeField(description='创建时间', auto_now_add=True, null=True)
    mtime = fields.DatetimeField(description='修改时间', auto_now=True, null=True)
    create_by = fields.CharField(max_length=500, null=True, description='创建人')
    update_by = fields.CharField(max_length=500, null=True, description='修改人')

    by_nsw_account: fields.ManyToManyRelation['Account'] = fields.ManyToManyField("app_system.Account",
                                                                                  related_name='by_nsw_account')
    by_account_nsw: fields.ReverseRelation['Account']

    class Meta:
        table = "sys_nsw"
        table_description = "Nsw 监控表"
        indexes = [
            ("apply_number",),
            ("sort",),
        ]
        ordering = ["ctime", "update_status", "sort"]


class Account(BaseModel):
    id = fields.IntField(pk=True, unique=True, description=' account ID')
    account_number = fields.CharField(max_length=500, unique=True, description='账号')
    password = fields.CharField(max_length=500, null=True, description='密码')
    nickname = fields.CharField(max_length=500, null=True, description='昵称')
    activate = fields.CharField(max_length=500, null=True, description='状态')
    feedback = fields.CharField(max_length=500, null=True, description='反馈')
    remark = fields.CharField(max_length=500, null=True, description='备注')
    ctime = fields.DatetimeField(description='创建时间', auto_now_add=True)
    mtime = fields.DatetimeField(description='修改时间', auto_now_add=True)
    create_by = fields.CharField(max_length=500, null=True, description='创建人')
    update_by = fields.CharField(max_length=500, null=True, description='修改人')

    by_account_aft: fields.ReverseRelation['Aft']
    by_account_nsw: fields.ReverseRelation['Nsw']
    by_account_Mor: fields.ReverseRelation['Mor']

    by_account_dict: ManyToManyRelation['Dict'] = fields.ManyToManyField("app_system.Dict",
                                                                         related_name='by_account_dict')

    class Meta:
        table = "sys_account"
        table_description = "账号中心"
        indexes = [
            ("account_number",),
        ]


class Dict(BaseModel):
    id = fields.IntField(pk=True, unique=True, description='字典ID')
    dict_name = fields.CharField(max_length=500, null=True, description='字典名称')
    dict_type = fields.CharField(max_length=500, null=True, description='字典类型')
    dict_value = fields.CharField(max_length=500, null=True, description='字典值')
    dict_sort = fields.CharField(max_length=500, null=True, description='字典排序')
    dict_status = fields.CharField(max_length=500, null=True, description='字典状态')
    remark = fields.CharField(max_length=500, null=True, description='备注')
    ctime = fields.DatetimeField(description='创建时间', auto_now_add=True)
    mtime = fields.DatetimeField(description='修改时间', auto_now_add=True)
    create_by = fields.CharField(max_length=500, null=True, description='创建人')
    update_by = fields.CharField(max_length=500, null=True, description='修改人')

    class Meta:
        table = "sys_dict"
        table_description = "字典表"
        indexes = [
            ("dict_name",),
            ("dict_type",),
        ]
        ordering = ["ctime", "dict_sort"]


class Job(BaseModel):
    id = fields.IntField(pk=True, unique=True, description='任务ID')
    job_name = fields.CharField(max_length=500, null=True, description='任务名称')
    job_group = fields.CharField(max_length=500, null=True, description='任务组')
    job_status = fields.CharField(max_length=500, null=True, description='任务状态')
    job_executor = fields.CharField(max_length=500, null=True, description='任务执行器')
    invoke_target = fields.CharField(max_length=500, null=True, description='调用目标')
    job_args = fields.CharField(max_length=500, null=True, description='位置参数')
    job_kwargs = fields.CharField(max_length=500, null=True, description='关键字位置参数')
    cron_expression = fields.CharField(max_length=500, null=True, description='cron表达式')
    misfire_policy = fields.CharField(max_length=500, null=True, default=3,
                                      description='计划执行错误策略（1立即执行 2执行一次 3放弃执行')
    concurrent = fields.CharField(max_length=500, null=True, default=1, description='是否并发,(0允许,1禁止)')
    create_time = fields.DatetimeField(description='创建时间', auto_now_add=True)
    update_time = fields.DatetimeField(description='修改时间', auto_now_add=True)
    create_by = fields.CharField(max_length=500, null=True, default=1, description='创建人')
    update_by = fields.CharField(max_length=500, null=True, default=1, description='修改人')
    remark = fields.CharField(max_length=500, null=True, description='备注')

    __all__ = [
        "Aft",
        "Account",
        'Mor',
        'Nsw',
        'Dict'
    ]
