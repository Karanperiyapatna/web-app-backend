

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
			"work_area": request.data.get("area"),
			"service_category" : "eldercaretaker",
			
			"handling_work": [item.strip() for item in request.data.get("handling", "").split(",")],  # Store as array
			
            
			"availability": [item.strip() for item in request.data.get("availability", "").split(",")], 
			"language": [lang.strip() for lang in request.data.get("language", "").split(",")],  # Store languages as array
			"charge_per_hour": int(request.data.get("hourlyRate", 0)),
			"experience": request.data.get("experience"),
			"register_via" : request.data.get("refer"),
			"refer_id" : request.data.get("extraId"),
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

