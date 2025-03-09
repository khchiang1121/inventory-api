django_ninja_backend/
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── README.md
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── backend/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── dependencies.py         # 共用依賴（例如認證驗證函式）
    ├── models.py               # 所有資料庫模型（依據資料庫設計）
    ├── schemas.py              # Pydantic schema 定義（供 Ninja 使用）
    └── routers/                # 各資源 CRUD 路由
         ├── __init__.py
         ├── maintainers.py
         ├── maintainer_groups.py
         ├── maintainer_group_members.py
         ├── resource_maintainers.py
         ├── hosts.py
         ├── host_groups.py
         ├── tenants.py
         ├── virtual_machines.py
         ├── vm_specifications.py
         ├── k8s_clusters.py
         └── host_group_tenant_quotas.py
