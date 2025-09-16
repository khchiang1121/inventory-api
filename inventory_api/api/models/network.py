from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .base import AbstractBase


class VLAN(AbstractBase):
    """VLAN model for network segmentation"""

    vlan_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=64)


class VRF(AbstractBase):
    """VRF (Virtual Routing and Forwarding) model"""

    name = models.CharField(max_length=64, unique=True)
    route_distinguisher = models.CharField(max_length=64)


class BGPConfig(AbstractBase):
    """BGP configuration model"""

    asn = models.PositiveIntegerField(help_text="Autonomous System Number")
    peer_ip = models.GenericIPAddressField(protocol="IPv4", help_text="BGP peer IP")
    local_ip = models.GenericIPAddressField(protocol="IPv4", help_text="Local BGP IP")
    password = models.CharField(max_length=64, blank=True)


class NetworkInterface(AbstractBase):
    """Network interface model for devices"""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    resource = GenericForeignKey("content_type", "object_id")

    name = models.CharField(max_length=64, help_text="Interface name, e.g., eth0")
    mac_address = models.CharField(max_length=32, help_text="MAC address")
    is_primary = models.BooleanField(default=False, help_text="Marks primary interface")

    ipv4_address = models.GenericIPAddressField(protocol="IPv4", null=True, blank=True)
    ipv4_netmask = models.GenericIPAddressField(
        protocol="IPv4", null=True, blank=True, help_text="IPv4 netmask"
    )
    ipv6_address = models.GenericIPAddressField(
        protocol="IPv6", null=True, blank=True, help_text="IPv6 address"
    )
    ipv6_netmask = models.GenericIPAddressField(
        protocol="IPv6", null=True, blank=True, help_text="IPv6 netmask"
    )
    gateway = models.GenericIPAddressField(null=True, blank=True, help_text="Default gateway")
    dns_servers = models.CharField(
        max_length=255, blank=True, help_text="Comma-separated list of DNS servers"
    )

    vlan = models.ForeignKey(VLAN, null=True, blank=True, on_delete=models.SET_NULL)
    vrf = models.ForeignKey(VRF, null=True, blank=True, on_delete=models.SET_NULL)
    bgp_config = models.OneToOneField(BGPConfig, null=True, blank=True, on_delete=models.SET_NULL)
