import re

from drf_spectacular.openapi import AutoSchema


def split_camel_case(name: str) -> str:
    """
    將 CamelCase 字串轉為有空格的表示，例如：
    'OrderManagementViewSet' ➜ 'Order Management'
    """
    name = name.replace("ViewSet", "")  # 移除 ViewSet 後綴
    name = re.sub(r"(?<!^)(?=[A-Z])", " ", name)
    return name.strip()


class CustomAutoSchema(AutoSchema):
    def get_override_view_name(self) -> str:
        view = self.view
        if hasattr(view, "__class__"):
            name = view.__class__.__name__
            return name
        return super().get_override_view_name()  # type: ignore

    def get_tags(self) -> list[str]:
        override_tag = self.get_override_view_name()
        return [override_tag] if override_tag else super().get_tags()  # type: ignore
