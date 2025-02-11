from app.models.system import BaseModel, Menu
from tortoise import fields

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
    by_account: fields.OneToOneRelation['Account'] = fields.OneToOneField("app_system.Account", related_name='aft',
                                                                       on_delete=fields.CASCADE)

    class Meta:
        table = "sys_aft"
        table_description = "Aft Affa 监控表"
        indexes = [
            ("apply_number",),
            ("sort",),
            ("aft_type",),
        ]
        ordering = ["ctime", "update_status", "sort"]


class Account(BaseModel):
    id = fields.IntField(pk=True, unique=True, description='Aft 许可ID')
    account_number = fields.CharField(max_length=500, unique=True, description='账号')
    password = fields.CharField(max_length=500, null=True, description='密码')
    nickname = fields.CharField(max_length=500, null=True, description='昵称')
    activate = fields.CharField(max_length=500, null=True, description='状态')
    active_type = fields.CharField(max_length=500, null=True, description='监控类型')
    ctime = fields.DatetimeField(description='创建时间', auto_now_add=True)
    mtime = fields.DatetimeField(description='修改时间', auto_now_add=True)
    feedback = fields.CharField(max_length=500, null=True, description='反馈')
    remark = fields.CharField(max_length=500, null=True, description='备注')
    create_by = fields.CharField(max_length=500, null=True, description='创建人')
    update_by = fields.CharField(max_length=500, null=True, description='修改人')

    class Meta:
        table = "sys_account"
        table_description = "账号中心"
        indexes = [
            ("account_number",),
        ]


__all__ = [
    "Aft",
    "Account",
]
