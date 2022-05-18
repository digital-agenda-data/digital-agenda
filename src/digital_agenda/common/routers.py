from rest_framework_nested import routers


class DefaultExtendableRouter(routers.DefaultRouter):
    def extend(self, router):
        self.registry.extend(router.registry)
