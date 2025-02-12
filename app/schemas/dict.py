from typing import Annotated

from pydantic import Field, BaseModel


class BaseDict(BaseModel):
    dict_status: Annotated[str | None, Field(alias="dictStatus", title="字典编码")] = None
    dict_name: Annotated[str | None, Field(alias="dictName", title="字典名称")] = None
    dict_type: Annotated[str | None, Field(alias="dictType", title="字典类型")] = None
    dict_value: Annotated[str | None, Field(alias="dictValue", title="字典值")] = None
    dict_sort: Annotated[str | None, Field(alias="dictSort", title="字典排序")] = None


class DictCreate(BaseDict):
    ...


class DictUpdate(BaseDict):
    ...


class DictSearch(BaseDict):
    current: Annotated[int | None, Field(description="页码")] = None
    size: Annotated[int | None, Field(description="每页数量")] = None
