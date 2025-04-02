To use `rest_framework.authentication.TokenAuthentication` in your Django REST Framework (DRF) project, follow this step-by-step guide. This setup allows your API to use **token-based authentication** where clients authenticate using a static token in the `Authorization` header.

---

## ✅ Step-by-Step: Use `TokenAuthentication` in DRF

---

### 🔹 1. Install `djangorestframework`

If you haven’t already:

```bash
pip install djangorestframework
```

---

### 🔹 2. Enable `rest_framework` and `authtoken` in `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
]
```

Then run the migration to create the token model:

```bash
python manage.py migrate
```

---

### 🔹 3. Configure DRF to use `TokenAuthentication`

In `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

---

### 🔹 4. Create tokens for your users

You can do this in multiple ways:

#### 🅰️ Option A: From Django shell

```bash
python manage.py shell
```

```python
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='admin')  # or create a user
token, created = Token.objects.get_or_create(user=user)
print(token.key)
```

#### 🅱️ Option B: Enable token login via endpoint

Add this to your `urls.py`:

```python
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    ...
    path('api-token-auth/', obtain_auth_token),
]
```

Then POST to `/api-token-auth/` with:

```json
{
  "username": "admin",
  "password": "yourpassword"
}
```

It will return:

```json
{
  "token": "yourauthtokenhere"
}
```

---

### 🔹 5. Use the token in requests

Clients should send the token in the `Authorization` header:

```
Authorization: Token yourauthtokenhere
```

Example with `curl`:

```bash
curl -H "Authorization: Token yourauthtokenhere" http://localhost:8000/api/your-secure-endpoint/
```

---

### ✅ Bonus: Secure only some views

If you want only certain views to require token authentication, you can set it per-view:

```python
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class MyProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Hello, authenticated user!'})
```

---

Let me know if you're combining this with Swagger UI and want to auto-enable the **Authorize** input — I can wire that up too.