# Data Seeding Guide

This project uses a custom django-seed command that automatically generates valid data while respecting all model validation constraints.

## How It Works

The custom `seed` command (`inventory_api/api/management/commands/seed.py`) extends django-seed with:

1. **Custom field formatters** for models with validation constraints:
   - **BaremetalGroup**: Ensures `available_*` ≤ `total_*` for CPU, memory, and storage
   - **Baremetal**: Ensures `available_*` ≤ `total_*` for CPU, memory, and storage
   - **BaremetalGroupTenantQuota**: Ensures quotas are between 0.1 and 1.0
   - **DataCenter**: Ensures at least one of `fab` or `phase` is set
   - **AnsibleGroup**: Prevents auto-creation of special groups

2. **Coordinated value generation**: Uses a context dictionary to share values between related fields (e.g., generating `total_cpu_cores` first, then using it to limit `available_cpu_cores`)

3. **Full validation enabled**: All model `save()` methods call `full_clean()`, so validation errors are caught immediately

## Usage

### Basic Seeding

```bash
# Seed 10 instances of each model
python manage.py seed api --number=10
```

### Options

- `--number N`: Number of instances to create for each model (default: 10)
- All standard django-seed options are supported

## How to Add Custom Formatters

If you add new models with validation constraints, update the `add_formatters()` method in `inventory_api/api/management/commands/seed.py`:

```python
def add_formatters(self, seeder: Seeder, model_class, number: int):
    _context = {}
    
    if model_class == models.YourModel:
        def gen_total_field(x):
            val = random.randint(100, 1000)
            _context['total'] = val
            return val
        
        def gen_available_field(x):
            total = _context.get('total', 1000)
            return random.randint(0, total)
        
        return {
            'total_field': gen_total_field,
            'available_field': gen_available_field,
        }
    
    # ... other models
    return {}
```

## Alternative: generate_fake_data Command

For more control over the seeding process, use the custom `generate_fake_data` command:

```bash
# Skip existing data (default)
python manage.py generate_fake_data --skip-existing

# Clear all data first, then seed
python manage.py generate_fake_data --clear-first

# Force recreation even if data exists
python manage.py generate_fake_data --force
```

This command creates realistic data with proper relationships and is fully customizable in `inventory_api/api/management/commands/generate_fake_data.py`.

## Benefits of This Approach

✅ **Validation enabled**: All data respects model constraints  
✅ **Easy to maintain**: Just add formatters for new models  
✅ **Automatic dependencies**: django-seed handles foreign key ordering  
✅ **Realistic data**: Generates proper values for each field type  

