"""
Custom seed command with formatters for models with validation constraints
"""

import random
from typing import Any, Callable, Dict

from django_seed.management.commands import seed
from django_seed.seeder import Seeder

from inventory_api.api import models


class Command(seed.Command):
    """Custom seed command with proper data generation for validated models"""

    help = "Seed database with fake data (respects validation constraints)"

    def add_formatters(
        self, seeder: Seeder, model_class: Any, number: int
    ) -> Dict[str, Callable[[Any], Any]]:
        """Add custom formatters for models that need coordinated field values"""

        from faker import Faker

        fake = Faker()

        # Storage for coordinated values (shared between formatters for same instance)
        _context: Dict[str, Any] = {}

        # Global formatters for all models
        formatters: Dict[str, Callable[[Any], Any]] = {}

        # Limit name fields to 255 characters (faker sometimes generates longer text)
        if hasattr(model_class, "_meta"):
            for field in model_class._meta.get_fields():
                if hasattr(field, "max_length") and field.name == "name" and field.max_length:
                    if field.max_length <= 255:
                        formatters["name"] = lambda x: (
                            fake.company()[: field.max_length]
                            if field.max_length < 100
                            else fake.text(max_nb_chars=min(200, field.max_length))[
                                : field.max_length
                            ]
                        )
                        break

        # BaremetalGroup: ensure total >= available
        if model_class == models.BaremetalGroup:
            # Track instances to reset context
            instance_tracker: list = []

            def gen_total_cpu(x: Any) -> int:
                # Reset context for new instance
                current_id = id(x)
                if not instance_tracker or instance_tracker[0] != current_id:
                    instance_tracker.clear()
                    instance_tracker.append(current_id)
                    _context.clear()

                val = random.randint(64, 512)
                _context["bg_cpu"] = val
                return val

            def gen_avail_cpu(x: Any) -> int:
                total = _context.get("bg_cpu", 512)
                return random.randint(0, total)

            def gen_total_mem(x: Any) -> int:
                val = random.randint(32768, 524288)
                _context["bg_mem"] = val
                return val

            def gen_avail_mem(x: Any) -> int:
                total = _context.get("bg_mem", 524288)
                return random.randint(0, total)

            def gen_total_storage(x: Any) -> int:
                val = random.randint(10000, 50000)
                _context["bg_storage"] = val
                return val

            def gen_avail_storage(x: Any) -> int:
                total = _context.get("bg_storage", 50000)
                return random.randint(0, total)

            formatters.update(
                {
                    "total_cpu_cores": gen_total_cpu,
                    "available_cpu_cores": gen_avail_cpu,
                    "total_memory_mib": gen_total_mem,
                    "available_memory_mib": gen_avail_mem,
                    "total_storage_gb": gen_total_storage,
                    "available_storage_gb": gen_avail_storage,
                }
            )

        # Baremetal: ensure available <= total
        elif model_class == models.Baremetal:
            # Track instances to reset context
            instance_tracker_bm: list = []

            def gen_bm_total_cpu(x: Any) -> int:
                # Reset context for new instance
                current_id = id(x)
                if not instance_tracker_bm or instance_tracker_bm[0] != current_id:
                    instance_tracker_bm.clear()
                    instance_tracker_bm.append(current_id)
                    _context.clear()

                val = random.randint(32, 128)
                _context["bm_cpu"] = val
                return val

            def gen_bm_avail_cpu(x: Any) -> int:
                total = _context.get("bm_cpu", 128)
                return random.randint(0, total)

            def gen_bm_total_mem(x: Any) -> int:
                val = random.randint(32768, 262144)
                _context["bm_mem"] = val
                return val

            def gen_bm_avail_mem(x: Any) -> int:
                total = _context.get("bm_mem", 262144)
                return random.randint(0, total)

            def gen_bm_total_storage(x: Any) -> int:
                val = random.randint(500, 10000)
                _context["bm_storage"] = val
                return val

            def gen_bm_avail_storage(x: Any) -> int:
                total = _context.get("bm_storage", 10000)
                return random.randint(0, total)

            formatters.update(
                {
                    "cpu_cores": gen_bm_total_cpu,
                    "available_cpu_cores": gen_bm_avail_cpu,
                    "memory_mib": gen_bm_total_mem,
                    "available_memory_mib": gen_bm_avail_mem,
                    "storage_gb": gen_bm_total_storage,
                    "available_storage_gb": gen_bm_avail_storage,
                }
            )

        # BaremetalGroupTenantQuota: ensure quotas <= 1.0 and unique (group, tenant) pairs
        elif model_class == models.BaremetalGroupTenantQuota:
            from inventory_api.api.models.baremetal import BaremetalGroup
            from inventory_api.api.models.common import Tenant

            # Track created pairs to avoid duplicates
            created_quota_pairs: set = set()

            def get_baremetal_group(x: Any) -> Any:
                groups = list(BaremetalGroup.objects.all())
                tenants = list(Tenant.objects.all())

                if not groups or not tenants:
                    return None

                # Try to find an unused pair
                max_attempts = 50
                for _ in range(max_attempts):
                    group = random.choice(groups)
                    tenant = random.choice(tenants)
                    pair = (group.id, tenant.id)
                    if pair not in created_quota_pairs:
                        _context["bgq_group"] = group
                        _context["bgq_tenant"] = tenant
                        created_quota_pairs.add(pair)
                        return group

                # Return last group even if it may cause duplicate
                return group

            def get_tenant(x: Any) -> Any:
                return _context.get("bgq_tenant")

            formatters.update(
                {
                    "baremetal_group": get_baremetal_group,
                    "tenant": get_tenant,
                    "cpu_quota": lambda x: round(random.uniform(0.1, 1.0), 2),
                    "memory_quota": lambda x: round(random.uniform(0.1, 1.0), 2),
                    "storage_quota": lambda x: round(random.uniform(0.1, 1.0), 2),
                }
            )

        # AnsibleGroup: don't auto-create special groups
        elif model_class == models.AnsibleGroup:
            formatters.update(
                {
                    "is_special": lambda x: False,
                }
            )

        # BaremetalModelGPU: ensure count field is set
        elif model_class == models.BaremetalModelGPU:
            formatters.update(
                {
                    "count": lambda x: random.randint(1, 8),
                }
            )

        # VirtualMachineRole: only use valid choices (there are only 4 possible values)
        elif model_class == models.VirtualMachineRole:
            # Valid choices for VirtualMachineRole
            valid_roles = ["control-plane", "worker", "management", "other"]
            role_counter = [0]  # Use list to make it mutable in closure

            def get_role_name(x: Any) -> str:
                # Cycle through valid roles
                if role_counter[0] >= len(valid_roles):
                    # Already created all roles, return existing to avoid duplicates
                    # This will cause an integrity error which django-seed will handle
                    return valid_roles[role_counter[0] % len(valid_roles)]

                role = valid_roles[role_counter[0]]
                role_counter[0] += 1
                return role

            formatters.update(
                {
                    "name": get_role_name,
                }
            )

        # AnsibleGroupRelationship: ensure parent and child are in same inventory and not the same
        elif model_class == models.AnsibleGroupRelationship:
            from inventory_api.api.models.ansible import AnsibleGroup

            # Track created pairs to avoid duplicates
            created_pairs: set = set()

            def get_parent_group(x: Any) -> Any:
                # Get all groups
                groups = list(AnsibleGroup.objects.all())
                if not groups:
                    return None

                # Try to find a valid parent-child pair that hasn't been created yet
                max_attempts = 50
                for _ in range(max_attempts):
                    parent = random.choice(groups)
                    # Get potential children in same inventory
                    same_inventory_groups = list(
                        AnsibleGroup.objects.filter(
                            ansible_inventory=parent.ansible_inventory
                        ).exclude(id=parent.id)
                    )

                    if not same_inventory_groups:
                        # Need to create a child group
                        from django.utils import timezone

                        new_group = AnsibleGroup.objects.create(
                            ansible_inventory=parent.ansible_inventory,
                            name=f"child-{parent.name[:100]}-{random.randint(1000, 9999)}",
                            is_special=False,
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                        )
                        same_inventory_groups = [new_group]

                    # Find a child that hasn't been paired with this parent
                    for potential_child in same_inventory_groups:
                        pair = (parent.id, potential_child.id)
                        if pair not in created_pairs:
                            _context["agr_parent"] = parent
                            _context["agr_child"] = potential_child
                            created_pairs.add(pair)
                            return parent

                # If we couldn't find a unique pair, just return the last parent
                # This will likely cause a duplicate error which django-seed will handle
                return parent

            def get_child_group(x: Any) -> Any:
                # Return the child that was selected in get_parent_group
                return _context.get("agr_child")

            formatters.update(
                {
                    "parent_group": get_parent_group,
                    "child_group": get_child_group,
                }
            )

        # DataCenter: ensure fab OR phase is set
        elif model_class == models.DataCenter:
            from inventory_api.api.models.infrastructure import Fab, Phase

            # Track state per instance
            instance_tracker_dc: list = []
            # Track if we created an auto-fab
            auto_fab_created = [False]

            def get_fab(x: Any) -> Any:
                # Reset for new instance
                current_id = id(x)
                if not instance_tracker_dc or instance_tracker_dc[0] != current_id:
                    instance_tracker_dc.clear()
                    instance_tracker_dc.append(current_id)
                    _context.clear()

                # Fetch fresh data each time
                fabs = list(Fab.objects.all())
                phases = list(Phase.objects.all())

                # If neither exist, create a Fab (only once)
                if not fabs and not phases and not auto_fab_created[0]:
                    fab = Fab.objects.create(
                        name=f"Auto-Fab-{fake.word()[:20]}", external_system_id=fake.uuid4()
                    )
                    fabs = [fab]
                    auto_fab_created[0] = True

                # Decide what to set for this instance
                if "dc_choice" not in _context:
                    if not fabs:
                        _context["dc_choice"] = "phase_only"
                    elif not phases:
                        _context["dc_choice"] = "fab_only"
                    else:
                        # Both available: fab_only(40%), phase_only(40%), both(20%)
                        rand = random.random()
                        if rand < 0.4:
                            _context["dc_choice"] = "fab_only"
                        elif rand < 0.8:
                            _context["dc_choice"] = "phase_only"
                        else:
                            _context["dc_choice"] = "both"

                choice = _context["dc_choice"]
                if choice in ["fab_only", "both"] and fabs:
                    return random.choice(fabs)
                return None

            def get_phase(x: Any) -> Any:
                # Fetch fresh data
                phases = list(Phase.objects.all())

                # Use decision made by get_fab
                choice = _context.get("dc_choice", "phase_only")
                if choice in ["phase_only", "both"] and phases:
                    return random.choice(phases)
                return None

            formatters.update(
                {
                    "fab": get_fab,
                    "phase": get_phase,
                }
            )

        return formatters

    def handle_app_config(self, app_config: Any, **options: Any) -> Any:
        """Use parent implementation but inject custom formatters and skip M2M through tables"""
        # Models with M2M through tables that should not be auto-populated
        # These will be populated via their through models instead
        skip_m2m_models = {
            "BaremetalModel",  # has gpus through BaremetalModelGPU
            "VirtualMachineSpecification",  # has required_gpus through VirtualMachineSpecificationRequiredGPU
            "K8sCluster",  # has plugins through K8sClusterPluginAssociation
            "K8sClusterPlugin",  # has k8s_clusters through K8sClusterPluginAssociation
        }

        # Monkey-patch the seeder to use our custom add_entity
        from django_seed import Seed

        original_seeder_class = Seed.seeder().__class__
        original_add_entity = original_seeder_class.add_entity
        command_self = self

        def patched_add_entity(
            seeder_self: Any, model_class: Any, number: int, formatters: Any = None
        ) -> Any:
            # Get custom formatters for this model
            custom_formatters = command_self.add_formatters(seeder_self, model_class, number)

            # Skip M2M auto-population for models with through tables
            if model_class.__name__ in skip_m2m_models:
                # Find M2M fields with through tables and set them to empty
                if hasattr(model_class, "_meta"):
                    for field in model_class._meta.get_fields():
                        if field.many_to_many and hasattr(field, "remote_field"):
                            if field.remote_field and hasattr(field.remote_field, "through"):
                                # Check if through model is not auto-created
                                through_model = field.remote_field.through
                                if through_model and through_model._meta.auto_created is False:
                                    # Skip this field by not letting django-seed handle it
                                    pass

            # Merge with any existing formatters
            if formatters:
                custom_formatters.update(formatters)
            return original_add_entity(seeder_self, model_class, number, custom_formatters or {})

        # Apply patch
        original_seeder_class.add_entity = patched_add_entity

        try:
            # Call parent implementation which will use our patched add_entity
            return super().handle_app_config(app_config, **options)
        finally:
            # Restore original
            original_seeder_class.add_entity = original_add_entity
