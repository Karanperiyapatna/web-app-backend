from rest_framework import serializers
from .models import Labour, Requirement, BabyCaretakerRequirement, UploadedPhoto, EmpBabyCaretaker, ElderCaretaker, EmpElderCaretaker

from .models import Cleaner, Cooking, Tankcleaner, Driver, EmpCleaner, EmpCooking, EmpTankcleaner, EmpDriver



# ----------------------------------------------------------------------------- Labour registration Form

from rest_framework import serializers
from .models import UserSignup

class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSignup
        fields = '__all__'

# --------------------------------------------------------------------------------------------------


class LabourSerializer(serializers.ModelSerializer):
	class Meta:
		model = Labour
		fields = '__all__'

class RequirementSerializer(serializers.ModelSerializer):
	class Meta:
		model = Requirement
		fields = '__all__'

class BabyCaretakerRequirementSerializer(serializers.ModelSerializer):
	class Meta:
		model = BabyCaretakerRequirement
		fields = '__all__'

class UploadedPhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = UploadedPhoto
		fields = '__all__'

class ElderCaretakerSerializer(serializers.ModelSerializer):
	class Meta:
		model = ElderCaretaker
		fields = '__all__'


class CookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cooking
		fields = '__all__'

class CleanerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cleaner
		fields = '__all__'

class TankcleanerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tankcleaner
		fields = '__all__'

class DriverSerializer(serializers.ModelSerializer):
	class Meta:
		model = Driver
		fields = '__all__'

class EmpBabyCaretakerSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmpBabyCaretaker
		fields = '__all__'

class EmpElderCaretakerSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmpElderCaretaker
		fields = '__all__'

class EmpCleanerSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmpCleaner
		fields = '__all__'

class EmpCookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmpCooking
		fields = '__all__'

class EmpTankcleanerSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmpTankcleaner
		fields = '__all__'

class EmpDriverSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmpDriver
		fields = '__all__'



# ------------------------------------------------------------------------  Get AC Repair Labour List
from rest_framework import serializers
from .models import EmpOtherServiceWorker

class EmpOtherServiceWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpOtherServiceWorker
        fields = '__all__'

