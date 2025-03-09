import uuid
from datetime import datetime
import random

from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, declarative_base
from faker import Faker

# 修改此處連線資訊，請根據你的環境設定連線字串
# read from .env file
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ------------------------------
# 現有的資料表模型
# ------------------------------

# 實體機群組表
class HostGroup(Base):
    __tablename__ = 'host_group'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(Text, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 租戶表
class Tenant(Base):
    __tablename__ = 'tenant'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(Text, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 實體機器表
class Host(Base):
    __tablename__ = 'host'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    status = Column(String)  # 例如：running, maintenance, offline
    total_cpu = Column(Integer)
    total_memory = Column(Integer)  # MB
    total_storage = Column(Integer)  # GB
    available_cpu = Column(Integer)
    available_memory = Column(Integer)  # MB
    available_storage = Column(Integer) # GB
    group_id = Column(UUID(as_uuid=True), ForeignKey("host_group.id"))
    region = Column(String)
    dc = Column(String)
    room = Column(String)
    rack = Column(String)
    unit = Column(String)
    old_system_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 群組租戶授權表
class HostGroupTenantQuota(Base):
    __tablename__ = 'host_group_tenant_quota'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("host_group.id"))
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"))
    cpu_quota_percentage = Column(Float)  # 百分比，例如 40.0
    memory_quota = Column(Integer)  # MB
    storage_quota = Column(Integer) # GB
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 虛擬機規格表
class VMSpecification(Base):
    __tablename__ = 'vm_specification'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    required_cpu = Column(Integer)
    required_memory = Column(Integer)   # MB
    required_storage = Column(Integer)  # GB
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 虛擬機器表
class VirtualMachine(Base):
    __tablename__ = 'virtual_machine'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"))
    host_id = Column(UUID(as_uuid=True), ForeignKey("host.id"))
    specification_id = Column(UUID(as_uuid=True), ForeignKey("vm_specification.id"))
    k8s_cluster_id = Column(UUID(as_uuid=True), ForeignKey("k8s_cluster.id"), nullable=True)
    status = Column(String)  # 例如：建立中、運行中、錯誤
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# ------------------------------
# 新增的資料表模型 (根據 database.md)
# ------------------------------

# 個人維護者
class Maintainer(Base):
    __tablename__ = 'maintainer'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 維護者群組
class MaintainerGroup(Base):
    __tablename__ = 'maintainer_group'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    group_manager_id = Column(UUID(as_uuid=True), ForeignKey("maintainer.id"))
    description = Column(Text, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 維護者群組成員
class MaintainerGroupMember(Base):
    __tablename__ = 'maintainer_group_member'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), ForeignKey("maintainer_group.id"))
    maintainer_id = Column(UUID(as_uuid=True), ForeignKey("maintainer.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 資源維護者關聯
class ResourceMaintainer(Base):
    __tablename__ = 'resource_maintainer'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_type = Column(String)
    resource_id = Column(UUID(as_uuid=True))
    maintainer_type = Column(String)  # "individual" 或 "group"
    maintainer_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# k8s叢集表
class K8sCluster(Base):
    __tablename__ = 'k8s_cluster'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenant.id"))
    description = Column(Text, nullable=True)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# 注意：資料庫已建立，因此不需要 create_all
Base.metadata.create_all(engine)

def create_fake_data():
    fake = Faker()
    session = SessionLocal()

    try:
        # 1. 新增 HostGroup (假設建立 3 個群組)
        host_groups = []
        for i in range(3):
            hg = HostGroup(
                name=f"HostGroup-{i+1}",
                description=fake.text(max_nb_chars=50),
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(hg)
            host_groups.append(hg)
        session.commit()  # 提交後才能取得自動產生的 ID

        # 2. 新增 Tenant (假設建立 5 個租戶)
        tenants = []
        for i in range(5):
            tenant = Tenant(
                name=f"Tenant-{i+1}",
                description=fake.text(max_nb_chars=50),
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(tenant)
            tenants.append(tenant)
        session.commit()

        # 3. 為部分 HostGroup 與 Tenant 建立授權配額 (50% 機率產生)
        for hg in host_groups:
            for tenant in tenants:
                if random.choice([True, False]):
                    quota = HostGroupTenantQuota(
                        group_id=hg.id,
                        tenant_id=tenant.id,
                        cpu_quota_percentage=round(random.uniform(20, 80), 2),
                        memory_quota=random.randint(4096, 32768),
                        storage_quota=random.randint(100, 1000),
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    session.add(quota)
        session.commit()

        # 4. 新增 Host (假設建立 10 台實體機)
        hosts = []
        statuses = ["running", "maintenance", "offline"]
        for i in range(10):
            total_cpu = random.choice([8, 16, 32, 64])
            total_memory = random.choice([16384, 32768, 65536])  # MB
            total_storage = random.choice([500, 1000, 2000])       # GB
            available_cpu = random.randint(1, total_cpu)
            available_memory = random.randint(1024, total_memory)
            available_storage = random.randint(100, total_storage)
            host = Host(
                name=f"Host-{i+1}",
                status=random.choice(statuses),
                total_cpu=total_cpu,
                total_memory=total_memory,
                total_storage=total_storage,
                available_cpu=available_cpu,
                available_memory=available_memory,
                available_storage=available_storage,
                group_id=random.choice(host_groups).id,
                region=fake.city(),
                dc=fake.company(),
                room=fake.street_name(),
                rack=fake.building_number(),
                unit=fake.secondary_address(),
                old_system_id=str(uuid.uuid4()),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(host)
            hosts.append(host)
        session.commit()

        # 5. 新增 VMSpecification (假設建立 5 種規格)
        vm_specs = []
        specs_options = [
            {"name": "small", "required_cpu": 1, "required_memory": 1024, "required_storage": 20},
            {"name": "medium", "required_cpu": 2, "required_memory": 2048, "required_storage": 50},
            {"name": "large", "required_cpu": 4, "required_memory": 4096, "required_storage": 100},
            {"name": "xlarge", "required_cpu": 8, "required_memory": 8192, "required_storage": 200},
            {"name": "2xlarge", "required_cpu": 16, "required_memory": 16384, "required_storage": 400},
        ]
        for spec in specs_options:
            vm_spec = VMSpecification(
                name=spec["name"],
                required_cpu=spec["required_cpu"],
                required_memory=spec["required_memory"],
                required_storage=spec["required_storage"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(vm_spec)
            vm_specs.append(vm_spec)
        session.commit()

        # 6. 新增 VirtualMachine (假設建立 100 台虛擬機)
        vm_statuses = ["建立中", "運行中", "錯誤"]
        vm_list = []
        for i in range(100):
            vm = VirtualMachine(
                name=f"VM-{i+1}",
                tenant_id=random.choice(tenants).id,
                host_id=random.choice(hosts).id,
                specification_id=random.choice(vm_specs).id,
                status=random.choice(vm_statuses),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(vm)
            vm_list.append(vm)
        session.commit()

        # 7. 新增 K8sCluster (為每個租戶建立一個 k8s 叢集)
        k8s_clusters = []
        for tenant in tenants:
            cluster = K8sCluster(
                name=f"K8sCluster-{tenant.name}",
                tenant_id=tenant.id,
                description=fake.text(max_nb_chars=50),
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(cluster)
            k8s_clusters.append(cluster)
        session.commit()

        # 8. 新增 Maintainer (假設建立 10 位維護者)
        maintainers = []
        for i in range(10):
            maintainer = Maintainer(
                name=f"Maintainer-{i+1}",
                email=fake.email(),
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(maintainer)
            maintainers.append(maintainer)
        session.commit()

        # 9. 新增 MaintainerGroup (假設建立 3 個群組)
        maintainer_groups = []
        for i in range(3):
            mg = MaintainerGroup(
                name=f"MaintainerGroup-{i+1}",
                group_manager_id=random.choice(maintainers).id,
                description=fake.text(max_nb_chars=50),
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(mg)
            maintainer_groups.append(mg)
        session.commit()

        # 10. 新增 MaintainerGroupMember (假設每個群組加入 3 至 5 位維護者)
        for mg in maintainer_groups:
            group_members = random.sample(maintainers, random.randint(3, 5))
            for m in group_members:
                mg_member = MaintainerGroupMember(
                    group_id=mg.id,
                    maintainer_id=m.id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(mg_member)
        session.commit()

        # 11. 新增 ResourceMaintainer (為部分資源隨機指派維護者)
        # 為 HostGroup 指派
        for hg in host_groups:
            if random.choice([True, False]):
                if random.choice([True, False]):
                    maintainer_type = "individual"
                    maintainer_id = random.choice(maintainers).id
                else:
                    maintainer_type = "group"
                    maintainer_id = random.choice(maintainer_groups).id
                rm = ResourceMaintainer(
                    resource_type="HostGroup",
                    resource_id=hg.id,
                    maintainer_type=maintainer_type,
                    maintainer_id=maintainer_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(rm)

        # 為 Tenant 指派
        for t in tenants:
            if random.choice([True, False]):
                if random.choice([True, False]):
                    maintainer_type = "individual"
                    maintainer_id = random.choice(maintainers).id
                else:
                    maintainer_type = "group"
                    maintainer_id = random.choice(maintainer_groups).id
                rm = ResourceMaintainer(
                    resource_type="Tenant",
                    resource_id=t.id,
                    maintainer_type=maintainer_type,
                    maintainer_id=maintainer_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(rm)

        # 為 Host 指派
        for host in hosts:
            if random.choice([True, False]):
                if random.choice([True, False]):
                    maintainer_type = "individual"
                    maintainer_id = random.choice(maintainers).id
                else:
                    maintainer_type = "group"
                    maintainer_id = random.choice(maintainer_groups).id
                rm = ResourceMaintainer(
                    resource_type="Host",
                    resource_id=host.id,
                    maintainer_type=maintainer_type,
                    maintainer_id=maintainer_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(rm)

        # 為 VirtualMachine 指派
        for vm in vm_list:
            if random.choice([True, False]):
                if random.choice([True, False]):
                    maintainer_type = "individual"
                    maintainer_id = random.choice(maintainers).id
                else:
                    maintainer_type = "group"
                    maintainer_id = random.choice(maintainer_groups).id
                rm = ResourceMaintainer(
                    resource_type="VirtualMachine",
                    resource_id=vm.id,
                    maintainer_type=maintainer_type,
                    maintainer_id=maintainer_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(rm)

        # 為 K8sCluster 指派
        for cluster in k8s_clusters:
            if random.choice([True, False]):
                if random.choice([True, False]):
                    maintainer_type = "individual"
                    maintainer_id = random.choice(maintainers).id
                else:
                    maintainer_type = "group"
                    maintainer_id = random.choice(maintainer_groups).id
                rm = ResourceMaintainer(
                    resource_type="K8sCluster",
                    resource_id=cluster.id,
                    maintainer_type=maintainer_type,
                    maintainer_id=maintainer_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(rm)

        session.commit()

        print("Fake data inserted successfully.")
    except Exception as e:
        session.rollback()
        print("Error occurred:", e)
    finally:
        session.close()

if __name__ == '__main__':
    create_fake_data()
