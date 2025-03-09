from ninja import ModelSchema
from backend import models
from ninja import Field, FilterSchema, Schema

# class MaintainerSchema(ModelSchema):
#     class Config:
#         model = models.Maintainer
#         model_fields = ['id', 'name', 'email', 'status', 'created_at', 'updated_at']

# class MaintainerCreateSchema(ModelSchema):
#     class Config:
#         model = models.Maintainer
#         model_fields = ['name', 'email', 'status']

# 其他 Schema 可依照模型定義方式類似建立…
# 例如：MaintainerGroupSchema, HostSchema, TenantSchema, VirtualMachineSchema 等
# ADD Host Schema
# class HostSchema(ModelSchema):
#     class Config:
#         model = models.Host
#         model_fields = ['id', 'name', 'status', 'total_cpu', 'total_memory', 'total_storage', 'available_cpu', 'available_memory', 'available_storage', 'group', 'region', 'dc', 'room', 'rack', 'unit', 'created_at', 'updated_at']

# class HostGroupSchema(ModelSchema):
#     class Config:
#         model = models.HostGroup
#         model_fields = ['id', 'name', 'description', 'status', 'created_at', 'updated_at']

class HostSchema(Schema):
    # id: str
    name: str
    status: str
    total_cpu: int
    total_memory: int
    total_storage: int
    available_cpu: int
    available_memory: int
    available_storage: int
    # group: str
    region: str
    dc: str
    room: str
    rack: str
    unit: str
    

    
class HostGroupSchema(Schema):
    # id: str
    name: str
    description: str
    status: str
