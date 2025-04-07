from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LabourViewSet, RequirementViewSet,  search_babycare, upload_photo, EmpTankcleaner, EmpDriver, emp_baby_caretaker, Tankcleaner, Driver
from .views import get_acrepair_workers, user_signup, user_login, user_logout
from .views import search_eldercare, search_cleaner, search_cook, search_helper, search_otherservice
from .views import emp_elder_caretaker, emp_cleaner, emp_cooking, emp_helper
from .views import requirement_cleaner, requirement_helper, requirement_babycaretaker, requirement_eldercaretaker, requirement_cooking
from .views import emp_otherservice , store_CustomerData, check_subscription
from .views import agent_signup, partner_signup, agent_login, agent_logout

router = DefaultRouter()
router.register(r'labours', LabourViewSet)
router.register(r'requirements', RequirementViewSet)

urlpatterns = [
	path('', include(router.urls)),   # Include the DRF router URLs

	path('api/user/user-signup/', user_signup, name='user_signup'),
	path('api/user/user-login/', user_login, name='user_login'),
	path('api/user/user-logout/', user_logout, name='user_logout'),

	path('api/requirements/baby-caretaker/', requirement_babycaretaker, name='post_requirement'),
	path('api/requirements/elder-caretaker/', requirement_eldercaretaker, name='post_requirement'),
	path('api/requirements/cleaner/', requirement_cleaner, name='Cleaner'),
	path('api/requirements/cooking/', requirement_cooking, name='Cooking'),
	path('api/requirements/helper/', requirement_helper, name='Helper'),

	path('api/Tankcleaner/', Tankcleaner, name='Tankcleaner'),
	path('api/Driver/', Driver, name='Driver'),

	path('api/acrepair/', get_acrepair_workers, name='acrepair-workers'),

	path('api/employees/baby-caretaker/', emp_baby_caretaker, name='emp_baby_caretaker'),
	path('api/employees/elder-caretaker/', emp_elder_caretaker, name='EmpElderCaretaker'),
	path('api/employees/labour-cooking/', emp_cooking, name='EmpCooking'),
	path('api/employees/labour-cleaner/', emp_cleaner, name='EmpCleaner'),
	path('api/employees/labour-otherservice/', emp_otherservice, name='EmpOtherServiceWorker'),
	path('api/EmpTankcleaner/', EmpTankcleaner, name='EmpTankcleaner'),
	path('api/EmpDriver/', EmpDriver, name='EmpDriver'),
	path('api/employees/helper/', emp_helper, name='EmpHelper'),	

	path('api/search/labour-babycaretaker/', search_babycare, name='search-labour-babycaretaker'),
	path('api/search/labour-eldercaretaker/', search_eldercare, name='search-labour-eldercaretaker'),
	path('api/search/labour-cleaner/', search_cleaner, name='search-labour-cleaner'),
	path('api/search/labour-cook/', search_cook, name='search-labour-cook'),
	path('api/search/labour-helper/', search_helper, name='search-labour-helper'),
	path('api/search/labour-otherservice/', search_otherservice, name='search-labour-otherservice'),
	
	path("api/storeCustomerData/", store_CustomerData, name="storeCustomerData"),
	path("api/check-subscription/", check_subscription, name="checksubscription"),

	path("upload/", upload_photo, name="upload-photo"),

	path("api/agent/agent-login/", agent_login, name="agent_login"),
	path("api/agent/agent-signup/", agent_signup, name="agent_signup"),
	path('api/agent/agent-logout/', agent_logout, name='agent_logout'),
	path("api/dromant/partner-signup/", partner_signup, name="partner_signup"),
	
]


from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# Add this to serve media files in development
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)