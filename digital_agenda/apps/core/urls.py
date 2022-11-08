from digital_agenda.common.routers import DefaultExtendableRouter

from .routers import main_routers, nested_routers


root = DefaultExtendableRouter()

for router in main_routers:
    root.extend(router)


urlpatterns = root.urls + [url for router in nested_routers for url in router.urls]
