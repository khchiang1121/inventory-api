
django-admin startproject virtflow
mamba install --yes --file requirements.txt
python manage.py showmigrations
python manage.py migrate --plan
python manage.py sqlmigrate app1 0002_add_new_field
 python manage.py createsuperuser

python manage.py makemigrations backend
python manage.py migrate
python manage.py runserver
python manage.py collectstatic

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
from backend.models import Baremetal
Baremetal.objects.create(name="test_host")
print(Baremetal.objects.all())
如果這時候仍然報錯 relation "backend_host" does not exist，那麼可能是資料庫的問題，請重新檢查 migration。

uvicorn virtflow.asgi:application --host 0.0.0.0 --port 8201

pip uninstall ninja
mamba install --yes --file requirements.txt

conda create --name virtflow python=3.13 "mamba>=0.22.1"
source ~/anaconda3/etc/profile.d/conda.sh
conda activate virtflow

export DJANGO_SETTINGS_MODULE=virtflow.settings

# 正確從0啟動流程

create .env
create pgadmin4/.pgpass
source .env
docker compose up -d
make migrations
make migrate
python manage.py createsuperuser
make fake
make stage

登入
<http://localhost:8201/admin/>
API
<http://localhost:8201/api/v1/>
文件
<http://localhost:8201/api/v1/docs>

how to set static
python manage.py collectstatic
