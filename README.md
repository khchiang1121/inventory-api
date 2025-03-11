# django_ninja_backend/README.md

# Django Ninja Backend

This project is a Django application that utilizes Django Ninja for building APIs. It is structured to support a variety of resources and includes Docker support for easy deployment.

## Project Structure

The project is organized as follows:

```
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
    ├── dependencies.py
    ├── models.py
    ├── schemas.py
    └── routers/
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
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd django_ninja_backend
   ```

2. **Build the Docker image:**
   ```
   docker build -t django_ninja_backend .
   ```

3. **Run the application using Docker Compose:**
   ```
   docker-compose up
   ```

4. **Access the application:**
   Open your web browser and go to `http://localhost:8000`.

## Usage

- Use `manage.py` to run server commands, apply migrations, and create new applications.
- The API endpoints are defined in the `backend/routers` directory, where you can find CRUD operations for various resources.

## Requirements

Make sure to install the required Python packages listed in `requirements.txt` if you are running the application outside of Docker.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
















django-admin startproject virtflow
mamba install --yes --file requirements.txt
python manage.py showmigrations
python manage.py migrate --plan
python manage.py sqlmigrate app1 0002_add_new_field
 python manage.py createsuperuser


python manage.py makemigrations backend
python manage.py migrate
python manage.py runserver

5️⃣ 測試模型是否能正常使用
如果你成功遷移，但仍然出錯，可以試試 Django shell：

bash
複製
編輯
python manage.py shell
然後：

python
複製
編輯
from backend.models import Host
Host.objects.create(name="test_host")
print(Host.objects.all())
如果這時候仍然報錯 relation "backend_host" does not exist，那麼可能是資料庫的問題，請重新檢查 migration。

uvicorn virtflow.asgi:application --host 0.0.0.0 --port 8000



pip uninstall ninja
mamba install --yes --file requirements.txt

conda create --name virtflow python=3.13 "mamba>=0.22.1"
source ~/anaconda3/etc/profile.d/conda.sh
conda activate virtflow