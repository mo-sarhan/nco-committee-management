
from django.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter
from apps.person.views import AfrPersonView
from apps.users.views import CustomTokenObtainView
from apps.report.views import (
    PhotoReportViewSet,
    LagnaAfrReportViewSet,
)
from apps.users.views import AccountViewSet
from apps.photos.views import (
    UploadImageView,
    RejectImageView
)
from apps.tanzem.views import (
    ArmyCodeViewSet,
    RankViewSet,
)
from apps.uisettings.views import (
    UiSectionViewSet,
    UiFieldViewSet,
    UiPageConfigView,
)
from apps.lagna.views import (
    LagnaViewSet,
    LagnaPersonsViewSet,
    LagnaMemberViewSet,
    LagnaPersonsOpinionViewSet,
    LagnaTypeSpacificViewSet,
    LagnaOpinionsViewSet,
    ConsPonsViewSet,
    BenefitTypeViewSet,
    CommanderJobTypeViewSet,
    LagnaAfrStatusViewSet,
)
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import (
    get_schema_view

)

from django.urls import path 


swagger_view =get_schema_view(
    openapi.Info(
        title="Swagger api",
        description='alsdfj',
        default_version="v1",
    ),
    public=True,
    permission_classes=[AllowAny]

)

# for login and auth
urlpatterns = [
    path('login/',view=CustomTokenObtainView.as_view(),name='login')
]

persons = DefaultRouter()
persons.register('persons',AfrPersonView,'persons')
# for person app
urlpatterns += [
    path('',view=include(persons.urls))
    # path('persons/',view=AfrPersonView().as_view(),name='persons'),
    # path('persons/<str:pk>/',view=AfrPersonDetailsView().as_view(),name='persons'),
]

urlpatterns += [
    path('swagger/',swagger_view.with_ui('swagger',cache_timeout=0),name='schema'),
    path('swagger/redoc/',swagger_view.with_ui('redoc',cache_timeout=0),name='swagger_ui'),

]


# for photo app
urlpatterns +=[
    path('photo/',view=UploadImageView().as_view(),name='upload-image'),
    path('rejection-reasons/',view=RejectImageView().as_view(),name='refuse-image')

]

# for report photo
report_router = DefaultRouter()
report_router.register('report',PhotoReportViewSet,basename='photo-report')

lagna_router = DefaultRouter()
lagna_router.register('lagna',LagnaAfrReportViewSet,basename='lagna-report')
urlpatterns +=[
    path('photo/',include(report_router.urls)),
    path('report/',include(lagna_router.urls)),
]


# for lagna app
lagna_router = DefaultRouter()
lagna_router.register(r'lagna',LagnaViewSet,basename='lagna')
lagna_router.register(r'lagna-persons',LagnaPersonsViewSet,basename='lagna-persons')
lagna_router.register(r'lagna-member',LagnaMemberViewSet,basename='lagna-member')
lagna_router.register(r'lagna-persons-opinion',LagnaPersonsOpinionViewSet,basename='lagna-persons-opinion')
lagna_router.register(r'lagna-spacific',LagnaTypeSpacificViewSet,basename='lagna-spacific')
lagna_router.register(r'opinion-types',LagnaOpinionsViewSet,basename='opinion-types')
lagna_router.register(r'pons-cons',ConsPonsViewSet,basename='pons-cons')
lagna_router.register(r'benefit',BenefitTypeViewSet,basename='benefit')
lagna_router.register(r'commander-job',CommanderJobTypeViewSet,basename='commander-job')
lagna_router.register(r'person-status',LagnaAfrStatusViewSet,basename='lagna-person-status')

urlpatterns +=[
    path('',include(lagna_router.urls)),
]


# for user app
user_router = DefaultRouter()
user_router.register(r'accounts',AccountViewSet,basename='account')

urlpatterns +=[
    path('',include(user_router.urls))
]


# for tanzem app
tanzem_router = DefaultRouter()
tanzem_router.register(r'army',ArmyCodeViewSet,basename='army')
tanzem_router.register(r'rank',RankViewSet,basename='rank')
urlpatterns +=[
    path('',include(tanzem_router.urls))
]


# for ui settings app
ui_router = DefaultRouter()
ui_router.register(r'sections',UiSectionViewSet,basename='ui-section')
ui_router.register(r'fields',UiFieldViewSet,basename='ui-field')

urlpatterns +=[
    path('ui-settings/',include(ui_router.urls)),
    path('ui-settings/pages/<str:page_key>/',view=UiPageConfigView.as_view(),name='ui-page-config'),
]