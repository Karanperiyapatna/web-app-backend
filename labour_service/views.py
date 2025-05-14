from django.shortcuts import render
from django.http import JsonResponse
from .models import Labour

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Labour  # Assuming you have a Labour model
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from pymongo import MongoClient

from rest_framework import viewsets
from .models import Labour, Requirement
from .serializers import LabourSerializer, RequirementSerializer

# api/views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BabyCaretakerRequirementSerializer

from pymongo import MongoClient
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import status


from datetime import datetime, timedelta

class LabourViewSet(viewsets.ModelViewSet):
	queryset = Labour.objects.all()
	serializer_class = LabourSerializer

class RequirementViewSet(viewsets.ModelViewSet):
	queryset = Requirement.objects.all()
	serializer_class = RequirementSerializer


from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Labour  

import json
from django.http import JsonResponse
from pymongo import MongoClient
from bson import ObjectId  

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import os



# ------------------------------------------------------------------------- Database Connection Details

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/") 
db = client["digi_labour"] 
labour_db = client["labours_data"]
users_db = client['user_data']  
orders = client["orders"]
req_db = client["requirements_data"]
agent_db = client["agent_data"]
dormant_db = client["dormant_data"]

transactions = client["transactions"]
subscription_db = client["subscription_data"]
check_subscription_col = users_db["users_data"]

labour_db["labour_signup"]
labour_credit_claim_col = labour_db['labour_credit_claim']

payment_transactions = transactions["payment_transactions"]

EmpBabycaretaker_col = labour_db["labour_baby_caretaker"] 
EmpElderCaretaker_col = labour_db["labour_elder_caretaker"] 
EmpCooking_col = labour_db["labour_cooking"] 
EmpCleaner_col = labour_db["labour_cleaner"] 
EmpHelper_col = labour_db["labour_helper"]

EmpTankcleaner_col = labour_db["labour_tank_cleaner"] 
EmpDriver_col = labour_db["labour_car_driver"] 
emp_otherservice_col = labour_db["labour_otherservice"]

req_babycaretaker_col = req_db["req_baby_caretaker"]
req_elder_caretaker_col = req_db["req_elder_caretaker"] 
req_cooking_col  = req_db["req_cooking"] 
req_cleaner_col = req_db["req_cleaner"] 
req_tank_cleaner_col = req_db["req_tankcleaner"] 
req_driver_col = req_db["req_driver"]   
req_helper_col =  req_db["req_helper"]   


get_acrepair_col = labour_db["EmpOtherservice"]
Customer_info_col = subscription_db["users_data"]

user_signup_col = users_db['users_data']  
agent_signup_col = agent_db["agent_signup"]
agent_credit_claim_col = agent_db['agent_credit_claim']

dromant_signup_col = dormant_db["partner_signup"]



#----------------------------------------------------------------- Collection Loopup based on the Labour code

# Global mapping of 2-letter codes to their respective collections
EMPLOYEE_COLLECTION_MAP = {
	"BC": EmpBabycaretaker_col,
	"HP": EmpHelper_col,
	# Add other mappings here, e.g.:
	# "CK": EmpCook_col,
	# "DR": EmpDriver_col,
}



# ------------------------------------------------------------------------ Generate 8 Digit Order ID

import random
import string

def generate_order_id():
	return str(random.randint(10000000, 99999999))

def generate_employee_id():
	return str(random.randint(10000000, 99999999))


def generate_agent_id(agent_name, mobile_number):
	if not agent_name or not mobile_number:
		return "UNKNOWN"  # Fallback value
	return ("AGT" + mobile_number[-3:]  + agent_name[:3]).upper()


def generate_employee_id(labour_name, mobile_number, work_header):
	name_part = labour_name[:3].upper() if labour_name else "XXX"
	mobile_part = mobile_number[-4:] if len(mobile_number) >= 4 else "0000"
	labour_id = f"{name_part}{mobile_part}{work_header}"

	return labour_id

def generate_user_id(labour_name, mobile_number):
	name_part = labour_name[:3].upper() if labour_name else "XXX"
	mobile_part = mobile_number[-4:] if len(mobile_number) >= 4 else "0000"
	user_id = f"{name_part}{mobile_part}"

	return user_id

import uuid

# Function to generate a 10-character alphanumeric sequence ID
def generate_sequence_id():
	return uuid.uuid4().hex[:16].lower()


# -------------------------------------------------------------------------- User Registration Details
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view




from django.utils.dateparse import parse_date

@api_view(['POST'])
def check_subscription_user(request):
    print("Requested data for check subscription is:", request.data)  # Log the request data

    # Get values from the request
    mobile_number = request.data.get("mobile_number")
    user_name = request.data.get("username")
    subscription_type = request.data.get("subscription_type", "plus")  # Default to 'plus' if not provided
    
    # Validate required fields
    if not mobile_number or not user_name:
        return Response({"error": "Mobile number and username are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Search for the user in the database
    user = check_subscription_col.find_one({
        "mobile_number": mobile_number,
        "user_name": user_name
    })
    print("printing the user for checking subscription :", user)

    if not user:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # Fetch subscription data
       # Extract subscription-related fields from user record
    subscription_status = int(user.get("subscription_status", 0))
    credit_points = int(user.get("credit_points", 0))
    start_date = user.get("susbcription_start_date", "NA")  # typo in field: susbcription_...


    if subscription_status == 1 and start_date != "NA":
        if isinstance(start_date, str):
            parsed_start = parse_date(start_date)
        else:
            parsed_start = start_date

        if parsed_start:
            days_passed = (datetime.now().date() - parsed_start).days
            days_left = max(30 - days_passed, 0)
        else:
            days_left = "Unknown"

        return Response({
            "subscription_status": 1,
            "credit_points": credit_points,
            "discounted_amount": 0,
            "days_left": days_left
        })

    # No active subscription
    discounted_amount = 50 if subscription_type == 'plus' else 100

    return Response({
        "subscription_status": 0,
        "credit_points": 0,
        "discounted_amount": discounted_amount,
        "days_left": 0})



@api_view(['POST'])
def payment_subscription_user(request):
    print("Requested data for payment check subscription is:", request.data)

    username = request.data.get('username')
    mobile_number = request.data.get('mobile_number')
    subscription_type = request.data.get('subscription_type')
    transaction_id = request.data.get('transaction_id')

    if not all([username, mobile_number, subscription_type, transaction_id]):
        return Response({'error': 'Missing required fields'}, status=400)

    user = user_signup_col.find_one({'username': username, 'mobile_number': mobile_number})

    if not user:
        return Response({'error': 'User not found'}, status=404)

    # Calculate subscription duration
    remaining_days = 30 if subscription_type == 'plus' else 60
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=remaining_days)

    # Update user subscription in MongoDB
    user_signup_col.update_one(
        {'_id': user['_id']},
        {'$set': {
            'subscription_type': subscription_type,
            'subscription_start_date': start_date.strftime('%Y-%m-%d'),
            'subscription_remaining_day': remaining_days,
            'transaction_id': transaction_id,
            'subscription_status': 1  # mark as active
        }}
    )

    return Response({
        'message': 'Subscription updated successfully.',
        'remaining_days': remaining_days,
        'transaction_id': transaction_id
    })




from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['POST'])
def user_signup(request):
	data = request.data
	print("Recieving the User Singup Details :", data)

	labour_name = data.get("name")
	mobile_number = data.get("mobile_number")
	try:
		customer = {
			"user_id" : generate_user_id(labour_name, mobile_number), 
			"user_name": data.get("name"),
			"password": data.get("password"),
			"mobile_number": data.get("mobile_number"),
			"alternative_mobile_number": data.get("alt_mobile_number"),
			"email": data.get("email"),
			"address": data.get("address"),
			"city": data.get("city"),
			"state": data.get("state"),
			"pincode": data.get("pincode"),
			"subscription_status" : 0,
			"credit_points" : 0,
			"agreed_terms_conditions": data.get("agreeTerms"),
			"susbcription_type" : data.get("susbcription_type") or "NA",
			"susbcription_start_date" : data.get("susbcription_start_date") or "NA",
			"susbcription_remaining_day" : data.get("susbcription_remaining_days") or "NA",
			
		}
		user_signup_col.insert_one(customer)
		return Response({"message": "Customer data stored successfully!"}, status=201)
	except Exception as e:
		return Response({"error": str(e)}, status=500)


from django.http import JsonResponse

@api_view(['POST'])
def user_login(request):
	print("Received a request to user_login")  # Add this line

	try:
		data = request.data
		print("Received Login Data:", data)  # Check if this prints

		username = data.get("username")
		password = data.get("password")

		if not username or not password:
			return Response({"error": "Username and password are required"}, status=400)

		# Fetch user from MongoDB and directly compare passwords
		user = user_signup_col.find_one({"user_name": username, "password": password}, {"_id": 0})

		if user:
			return Response({
				"message": "Login successful",
				"user_id": user["user_id"],
				"name": user["user_name"],
				"credit_points" : user["credit_points"],
			}, status=200)
		else:
			return Response({"error": "Invalid credentials"}, status=401)

	except Exception as e:
		print("Error in user_login:", str(e))  # Print error message
		return JsonResponse({"error": "Internal server error"}, status=500)
	
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def user_subscription_status(request, user_id):
    try:
        user = user_signup_col.find_one({"user_id": user_id})
        if user:
            return Response({
                "subscription_status": user.get("subscription_status", 0),
                "credit_points": user.get("credit_points", 0)
            }, status=200)
        else:
            return Response({"error": "User not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

	

from django.contrib.auth import logout
from django.http import JsonResponse

@api_view(['POST'])
def user_logout(request):
	if request.method == 'POST':
		logout(request)  # Logs out user
		response = JsonResponse({"message": "Logout successful!"})
		response.delete_cookie('sessionid')  # Remove session ID cookie
		response.delete_cookie('csrftoken')  # Remove CSRF token if stored in cookies
		request.session.flush()  # Clear the session completely
		return response
	return JsonResponse({"error": "Invalid request"}, status=400)



# --------------------------------------------------------------------------- Agent Signup


from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status



@api_view(['POST'])
def agent_creditclaim(request):
	data = request.data
	print("Agent Credit Claim Amount is :", data)

	# Ensure required fields are present
	required_fields = ['userId', 'name', 'claimedAmount', 'accountHolder', 'bankName', 'accountNumber', 'ifscCode']
	for field in required_fields:
		if field not in data:
			return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

	# Rename for clarity
	userId = data['userId']  # Using userId as agent_id

	# Add additional fields
	data['userId'] = userId
	data['claimed_at'] = datetime.utcnow()
	data['process_status'] = 0

	try:
		# Check if a similar claim already exists
		existing_claim = agent_credit_claim_col.find_one({
			'userId': userId,
			'process_status': {'$in': [0, 777]}
		})

		if existing_claim:
			return Response({'message': 'Claim already exists with status 0 or 777'}, status=status.HTTP_200_OK)

		# Insert into MongoDB
		result = agent_credit_claim_col.insert_one(data)
		return Response({'message': 'Claim request submitted successfully', 'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)

	except Exception as e:
		print("Error inserting data:", e)
		return Response({'error': 'Failed to submit claim'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def agent_signup(request):
	data = request.data
	print("Recieving the User Singup Details :", data)

	labour_name = data.get("name")
	mobile_number = data.get("mobile_number")
	try:
		customer = {
			"agent_id" : generate_agent_id(labour_name, mobile_number), 
			"agent_name": data.get("name"),
			"username" : data.get("username"),
			"password": data.get("password"),
			"mobile": data.get("mobile_number"),
			"alternative_mobile": data.get("alt_mobile_number"),
			"email": data.get("email"),
			"address": data.get("address"),
			"city": data.get("city"),
			"state": data.get("state"),
			"pincode": data.get("pincode"),
			"subscription_status" : 0,
			"credit_points" : 0,

			"registered_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,  # after verification, 777 become 1
			"process_status_result" : "application applied, waiting for approval from company", # Update if have any status result
			"work_status" : 0,  # 1 means ready to work, 0 means not available
			"user_credits_consumed" : 0, # change the value as user fetch the mobile number
			"feedback_credits" : 0, # change the value whenever give stars to labour
			"labour_rewards": 0, # change the value whenever labour get credits more than 1000rs transaction

			"transaction_credits_consumed" : 0, # concept of 1000rs transaction
			"comp_transaction_credits_consumed" : 0,  # concept of 50 points from 1000 points
			"referred_transaction_credits_consumed" : 0, # concept of 
			"company_end_work_status" : 0, # If they crosses/high demand for this labour - make charge in future
			"company_end_work_status_reason" : "Still Not yet cross 1000 user_credit_consumed"

			
		}
		agent_signup_col.insert_one(customer)
		return Response({"message": "Customer data stored successfully!"}, status=201)
	except Exception as e:
		return Response({"error": str(e)}, status=500)




@api_view(['POST'])
def agent_login(request):
	print("Received a request to user_login")  # Add this line

	try:
		data = request.data
		print("Received Login Data:", data)  # Check if this prints

		username = data.get("username")
		password = data.get("password")

		if not username or not password:
			return Response({"error": "Username and password are required"}, status=400)

		# Fetch user from MongoDB and directly compare passwords
		user = agent_signup_col.find_one({"username": username, "password": password})

		if user:
			print("fetched agent details is :", user)

			user_credits_consumed = user["user_credits_consumed"]
			referred_transaction_credits_consumed = user["referred_transaction_credits_consumed"]
			comp_transaction_credits_consumed = user["comp_transaction_credits_consumed"]

			Consumed_Credit_Point = int(user_credits_consumed) + int(referred_transaction_credits_consumed )
			Total_credit_Point = int(Consumed_Credit_Point - comp_transaction_credits_consumed)
			print("Agent Total_credit_Point is :", Total_credit_Point)

			return Response({
				"message": "Login successful",
				"user_id": user["agent_id"],
				"name": user["agent_name"],
				"user_credits_consumed" : user['user_credits_consumed'],
				"Total_credit_Point" : Total_credit_Point
			}, status=200)
		else:
			return Response({"error": "Invalid credentials"}, status=401)

	except Exception as e:
		print("Error in user_login:", str(e))  # Print error message
		return JsonResponse({"error": "Internal server error"}, status=500)
	



@api_view(['POST'])
def agent_logout(request):
	if request.method == 'POST':
		logout(request)  # Logs out user
		response = JsonResponse({"message": "Logout successful!"})
		response.delete_cookie('sessionid')  # Remove session ID cookie
		response.delete_cookie('csrftoken')  # Remove CSRF token if stored in cookies
		request.session.flush()  # Clear the session completely
		return response
	return JsonResponse({"error": "Invalid request"}, status=400)


	

#  -------------------------------------------------------------------------- Dromant Registration Page





@api_view(['POST'])
def partner_signup(request):
	data = request.data
	print("Agent Registration form details :", data)

	try:
		agent_name = data.get("username")
		mobile_number = data.get("mobile_number")
				# Ensure agent_name and mobile_number are not None
		if not agent_name or not mobile_number:
			return Response({"error": "Username or Mobile Number is missing"}, status=400)

		partner_id = generate_agent_id(agent_name, mobile_number)
		print("Agent ID is :", partner_id)
		customer = {
			"agent_name": data.get("username"),
			"mobile_number": data.get("mobile_number"),
			"alternative_mobile": data.get("alternative_mobile"),
			"email": data.get("email"),
			"address": data.get("address"),
			"city": data.get("city"),
			"state": data.get("state"),
			"pincode": data.get("pincode"),
			"password": data.get("password"),
			# "agent_id" : generate_user_id(), 
			"aprtner_id" : partner_id, 
		}
		print("Agent Register Details : ", customer)
		dromant_signup_col.insert_one(customer)
		return Response({"message": "Customer data stored successfully!"}, status=201)
	except Exception as e:
		return Response({"error": str(e)}, status=500)



#  ------------------------------------------------------------------------------ User Registration Block

from django.http import JsonResponse

@api_view(['POST'])
def user_login(request):
	print("Received a request to user_login")  # Add this line

	try:
		data = request.data
		print("Received Login Data:", data)  # Check if this prints

		username = data.get("username")
		password = data.get("password")

		if not username or not password:
			return Response({"error": "Username and password are required"}, status=400)

		# Fetch user from MongoDB and directly compare passwords
		user = user_signup_col.find_one({"user_name": username, "password": password}, {"_id": 0})

		if user:
			return Response({
				"message": "Login successful",
				"user_id": user["user_id"],
				"name": user["user_name"],
				"subscription_status" : user["subscription_status"],
				"credit_points" : user["credit_points"]
			}, status=200)
		else:
			return Response({"error": "Invalid credentials"}, status=401)

	except Exception as e:
		print("Error in user_login:", str(e))  # Print error message
		return JsonResponse({"error": "Internal server error"}, status=500)


# ----------------------------------------------------------------------------- Store Customer Details

@api_view(["POST"])
def store_CustomerData(request):
	data = request.data
	print("serach Baby caretaker labour data by User :", data)
	try:
		customer = {
			"user_name": data.get("username"),
			"mobile_number": data.get("mobile"),
			"mail_id": data.get("email"),
			"work_category" : data.get("work_category"),
			'agreedToTerms': data.get("agreedToTerms"),
			"processed_datetime": datetime.now(), 
			"fetched_labour_id": data.get("labour_id"),
			"fetched_labour_name": data.get("labour_name")

		}
		result = Customer_info_col.insert_one(customer)
		return Response({
            "message": "Customer data stored successfully!",
            "_id": str(result.inserted_id)  # send _id back as string
        }, status=201)

	except Exception as e:
		return Response({"error": str(e)}, status=500)


# --------------------------------------------------------------------------- Get AC Repair Labour List



@api_view(['GET'])
def get_acrepair_workers(request):
	query = {"work_category": "acrepair"}
	workers = list(get_acrepair_col.find(query, {"_id": 0}))  
	return Response(workers)


# ----------------------------------------------------------------------------- Helper



@api_view(["POST"])
def search_helper(request):
	if request.method == "POST":
		try:
			# Decode JSON request
			data = json.loads(request.body.decode("utf-8"))
			print("request labour data for baby caretaker :", data)

			gender = data.get("gender")
			careLocation = data.get("careLocation") 
			area = data.get("area")  
			selected_category = data.get("selected_category")

			# Ensure required fields are present
			if not gender:
				return JsonResponse({"error": "Gender is required"}, status=400)
			if not careLocation:
				return JsonResponse({"error": "City is required"}, status=400)
			if not area:
				return JsonResponse({"error": "Area is required"}, status=400)
			if not selected_category:
				return JsonResponse({"error": "Category is required"}, status=400)

			# MongoDB Query
			query = {
				"gender": gender,
				"city": careLocation,
				"working_area": area,
				"sub_service_category":  {"$in": [selected_category]}
			}
			print("babycaretaker labour search query is :", query)

			# Fetch data from MongoDB

			labours = list(EmpHelper_col.find(query, {"full_name": 1, "gender": 1, "age": 1,  "sub_service_category": 1}))

			# Convert ObjectId to string for JSON serialization
			for labour in labours:
				if '_id' in labour:
					labour['_id'] = str(labour['_id'])

			print("fetched and passing babycaretaker labour details is :", labours)

			return JsonResponse({"labours": labours}, status=200)

		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON format"}, status=400)

		except Exception as e:
			return JsonResponse({"error": "Internal Server Error"}, status=500)

	return JsonResponse({"error": "Invalid request"}, status=400)





#  Baby Care Taker Requirements Code

@api_view(['POST'])
def requirement_helper(request):
	if request.method == 'POST':
		print("Request data is:", request.data)


		sequence_id = generate_sequence_id()	

		# Preparing Data for MongoDB
		requirement_data = {
			"sequence_id" :  uuid.uuid4().hex[:16].lower(),
			"order_id": generate_order_id(), # Generate and print a unique 8-character word
			"order_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,
			"process_status_result" : "requested for labour requirement, waiting for process", # Update if have any status result
			"service_category" : "housekeeping",
			"sub_service_category": request.data.get("selected_category"),

			"user_name": request.data.get("username"),
			"mobile_number": request.data.get("mobilenumber", 0),
			"alternative_mobile_number" : request.data.get("alternative_mobile_number", 0),
			"mail_id": request.data.get("email"),
			"address": request.data.get("address"),
			"pincode" : request.data.get("pincode"),

			"city": request.data.get("city"),
			"area": request.data.get("area"),
			"preferred_language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"preferred_gender": request.data.get("gender"),
			"preferred_priority": request.data.get("urgency"),
			"preferred_work_timings" : request.data.get("preferredworkTime"),
			"preferred_duration": request.data.get("duration"),
			"preferred_task": request.data.get("handling", "").split(",") ,# Handling multiple checkbox values
			
			"additional_note": request.data.get("additionalNotes"),
			"salary_offered": request.data.get("salaryOffered"),
		}

		# Insert into MongoDB
		result = req_helper_col.insert_one(requirement_data)

		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def labour_login(request):
	if request.method == 'POST':
		print("Request labour data is:", request.data)

		print("Request labour data is:", request.data)
		username = request.data.get('username')
		password = request.data.get('password')
		service_category = request.data.get('service_category')

		if not username or not password:
			return Response({"error": "Username and password are required"}, status=400)
		
		if service_category == "babycaretaker":
			labour_login_col = EmpBabycaretaker_col
		elif service_category == "eldercaretaker":
			labour_login_col = EmpElderCaretaker_col
		else:
			print("no labour collection found for login")
			return Response({'message': 'Invalid service category'}, status=status.HTTP_400_BAD_REQUEST)

		# Fetch user from MongoDB and directly compare passwords
		user = labour_login_col.find_one({"username": username, "password": password}, {"_id": 0})

		if user:
			user_credits_consumed = user["user_credits_consumed"]
			referred_transaction_credits_consumed = user["referred_transaction_credits_consumed"]
			comp_transaction_credits_consumed = user["comp_transaction_credits_consumed"]

			Consumed_Credit_Point = int(user_credits_consumed) + int(referred_transaction_credits_consumed )
			Total_credit_Point = int(Consumed_Credit_Point - comp_transaction_credits_consumed)

			return Response({
				"message": "Login successful",
				"labour_id": user["labour_id"],
				"labour_name": user["labour_name"],
				"user_credits_consumed" : user["user_credits_consumed"],
				"referred_transaction_credits_consumed" : user["referred_transaction_credits_consumed"], 
				"Total_credit_Point" : Total_credit_Point
			}, status=200)
		else:
			return Response({"error": "Invalid credentials"}, status=401)




@api_view(['POST'])
def labour_logout(request):
	if request.method == 'POST':
			
		logout(request)  # Logs out user
		response = JsonResponse({"message": "Logout successful!"})
		response.delete_cookie('sessionid')  # Remove session ID cookie
		response.delete_cookie('csrftoken')  # Remove CSRF token if stored in cookies
		request.session.flush()  # Clear the session completely
		return response
	return JsonResponse({"error": "Invalid request"}, status=400)



@api_view(['POST'])
def labour_creditclaim(request):
	data = request.data
	print("Agent Credit Claim Amount is :", data)

	# Ensure required fields are present
	required_fields = ['userId', 'name', 'claimedAmount', 'accountHolder', 'bankName', 'accountNumber', 'ifscCode']
	for field in required_fields:
		if field not in data:
			return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

	# Rename for clarity
	userId = data['userId']  # Using userId as agent_id

	# Add additional fields
	data['userId'] = userId
	data['claimed_at'] = datetime.utcnow()
	data['process_status'] = 0

	try:
		# Check if a similar claim already exists
		existing_claim = agent_credit_claim_col.find_one({
			'userId': userId,
			'process_status': {'$in': [0, 777]}
		})

		if existing_claim:
			return Response({'message': 'Claim already exists with status 0 or 777'}, status=status.HTTP_200_OK)

		# Insert into MongoDB
		result = agent_credit_claim_col.insert_one(data)
		return Response({'message': 'Claim request submitted successfully', 'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)

	except Exception as e:
		print("Error inserting data:", e)
		return Response({'error': 'Failed to submit claim'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def emp_helper(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Generate sequence ID
		sequence_id = generate_sequence_id()		


		# Convert handling field into an array (if provided)
		handling = request.data.getlist("handling[]")  # Get list directly from QueryDict
	
		if isinstance(handling, str):  # If handling is a string, convert to a list
			handling = [item.strip() for item in handling.split(",")]

		# Handling File Uploads (Save to Local Storage)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		# Define the base upload directory inside MEDIA_ROOT
		base_upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

		# Create a unique folder inside "uploads" using the sequence_id
		folder_path = os.path.join(base_upload_dir, sequence_id)
		os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists


		if photo:
			photo_name = f"{sequence_id}_{photo.name}"
			photo_path = os.path.join(folder_path, photo_name)

			# Save file properly using Django's default_storage
			default_storage.save(photo_path, ContentFile(photo.read()))


		if identity_card:
			identity_card_name = f"{sequence_id}_{identity_card.name}"
			identity_card_path = os.path.join(folder_path, identity_card_name)
				# Save file properly
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))

		# Generate labour ID
		labour_name = request.data.get("name", "").strip()
		mobile_number = request.data.get("mobilenumber", "0").strip()
		work_header = "HP"
		labour_id = generate_employee_id(labour_name, mobile_number , work_header)

		
		# Prepare data for MongoDB
		emp_helper_data = {
			"labour_id": labour_id,
			"sequence_id" : sequence_id,
			"labour_name": request.data.get("name"),
			"mail_id": request.data.get("email"),
			"mobile_number": int(request.data.get("mobilenumber", 0)),
			"gender": request.data.get("gender"),
			"age": int(request.data.get("age", 0)),
			"address": request.data.get("address"),
			"photo_path": photo_path  if photo else None,
			"id_card_path": identity_card_path  if identity_card else None,
			
			"username": request.data.get("username"),
			"password": request.data.get("password"),

			"city": request.data.get("careLocation"),
			'work_area': request.data.get("area"),
			"service_category" : "helper",
			"sub_service_category": handling,  # Store as array


			"handling_work": [item.strip() for item in request.data.get("handling", "").split(",")],  # Store as array

			"availability": [item.strip() for item in request.data.get("availability", "").split(",")], 
			"language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"charge_per_hour": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("experience"),
			"register_via" : request.data.get("refer"),
			"reference_id" : request.data.get("extraId"),
			"work_specialization": request.data.get("workdescription"),
			"registered_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,  # after verification, 777 become 1
			"process_status_result" : "application applied, waiting for approval", # Update if have any status result
			"work_status" : 1,  # 1 means ready to work, 0 means not available
			"user_credits_consumed" : 0, # change the value as user fetch the mobile number
			"feedback_credits" : 0, # change the value whenever give stars to labour

		}

		# Insert into MongoDB
		result = EmpHelper_col.insert_one(emp_helper_data)

		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!', 'labour_id': labour_id}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------------------------------------------------------------------------------- Babycaretaker Option Code

@api_view(["POST"])
def search_babycare(request):
	if request.method == "POST":
		try:
			# Decode JSON request
			data = json.loads(request.body.decode("utf-8"))
			print("request labour data for baby caretaker :", data)

			gender = data.get("gender")
			city = data.get("city")  # Get city
			area = data.get("area")  # Get area

			# Ensure required fields are present
			if not gender:
				return JsonResponse({"error": "Gender is required"}, status=400)
			if not city:
				return JsonResponse({"error": "City is required"}, status=400)
			if not area:
				return JsonResponse({"error": "Area is required"}, status=400)

			# MongoDB Query
			query = {
				"gender": gender,
				"city": city,
				"work_area": area
			}
			print("babycaretaker labour search query is :", query)

			# Fetch data from MongoDB
			labours = list(EmpBabycaretaker_col.find(query, {
					"_id" :1,
					"labour_name": 1, 
					"gender": 1, 
					"age": 1, 
					"experience" : 1 , 
					"mobile_number" : 1, 
					"photo_path" : 1,
					"labour_id" : 1,
					"register_via": 1,
					"referred_by_agent": 1,
					"referred_by_labour": 1 }))

			# Convert ObjectId to string for JSON serialization
			for labour in labours:
				if '_id' in labour:
					labour['_id'] = str(labour['_id'])

				# Determine who referred them, if any
				labour["referred_by"] = labour.get("referred_by_agent") or labour.get("referred_by_labour") or "N/A"

				# Clean up unused fields if needed
				labour.pop("referred_by_agent", None)
				labour.pop("referred_by_labour", None)

			print("fetched and passing babycaretaker labour details is :", labours)

			return JsonResponse({"labours": labours}, status=200)

		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON format"}, status=400)

		except Exception as e:
			return JsonResponse({"error": "Internal Server Error"}, status=500)

	return JsonResponse({"error": "Invalid request"}, status=400)



@api_view(["POST"])
def payment_update(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            print("Payment update received:", data)

            _id = data.get("_id")
            price = data.get("price")
            discount = data.get("discount")
            final_price = data.get("final_price")
            register_via = data.get("register_via")
            referred_by = data.get("referred_by")

            if not _id:
                return JsonResponse({"error": "Missing _id field"}, status=400)

            object_id = ObjectId(_id)

            # Step 1: Update the customer document
            update_result = Customer_info_col.update_one(
                {"_id": object_id},
                {
                    "$set": {
                        "price": price,
                        "discount": discount,
                        "final_price": final_price,
                        "register_via": register_via,
                        "referred_by": referred_by,
                        "payment_updated_at": datetime.now()
                    }
                }
            )

            if update_result.matched_count == 0:
                return JsonResponse({"error": "No record found with provided _id"}, status=404)

            # Step 2: Fetch the updated customer document
            customer_data = Customer_info_col.find_one({"_id": object_id})
            print("Updated Customer Info:", customer_data)
			
			# Convert ObjectId to string for JSON serialization
			# Fetching from the Subcription - user_data collection and updating with respect to the labour and then Agent or Labour
            customer_data["_id"] = str(customer_data["_id"])

            work_category = customer_data.get("work_category")
            labour_id = customer_data.get("fetched_labour_id")
            referred_by = customer_data.get("referred_by")
            register_via = customer_data.get("register_via")

            # Step 3: Identify correct labour collection
            labour_col = None
            if work_category == "Baby Caretaker":
                labour_col = EmpBabycaretaker_col
            elif work_category == "Elder Caretaker":
                labour_col = EmpElderCaretaker_col
            # Add more categories as needed
            else:
                return JsonResponse({"error": f"Unsupported work_category: {work_category}"}, status=400)

            # Step 4: Update the matched labour document
            labour_update = labour_col.update_one(
                {"labour_id": labour_id},
                {
					"$inc": {
						"transaction_credits_consumed": price,
						"user_credits_consumed": 1
					}}
            )

            if labour_update.matched_count == 0:
                return JsonResponse({"error": "No labour found with provided labour_id"}, status=404)

			# Step 5: Handle 'register_via' logic
            if register_via == "Via Agent":
                agent_update = agent_signup_col.update_one(
					{"agent_id": referred_by},
					{"$inc": {"user_credits_consumed" : 1, "transaction_credits_consumed": price}}
				)
                if agent_update.matched_count == 0:
                    print(f"Agent with ID {referred_by} not found in agent_db.")

            elif register_via == "Via Labour":
				 # Step 3: Identify correct labour collection
                labour_col = None
                if work_category == "Baby Caretaker":
                    labour_col = EmpBabycaretaker_col
                elif work_category == "Elder Caretaker":
                    labour_col = EmpElderCaretaker_col
				# Add more categories as needed
                else:
                    return JsonResponse({"error": f"Unsupported work_category: {work_category}"}, status=400)

                labour_ref_update = labour_col.update_one(
					{"labour_id": referred_by},
					{"$inc": {"user_credits_consumed" : 1, "transaction_credits_consumed": price}}
				)
                if labour_ref_update.matched_count == 0:
                    print(f"Labour with ID {referred_by} not found in labour_db.")

            elif register_via == "Direct":
                print("Direct registration — no referral update needed.")

            else:
                print(f"Unexpected register_via value: {register_via}")
				
            return JsonResponse({
                "message": "Payment details updated successfully and labour credits consumed updated",
                "customer": customer_data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            print("Error during payment update:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
	
#  Baby Care Taker Requirements Code

@api_view(['POST'])
def requirement_babycaretaker(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		sequence_id = ()

		caretaker_data = {
			"sequence_id" : uuid.uuid4().hex[:16].lower(),
			"order_id": generate_order_id(), 
			"order_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,
			"process_status_result" : "requested for labour requirement, waiting for process", # Update if have any status result
			"service_category" : "babycaretaker",
			"name": request.data.get("name"),
			"mobile_number": request.data.get("mobilenumber", 0),
			"alternative_mobile_number" : request.data.get("alternative_mobile_number", 0),
			"mail_id": request.data.get("email"),
			"address": request.data.get("address"),
			"pincode" : request.data.get("pincode"),
			"city": request.data.get("city"),
			"area": request.data.get("area"),

			"preferred_language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"child_age": int(request.data.get("age", 0)),
			"child_gender": request.data.get("gender"),
			"preferred_priority": request.data.get("urgencyStatus"),
			"preferred_care_timings" : request.data.get("preferredCareTime"),
			"preferred_duration": request.data.get("requiredDuration"),
			"preferredgender" : request.data.get("preferredGender"),

			"preferred_task": [item.strip() for item in request.data.get("baby_care_tasks", "").split(",")],  # Store as array
			"additional_note": request.data.get("additionalNotes"),
			"salary_offered": request.data.get("salaryOffered"),
			'agreedToTerms': request.data.get("agreedToTerms"),
		}

		# Insert into MongoDB
		result = req_babycaretaker_col.insert_one(caretaker_data)

		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def emp_baby_caretaker(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Generate sequence ID
		sequence_id = generate_sequence_id()

		# Handling File Uploads (Save to Local Storage)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		base_upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
		folder_path = os.path.join(base_upload_dir, sequence_id)
		os.makedirs(folder_path, exist_ok=True) 

		if photo:
			photo_name = f"{sequence_id}_{photo.name}"

			photo_path = os.path.join(folder_path, photo_name)
			default_storage.save(photo_path, ContentFile(photo.read()))

		if identity_card:
			identity_card_name = f"{sequence_id}_{identity_card.name}"

			identity_card_path = os.path.join(folder_path, identity_card_name)
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))

		# Generate labour ID
		labour_name = request.data.get("name", "").strip()
		mobile_number = request.data.get("mobilenumber", "0").strip()
		work_header = "BC"
		labour_id = generate_employee_id(labour_name, mobile_number , work_header)

		# Preparing Data for MongoDB
		emp_caretaker_data = {
			"labour_id": labour_id,
			"sequence_id" : sequence_id,
			"labour_name": request.data.get("name"),
			"mobile_number": int(request.data.get("mobilenumber", 0)),
			"mail_id": request.data.get("email"),
			"gender": request.data.get("gender"),
			"age": int(request.data.get("age", 0)),
			"address": request.data.get("address"),
			"photo_path": photo_path if photo else None,
			"id_card_path": identity_card_path if identity_card else None,
			"username": request.data.get("username"),
			"password": request.data.get("password"),
			"city": request.data.get("city"),
			"work_area": request.data.get("area"),
			"service_category" : "babycaretaker",
			"handling_work": [item.strip() for item in request.data.get("handling", "").split(",")],  # Store as array
			"availability": [item.strip() for item in request.data.get("availability", "").split(",")], 
			"language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"charge_per_hour": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("Experience"),
			"agreed_terms_conditions": request.data.get("agreedToTerms"),

			"register_via" : request.data.get("refer"),
			"referred_by_agent" : request.data.get("agentId"),
			"referred_by_labour" : request.data.get("labourId"),

			"work_specialization": request.data.get("workdescription"),
			"registered_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,  # after verification, 777 become 1
			"process_status_result" : "application applied, waiting for approval from company", # Update if have any status result
			"work_status" : 1,  # 1 means ready to work, 0 means not available
			"user_credits_consumed" : 0, # change the value as user fetch the mobile number
			"feedback_credits" : 0, # change the value whenever give stars to labour
			"labour_rewards": 0, # change the value whenever labour get credits more than 1000rs transaction

			"transaction_credits_consumed" : 0, # concept of 1000rs transaction
			"comp_transaction_credits_consumed" : 0,  # concept of 50 points from 1000 points
			"referred_transaction_credits_consumed" : 0, # concept of 
			"company_end_work_status" : 1, # If they crosses/high demand for this labour - make charge in future
			"company_end_work_status_reason" : "Still Not yet cross 1000 user_credit_consumed"

		}

		# Insert into MongoDB
		result = EmpBabycaretaker_col.insert_one(emp_caretaker_data)



		if result.inserted_id:

			referred_by = request.data.get("agentId", "").strip()
			# Extract last two letters for service code (e.g., 'L123BC' -> 'BC')
			service_code = referred_by[-2:] if len(referred_by) >= 2 else ""

			referred_by = request.data.get("agentId", "")
			
			if referred_by.startswith("AGT"):
				agent_signup_col.update_one(
					{"agent_id": referred_by},
					{"$inc": {"referred_transaction_credits_consumed": 10}}
				)
			elif referred_by.startswith("L") and service_code in EMPLOYEE_COLLECTION_MAP:
				# Referred by labour and valid service code
				collection = EMPLOYEE_COLLECTION_MAP[service_code]
				collection.update_one(
					{"labour_id": referred_by},
					{"$inc": {"referred_transaction_credits_consumed": 10}}
				)
				
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ------------------------------------------------------------------------------------- Elder Caretaker



@api_view(["POST"])
def search_eldercare(request):
	if request.method == "POST":
		try:
			# Decode JSON request
			data = json.loads(request.body.decode("utf-8"))
			print("request labour data for baby caretaker :", data)

			gender = data.get("gender")
			city = data.get("city")  # Get city
			area = data.get("area")  # Get area

			# Ensure required fields are present
			if not gender:
				return JsonResponse({"error": "Gender is required"}, status=400)
			if not city:
				return JsonResponse({"error": "City is required"}, status=400)
			if not area:
				return JsonResponse({"error": "Area is required"}, status=400)

			# MongoDB Query
			query = {
				"gender": gender,
				"city": city,
				"working_area": area
			}
			print("babycaretaker labour search query is :", query)

			# Fetch data from MongoDB
			labours = list(EmpBabycaretaker_col.find(query, {"full_name": 1, "gender": 1, "age": 1}))

			# Convert ObjectId to string for JSON serialization
			for labour in labours:
				if '_id' in labour:
					labour['_id'] = str(labour['_id'])

			print("fetched and passing babycaretaker labour details is :", labours)

			return JsonResponse({"labours": labours}, status=200)

		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON format"}, status=400)

		except Exception as e:
			return JsonResponse({"error": "Internal Server Error"}, status=500)

	return JsonResponse({"error": "Invalid request"}, status=400)


@api_view(['POST'])
def requirement_eldercaretaker(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		sequence_id = generate_sequence_id()

		# Preparing Data for MongoDB
		caretaker_data = {
			"sequence_id" : uuid.uuid4().hex[:16].lower(),
			"order_id": generate_order_id(), # Generate and print a unique 8-character word
			"order_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,
			"process_status_result" : "requested for labour requirement, waiting for process", # Update if have any status result
			"service_category" : "eldercaretaker",


			"user_name": request.data.get("name"),
			"mobile_number": request.data.get("mobilenumber", 0),
			"alternative_mobile_number" : request.data.get("alternative_mobile_number", 0),
			"mail_id": request.data.get("email"),
			"address": request.data.get("address"),
			"pincode" : request.data.get("pincode"),
			"city": request.data.get("city"),
			"area": request.data.get("area"),

			"preferred_language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"elder_age": int(request.data.get("age", 0)),
			"elder_gender": request.data.get("gender"),
			"preferred_priority": request.data.get("urgency"),
			"preferred_care_timings" : request.data.get("preferredCareTime"),
			"preferred_duration": request.data.get("duration"),

			"required_task": [item.strip() for item in request.data.get("elder_care_tasks", "").split(",")],  # Store as array
			"additional_note": request.data.get("additionalNotes"),
			"salary_offered": request.data.get("salaryOffered"),

		}

		# Insert into MongoDB
		result = req_elder_caretaker_col.insert_one(caretaker_data)
		
		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def emp_elder_caretaker(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Generate sequence ID
		sequence_id = generate_sequence_id()
	
		# Handling File Uploads (Save to Local Storage)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		# Define the base upload directory (make sure "media/uploads/" is defined in Django settings)
		# base_upload_dir = "media/uploads"
		# Define the base upload directory inside MEDIA_ROOT
		base_upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

		# Create a unique folder inside "uploads" using the sequence_id
		folder_path = os.path.join(base_upload_dir, sequence_id)
		os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

		if photo:
			photo_name = f"{sequence_id}_{photo.name}"
			photo_path = os.path.join(folder_path, photo_name)

			# Save file properly using Django's default_storage
			default_storage.save(photo_path, ContentFile(photo.read()))


		if identity_card:
			identity_card_name = f"{sequence_id}_{identity_card.name}"
			identity_card_path = os.path.join(folder_path, identity_card_name)
				# Save file properly
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))

			# default_storage.save(identity_card_path, ContentFile(identity_card.read()))

		# Generate labour ID
		labour_name = request.data.get("name", "").strip()
		mobile_number = request.data.get("mobilenumber", "0").strip()
		work_header = "EC"
		labour_id = generate_employee_id(labour_name, mobile_number , work_header)

		# Preparing Data for MongoDB
		emp_caretaker_data = {
			"labour_id": labour_id,
			"sequence_id" : sequence_id,
			"labour_name": request.data.get("name"),
			"mobile_number": int(request.data.get("mobilenumber", 0)),
			"mail_id": request.data.get("email"),
			"gender": request.data.get("gender"),
			"age": int(request.data.get("age", 0)),
			"address": request.data.get("address"),
			"photo_path": photo_path  if photo else None,
			"id_card_path": identity_card_path  if identity_card else None,
			"username": request.data.get("username"),
			"password": request.data.get("password"),
			"city": request.data.get("city"),
			"working_area": request.data.get("area"),
			"service_category" : "eldercaretaker",
			"handling_work": [item.strip() for item in request.data.get("handling", "").split(",")],  # Store as array
			"availability": [item.strip() for item in request.data.get("availability", "").split(",")], 
			"language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"charge_per_hour": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("experience"),
			"register_via" : request.data.get("refer"),
			"reference_id" : request.data.get("extraId"),
			"work_specialization": request.data.get("workdescription"),
			"registered_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,  # after verification, 777 become 1
			"process_status_result" : "application applied, waiting for approval", # Update if have any status result
			"work_status" : 1,  # 1 means ready to work, 0 means not available
			"user_credits_consumed" : 0, # change the value as user fetch the mobile number
			"feedback_credits" : 0, # change the value whenever give stars to labour

		}

		# Insert into MongoDB
		result = EmpElderCaretaker_col.insert_one(emp_caretaker_data)
		
		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#  --------------------------------------------------------------------------------------- Cleaner


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient


@api_view(['POST'])
def requirement_cleaner(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Handling File Uploads (Save to Local Storage)

		sequence_id = generate_sequence_id()

		# Preparing Data for MongoDB
		cleaner_data = {
			"sequence_id" :  uuid.uuid4().hex[:16].lower(),
			"order_id": generate_order_id(), # Generate and print a unique 8-character word
			"order_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,
			"process_status_result" : "requested for labour requirement, waiting for process", # Update if have any status result
			"service_category" : "housekeeping",

			"user_name": request.data.get("username"),
			"mobile_number": request.data.get("mobilenumber", 0),
			"alternative_mobile_number" : request.data.get("alternative_mobile_number", 0),
			"mail_id": request.data.get("email"),
			"address": request.data.get("address"),
			"pincode" : request.data.get("pincode"),

			"city": request.data.get("city"),
			"area": request.data.get("area"),
			"preferred_language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"preferred_gender": request.data.get("gender"),
			"preferred_priority": request.data.get("urgency"),
			"preferred_work_time": request.data.get("preferredworkTime"),
			"preferred_duration": request.data.get("duration"),

			"preferred_task": request.data.get("handling", "").split(",") ,# Handling multiple checkbox values
			"additional_note": request.data.get("additionalNotes"),
			"salary_offered": request.data.get("salaryOffered"),

		}

		# Insert into MongoDB
		result = req_cleaner_col.insert_one(cleaner_data)

		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def search_cleaner(request):
	if request.method == "POST":
		try:
			# Decode JSON request
			data = json.loads(request.body.decode("utf-8"))
			print("request labour data for baby caretaker :", data)

			gender = data.get("gender")
			careLocation = data.get("careLocation")  # Get city
			area = data.get("area")  # Get area

			# Ensure required fields are present
			if not gender:
				return JsonResponse({"error": "Gender is required"}, status=400)
			if not careLocation:
				return JsonResponse({"error": "City is required"}, status=400)
			if not area:
				return JsonResponse({"error": "Area is required"}, status=400)

			# MongoDB Query
			query = {
				"gender": gender,
				"city": careLocation,
				"working_area": area
			}
			print("Cleaner Labour Search Query is :", query)

			# Fetch data from MongoDB
			labours = list(EmpCleaner_col.find(query, {"full_name": 1, "gender": 1, "age": 1}))

			# Convert ObjectId to string for JSON serialization
			for labour in labours:
				if '_id' in labour:
					labour['_id'] = str(labour['_id'])

			print("fetched and passing babycaretaker labour details is :", labours)

			return JsonResponse({"labours": labours}, status=200)

		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON format"}, status=400)

		except Exception as e:
			return JsonResponse({"error": "Internal Server Error"}, status=500)

	return JsonResponse({"error": "Invalid request"}, status=400)


	
@api_view(['POST'])
def emp_cleaner(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Generate sequence ID
		sequence_id = generate_sequence_id()
		
		# Handling File Uploads (Save to Local Storage with Unique Filenames)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		# Define the base upload directory inside MEDIA_ROOT
		base_upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

		# Create a unique folder inside "uploads" using the sequence_id
		folder_path = os.path.join(base_upload_dir, sequence_id)
		os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

		if photo:
			photo_name = f"{sequence_id}_{photo.name}"
			photo_path = os.path.join(folder_path, photo_name)

			# Save file properly using Django's default_storage
			default_storage.save(photo_path, ContentFile(photo.read()))

		if identity_card:
			identity_card_name = f"{sequence_id}_{identity_card.name}"
			identity_card_path = os.path.join(folder_path, identity_card_name)
				# Save file properly
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))


		# Generate labour ID
		labour_name = request.data.get("name", "").strip()
		mobile_number = request.data.get("mobilenumber", "0").strip()
		work_header = "EC"
		labour_id = generate_employee_id(labour_name, mobile_number , work_header)

		# Preparing Data for MongoDB
		emp_caretaker_data = {
			"labour_id": labour_id,
			"sequence_id" : sequence_id,
			"labour_name": request.data.get("name", "").strip(),
			"mobile_number": request.data.get("mobilenumber", "").strip(),
			"mail_id": request.data.get("email", "").strip(),
			"gender": request.data.get("gender", "").strip(),
			"age": int(request.data.get("age", 0)),
			"address": request.data.get("address", "").strip(),
			"photo": photo_path  if photo else None ,
			"identity_card": identity_card_path if identity_card else None,
			
			"username": request.data.get("username"),
			"password": request.data.get("password"),
			"city": request.data.get("city"),
			"work_area": request.data.get("area"),
			"service_category" : "housekeeping",

			"handling_work": [item.strip() for item in request.data.get("handling", "").split(",")],  # Store as array


			"availability": [item.strip() for item in request.data.get("availability", "").split(",")], 
			"language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"charge_per_hour": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("experience"),
			"register_via" : request.data.get("refer"),
			"reference_id" : request.data.get("extraId"),
			"work_specialization": request.data.get("workdescription"),
			"registered_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,  # after verification, 777 become 1
			"process_status_result" : "application applied, waiting for approval", # Update if have any status result
			"work_status" : 1,  # 1 means ready to work, 0 means not available
			"user_credits_consumed" : 0, # change the value as user fetch the mobile number
			"feedback_credits" : 0, # change the value whenever give stars to labour

		}

		# Insert into MongoDB
		result = EmpCleaner_col.insert_one(emp_caretaker_data)

		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!', 'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#  ------------------------------------------------------------------------------------------ Cooking

@api_view(['POST'])
def requirement_cooking(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Handling File Uploads (Save to Local Storage)
		sequence_id = generate_sequence_id()

		# Preparing Data for MongoDB
		caretaker_data = {

			"sequence_id" :  uuid.uuid4().hex[:16].lower(),
			"order_id": generate_order_id(), # Generate and print a unique 8-character word
			"order_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,
			"process_status_result" : "requested for labour requirement, waiting for process", # Update if have any status result
			
			"user_name": request.data.get("username"),
			"mobile_number": request.data.get("mobilenumber", 0),
			"alternative_mobile_number" : request.data.get("alternative_mobile_number", 0),
			"mail_id": request.data.get("email"),
			"address": request.data.get("address"),
			"pincode" : request.data.get("pincode"),

			"city": request.data.get("city"),
			"area": request.data.get("area"),
			"preferred_language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"preferred_priority": request.data.get("urgency"),
			"preferred_duration": request.data.get("duration"),
			"preferred_cooking_time": request.data.get("preferredCookTime"),

			# Cooking Service Details (Split values correctly)
			"preferred_food_type": request.data.get("FoodType", "").split(",") if request.data.get("FoodType") else [],
			"preferred_meals_type": request.data.get("MealsType", "").split(",") if request.data.get("MealsType") else [],
			"preferred_cuisine_type": request.data.get("CuisineType", "").split(",") if request.data.get("CuisineType") else [],
			"preferred_dietary_restrictions": request.data.get("DietaryRestrictions", "").split(",") if request.data.get("DietaryRestrictions") else [],
		
			"additional_note": request.data.get("additionalNotes"),
			"salary_offered": request.data.get("salaryOffered"),
		}

		# Insert into MongoDB
		result = req_cooking_col.insert_one(caretaker_data)
		
		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def emp_cooking(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Generate sequence ID
		sequence_id = generate_sequence_id()

		# Handling File Uploads (Save to Local Storage)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		# Define the base upload directory inside MEDIA_ROOT
		base_upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")


		# Create a unique folder inside "uploads" using the sequence_id
		folder_path = os.path.join(base_upload_dir, sequence_id)
		os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

		if photo and photo != 'null':
			photo_name = f"{sequence_id}_{photo.name}"
			photo_path = os.path.join(folder_path, photo_name)
			default_storage.save(photo_path, ContentFile(photo.read()))

		if identity_card and identity_card != 'null':
			identity_card_name = f"{sequence_id}_{identity_card.name}"
			identity_card_path = os.path.join(folder_path, identity_card_name)
				# Save file properly
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))


		# Generate labour ID
		labour_name = request.data.get("name", "").strip()
		mobile_number = request.data.get("mobilenumber", "0").strip()
		work_header = "EC"
		labour_id = generate_employee_id(labour_name, mobile_number , work_header)

		# Preparing Data for MongoDB
		emp_caretaker_data = {
			"labour_id": labour_id,
			"sequence_id" : sequence_id,
			"labour_name": request.data.get("name"),
			"mobile_number": int(request.data.get("mobilenumber", 0)),
			"mail_id": request.data.get("email"),
			"address": request.data.get("address"),
			"gender": request.data.get("gender"),
			"age": int(request.data.get("age", 0)),
			"photo": photo_path if photo else None,
			"identity_card": identity_card_path  if identity_card else None,

			"username": request.data.get("username"),
			"password": request.data.get("password"),
			"city": request.data.get("city"),
			"work_area": request.data.get("area"),
			"service_category" : "eldercaretaker",

			"urgency": request.data.get("urgency"),
			"working_hours": request.data.get("workingHours"),
			"specific_requirement": request.data.get("specificRequirement"),
			"food_type": request.data.get("FoodType"),
			"meals_type": request.data.get("MealsType"),
			"cuisine_type": request.data.get("CuisineType"),
			"dietary_restrictions": request.data.get("DietaryRestrictions"),
			"cooking_style": request.data.get("CookingStyle"),
			"special_requirements": request.data.get("SpecialRequirements"),
			"service_type": request.data.get("ServiceType"),
			"kitchen_cleaning": request.data.get("KitchenCleaning"),
			"grocery_handling": request.data.get("GroceryHandling"),
			"additional_services": request.data.get("AdditionalServices"),
			"salary_offer": request.data.get("salaryOffer"),
			"specific_preferences_language": request.data.get("specificPreferencesLanguage"),
			"specific_requirements": request.data.get("specificRequirements"),
			"preferred_care_time": request.data.get("preferredCareTime"),


			"availability": [item.strip() for item in request.data.get("availability", "").split(",")], 
			"language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"charge_per_hour": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("experience"),
			"register_via" : request.data.get("refer"),
			"reference_id" : request.data.get("extraId"),
			"work_specialization": request.data.get("workdescription"),
			"registered_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,  # after verification, 777 become 1
			"process_status_result" : "application applied, waiting for approval", # Update if have any status result
			"work_status" : 1,  # 1 means ready to work, 0 means not available
			"user_credits_consumed" : 0, # change the value as user fetch the mobile number
			"feedback_credits" : 0, # change the value whenever give stars to labour

		}

		# Insert into MongoDB
		result = EmpCooking_col.insert_one(emp_caretaker_data)

		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def search_cook(request):
	if request.method == "POST":
		try:
			# Decode JSON request
			data = json.loads(request.body.decode("utf-8"))
			print("request labour data for baby caretaker :", data)

			gender = data.get("gender")
			careLocation = data.get("careLocation")  # Get city
			area = data.get("area")  # Get area

			# Ensure required fields are present
			if not gender:
				return JsonResponse({"error": "Gender is required"}, status=400)
			if not careLocation:
				return JsonResponse({"error": "City is required"}, status=400)
			if not area:
				return JsonResponse({"error": "Area is required"}, status=400)

			# MongoDB Query
			query = {
				"gender": gender,
				"care_location": careLocation,
				"area": area
			}
			print("Cleaner Labour Search Query is :", query)

			# Fetch data from MongoDB
			labours = list(EmpCooking_col.find(query, {"labour_name": 1, "gender": 1, "age": 1}))

			# Convert ObjectId to string for JSON serialization
			for labour in labours:
				if '_id' in labour:
					labour['_id'] = str(labour['_id'])

			print("fetched and passing babycaretaker labour details is :", labours)

			return JsonResponse({"labours": labours}, status=200)

		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON format"}, status=400)

		except Exception as e:
			return JsonResponse({"error": "Internal Server Error"}, status=500)

	return JsonResponse({"error": "Invalid request"}, status=400)


# ----------------------------------------------------------------------------- All Other Service


@api_view(['POST'])
def emp_otherservice(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Generate sequence ID
		sequence_id = generate_sequence_id()
		
		# Handling File Uploads (Save to Local Storage with Unique Filenames)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		# Define the base upload directory inside MEDIA_ROOT
		base_upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")

		# Create a unique folder inside "uploads" using the sequence_id
		folder_path = os.path.join(base_upload_dir, sequence_id)
		os.makedirs(folder_path, exist_ok=True)  # Ensure the folder exists

		if photo:
			photo_name = f"{sequence_id}_{photo.name}"
			photo_path = os.path.join(folder_path, photo_name)

			# Save file properly using Django's default_storage
			default_storage.save(photo_path, ContentFile(photo.read()))

		if identity_card:
			identity_card_name = f"{sequence_id}_{identity_card.name}"
			identity_card_path = os.path.join(folder_path, identity_card_name)
				# Save file properly
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))


		# Generate labour ID
		labour_name = request.data.get("name", "").strip()
		mobile_number = request.data.get("mobilenumber", "0").strip()
		work_header = "OS"
		labour_id = generate_employee_id(labour_name, mobile_number , work_header)

		# Preparing Data for MongoDB
		emp_data = {
			"labour_id": labour_id,
			"sequence_id" : sequence_id,
			"labour_name": request.data.get("name", "").strip(),
			"mobile_number": request.data.get("mobilenumber", "").strip(),
			"mail_id": request.data.get("email", "").strip(),
			"address": request.data.get("address", "").strip(),
			"gender": request.data.get("gender", "").strip(),
			"age": int(request.data.get("age", 0)),
			"photo": photo_path if photo else None,
			"identity_card": identity_card_path if identity_card else None,
			
			"username": request.data.get("username"),
			"password": request.data.get("password"),
			"city": request.data.get("city"),
			"work_area": request.data.get("area"),
			# "service_category" : "otherservice",
			"service_category": request.data.get("service", "").strip(),

			"availability": [item.strip() for item in request.data.get("availability", "").split(",")], 
			"language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"charge_per_hour": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("experience"),
			"register_via" : request.data.get("refer"),
			"reference_id" : request.data.get("extraId"),
			"work_specialization": request.data.get("workdescription"),
			"registered_datetime" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
			"process_status": 777,  # after verification, 777 become 1
			"process_status_result" : "application applied, waiting for approval", # Update if have any status result
			"work_status" : 1,  # 1 means ready to work, 0 means not available
			"user_credits_consumed" : 0, # change the value as user fetch the mobile number
			"feedback_credits" : 0, # change the value whenever give stars to labour

		}

		# Insert into MongoDB
		result = emp_otherservice_col.insert_one(emp_data)

		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!', 'id': str(result.inserted_id)}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
def search_otherservice(request):
	if request.method == "POST":
		try:
			# Decode JSON request
			data = json.loads(request.body.decode("utf-8"))
			print("request labour data for baby caretaker :", data)

			gender = data.get("gender")
			city = data.get("careLocation")  # Get city
			area = data.get("area")  # Get area

			service_category = data.get("service_category")

			# Ensure required fields are present
			if not gender:
				return JsonResponse({"error": "Gender is required"}, status=400)
			if not city:
				return JsonResponse({"error": "City is required"}, status=400)
			if not area:
				return JsonResponse({"error": "Area is required"}, status=400)

			# MongoDB Query
			query = {
				"gender": gender,
				"city": city,
				"working_area": area,
				"service_category": service_category
			}
			print("Cleaner Labour Search Query is :", query)

			# Fetch data from MongoDB
			labours = list(emp_otherservice_col.find(query, {"labour_name": 1, "gender": 1, "age": 1}))

			# Convert ObjectId to string for JSON serialization
			for labour in labours:
				if '_id' in labour:
					labour['_id'] = str(labour['_id'])

			print("fetched and passing babycaretaker labour details is :", labours)

			return JsonResponse({"labours": labours}, status=200)

		except json.JSONDecodeError:
			return JsonResponse({"error": "Invalid JSON format"}, status=400)

		except Exception as e:
			return JsonResponse({"error": "Internal Server Error"}, status=500)

	return JsonResponse({"error": "Invalid request"}, status=400)



# ------------------------------------------------------------------------------ All Other Services

@api_view(['POST'])
def Tankcleaner(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Handling File Uploads (Save to Local Storage)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		if photo:
			photo_path = f"uploads/photos/{photo.name}"
			default_storage.save(photo_path, ContentFile(photo.read()))

		if identity_card:
			identity_card_path = f"uploads/identity_cards/{identity_card.name}"
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))

		# Preparing Data for MongoDB
		caretaker_data = {
			"full_name": request.data.get("username"),
			"age": int(request.data.get("age", 0)),
			"email": request.data.get("email"),
			"address": request.data.get("address"),
			"photo": photo_path,
			"identity_card": identity_card_path,
			"child_name": request.data.get("childname"),
			"child_age": int(request.data.get("childage", 0) or 0), 
			"child_gender": request.data.get("childgender"),
			"child_health_issues": request.data.get("childhealth"),
			"urgency": request.data.get("urgency"),
			"preferred_care_time": request.data.get("preferredCareTime"),
			"duration": request.data.get("duration"),
			"care_location": request.data.get("careLocation"),
			"specific_preferences_language": request.data.get("specificPreferencesLanguage"),
			"specific_requirements": request.data.get("specificRequirements"),
			"salary_offer": request.data.get("salaryOffer"),
			"process_status" : 777
		}

		# Insert into MongoDB
		result = req_tank_cleaner_col.insert_one(caretaker_data)
		
		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def Driver(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Handling File Uploads (Save to Local Storage)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		if photo:
			photo_path = f"uploads/photos/{photo.name}"
			default_storage.save(photo_path, ContentFile(photo.read()))

		if identity_card:
			identity_card_path = f"uploads/identity_cards/{identity_card.name}"
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))

		# Preparing Data for MongoDB
		caretaker_data = {
			"full_name": request.data.get("username"),
			"age": int(request.data.get("age", 0)),
			"email": request.data.get("email"),
			"address": request.data.get("address"),
			"photo": photo_path,
			"identity_card": identity_card_path,
			"child_name": request.data.get("childname"),
			"child_age": int(request.data.get("childage", 0) or 0), 
			"child_gender": request.data.get("childgender"),
			"child_health_issues": request.data.get("childhealth"),
			"urgency": request.data.get("urgency"),
			"preferred_care_time": request.data.get("preferredCareTime"),
			"duration": request.data.get("duration"),
			"care_location": request.data.get("careLocation"),
			"specific_preferences_language": request.data.get("specificPreferencesLanguage"),
			"specific_requirements": request.data.get("specificRequirements"),
			"salary_offer": request.data.get("salaryOffer"),
			"process_status" : 777
		}

		# Insert into MongoDB
		result = req_driver_col.insert_one(caretaker_data)
		
		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def EmpTankcleaner(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Handling File Uploads (Save to Local Storage)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		if photo:
			photo_path = f"uploads/photos/{photo.name}"
			default_storage.save(photo_path, ContentFile(photo.read()))

		if identity_card:
			identity_card_path = f"uploads/identity_cards/{identity_card.name}"
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))

		# Preparing Data for MongoDB
		emp_caretaker_data = {
			"full_name": request.data.get("username"),
			"age": int(request.data.get("age", 0)),
			"email": request.data.get("email"),
			"address": request.data.get("address"),
			"photo": photo_path,
			"identity_card": identity_card_path,
			"gender": request.data.get("urgency"),
			"duration": request.data.get("duration"),
			"city": request.data.get("careLocation"),
			"working_area": request.data.get("area"),
			"availability": request.data.get("availability"),
			"language": request.data.get("specificPreferencesLanguage"),
			"hourly_rate": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("experience"),
			"specific_requirements": request.data.get("specificRequirements"),
			"process_status": 777
		}

		# Insert into MongoDB
		result = EmpTankcleaner_col.insert_one(emp_caretaker_data)
		
		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def EmpDriver(request):
	if request.method == 'POST':
		print("Request data is:", request.data)

		# Handling File Uploads (Save to Local Storage)
		photo = request.FILES.get("photo")
		identity_card = request.FILES.get("identityCard")

		photo_path = None
		identity_card_path = None

		if photo:
			photo_path = f"uploads/photos/{photo.name}"
			default_storage.save(photo_path, ContentFile(photo.read()))

		if identity_card:
			identity_card_path = f"uploads/identity_cards/{identity_card.name}"
			default_storage.save(identity_card_path, ContentFile(identity_card.read()))

		# Preparing Data for MongoDB
		emp_caretaker_data = {
			"full_name": request.data.get("username"),
			"age": int(request.data.get("age", 0)),
			"email": request.data.get("email"),
			"address": request.data.get("address"),
			"photo": photo_path,
			"identity_card": identity_card_path,
			"gender": request.data.get("urgency"),
			"duration": request.data.get("duration"),
			"city": request.data.get("careLocation"),
			"working_area": request.data.get("area"),
			"availability": request.data.get("availability"),
			"language": request.data.get("specificPreferencesLanguage"),
			"hourly_rate": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("experience"),
			"specific_requirements": request.data.get("specificRequirements"),
			"process_status": 777
		}

		# Insert into MongoDB
		result = EmpDriver_col.insert_one(emp_caretaker_data)
		
		if result.inserted_id:
			return Response({'message': 'Form submitted successfully!'}, status=status.HTTP_201_CREATED)
		else:
			return Response({'message': 'Error saving to MongoDB'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedPhoto
from .serializers import UploadedPhotoSerializer

@api_view(['POST'])
def upload_photo(request):
	if 'photo' not in request.FILES:
		return Response({'error': 'No photo uploaded'}, status=status.HTTP_400_BAD_REQUEST)
	
	photo = request.FILES['photo']
	uploaded_photo = UploadedPhoto(photo=photo)
	uploaded_photo.save()
	
	return Response({'message': 'Photo uploaded successfully!'}, status=status.HTTP_201_CREATED)
