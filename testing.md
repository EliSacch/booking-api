# Testing

Back to [main README](readme.md)

## Table of content

[Manual testing](#manual-test)

[Validator Testing](#validator-testing)

[Fixed bugs](#fixed-bugs)

[Unfixed bugs](#unfixed-bugs)


## Manual test

<details>
<summary>Unauthenticated users</summary>


| Action | Expected result | Pass/Fail |
|--------|-----------------|-----------|
| Open the link in the browser | The welcome message is displayed | Pass |
| Access the "/treatments/" url  | The treatments are fetched | Pass |
| Access the "/treatments/1" url | The treatment #1 is active, so we can retrieve the details | Pass |
| Go to "/treatments/999" | The treatment doesn't exist, so the api return error 404 | Pass |
| Go to "/appointments/" | The api returns error 403 because we are not authenticated | Pass |
| Go to "/my-appointmnets/" | The api returns error 403 because we are not authenticated | Pass |
| Go to "/profiles/1! | The api returns error 403 because we are not authenticated | Pass |
| Go to "/clients/" | The api returns error 403 because we are not authenticated | Pass |
| Go to set-staff-permission | The api returns error 403 because we are not authenticated | Pass |

</details>


<details>
<summary>Logged in as a client</summary>


| Action | Expected result | Pass/Fail |
|--------|-----------------|-----------|
|  Go to "/my-appointments/" | The api returns the appointments whose owner is the logged in user | Pass |
| Go to "/my-appointments/3" | Because this appointment belongs to the current user, I can access the appointment details | Pass |
| Go to "/my-appointments/1" | The api returns error 403 because this appointment doesn't belong to us, and we are not authorized to view other client's appointments | Pass |
| go to "/my-appointments/999" | The api returns error 404 | Pass |
| Go to "/appointmnets/" | Because the logged in user is a client, the api return error 403 - forbidden" | Pass |
| Go to "/clients/" | Because the logged in user is a client, the api return error 403 - forbidden" | Pass |
| Go to "/profiles/1/" | Because this profile belongs to another user, the api return error 403 - forbidden" | Pass |
| Go to "/profiles/2/" | Because this profile belongs to the logged in user, the api return the profile information | Pass |
| Try and edit the Name | The name is updated | Pass |
| Try and upload an image bigged than 2MB | The api returns an error message, stating that the image is too big | Pass |
| Try and upload a valid image |The image is uploaded to cloudinary | Pass |

</details>


<details>
<summary>Manage appointment - logged in as a client</summary>


| Action | Expected result | Pass/Fail |
|--------|-----------------|-----------|
| Go to "/my-appointments/" and send a post request without selecting any data | The api gives an error since we need to choose a date, while Time and Treatment are assigned automatically a default value | Pass |
| Send a post request this time selecting a date in the past | The api returns an error to let us know that we cannot book that date | Pass |
| Send a request for the next Monday | The api returns an error to let us know that we cannot book on Sundays or Mondays | Pass |
| Send a request for today | The api returns an error to let us know that we cannot book for today | Pass |
| Select a valid date | The request is submittedd successfully and we can access this appoinment information | Pass |
| Try and send a request for the same date and time | The api returns an error sating that there is already an appointment | Pass |
| Try and make an appointment for half an hour before but select a treatment that lasts more than half an hour | We are informed that the date/time selected are not available. | Pass |
| Fetch the newly created appointment and send a put request, but change de date to an invalid one  | The api returns error 400 with a message | Pass |
| Send a new request with valid data | The request is acepted and the api returns the new data for ths appointment | 


</details>


<details>
<summary>Logged in as a</summary>


| Action | Expected result | Pass/Fail |
|--------|-----------------|-----------|
| Go to "/appointments/" | The api returns all the appointments | Pass |
| go to "/appointments/2" | Even if this appointment doesn't belong to the user, the api returns the information since the user is a staff member | Pass |
| Go to "/clients/" | the api returns the list of all clients | Pass |
| Go to "/clients/2" | Even if this is not the current user's profile the api returns the profile information, because the user is a  staff member | Pass | 
|  Send a put request with some notes | The request goes through and the newly added notes are returned for this user's profile | Pass |
| Go to treatments | All the treatments are returned | Pass |
| Send a post request with an empty title | The api returns an error message for the title field that cannot be blank | Pass | 
| Send a post request with a title that already exists | The api returns a message stating that a treatment with this title already exists | Pass |
| Send a post request with a valid title | The treatment is created | Pass |
| Go to "/treatments/1/" | The api returns the treatment information | Pass |
| Send a put request with invalid information | The new information is validated again and the api returns an error for each invalid field | Pass |
|Send a put request with valid data | The request goes through and the new information are fetched with this treatment | Pass | 


</details>


<details>
<summary>Manage appointment - logged in as a staff member</summary>


| Action | Expected result | Pass/Fail |
|--------|-----------------|-----------|
| Go to "/appointments/" and send a post request without selecting any data | The api gives an error for the date, and an error for the client_name since we need to choose a date, and we need to enter a name if we don't select a user | Pass |
| Send a post request this time selecting a date in the past | The api returns an error to let us know that we cannot book that date | Pass |
| Send a request for the next Monday | The api returns an error to let us know that we cannot book on Sundays or Mondays | Pass |
| Send a request for today, but a time in the past | The api returns an error to let us know that we cannot book for the past | Pass |
| Send a request for today, but a time at least 30minutes away from now | The request is successful | Pass |
| Select a valid date but no owner or client_name | The returns an error stating that we need to enter  aname for unregistered users | Pass |
| Select a valid date and owner or client_name | The request is submittedd successfully and we can access this appoinment information | Pass |
| Try and send a request for the same date and time | The api returns an error sating that there is already an appointment | Pass |
| Try and make an appointment for half an hour before but select a treatment that lasts more than half an hour | We are informed that the date/time selected are not available. | Pass |
| Fetch the newly created appointment and send a put request, but change de date to an invalid one  | The api returns error 400 with a message | Pass |
| Send a new request with valid data | The request is acepted and the api returns the new data for ths appointment | 


</details>


[Back to the top](#table-of-content)


## Validator Testing


The final version of python files was checked using [CI Python Linter](https://pep8ci.herokuapp.com/#)

Se screenshots below:

<details>
  <summary>Appointments</summary>

  | File | Result |
  | -----| ------ |
  | [admin.py](media/testing/validation/appoint-admin.png) | clean code |
  | [filters.py](media/testing/validation/appoint-filters.png) | clean code |
  | [models.py](media/testing/validation/appoint-models.png) | clean code |
  | [serializers.py](media/testing/validation/appoint-serializers.png) | clean code |
  | [test.py](media/testing/validation/appoint-tests.png) | clean code |
  | [urls.py](media/testing/validation/appoint-urls.png) | clean code |
  | [views.py](media/testing/validation/appoint-views.png) | clean code |

</details>

<details>
  <summary>Booking api</summary>

  | File | Result |
  | -----| ------ |
  | [permissions.py](media/testing/validation/booking-permissions.png) | clean code |
  | [serializers.py](media/testing/validation/booking-serializers.png) | clean code |
  | [urls.py](media/testing/validation/booking-urls.png) | clean code |
  | [views.py](media/testing/validation/booking-views.png) | clean code |

</details>


<details>
  <summary>Profiles</summary>

  | File | Result |
  | -----| ------ |
  | [admin.py](media/testing/validation/profiles-admin.png) | clean code |
  | [models.py](media/testing/validation/profiles-models.png) | clean code |
  | [serializers.py](media/testing/validation/profiles-serializers.png) | clean code |
  | [urls.py](media/testing/validation/profiles-urls.png) | clean code |
  | [views.py](media/testing/validation/profiles-views.png) | clean code |

</details>

<details>
  <summary>Treatments</summary>

  | File | Result |
  | -----| ------ |
  | [admin.py](media/testing/validation/treatment-admin.png) | clean code |
  | [models.py](media/testing/validation/treatment-model.png) | clean code |
  | [serializers.py](media/testing/validation/treatment-serializers.png) | clean code |
  | [urls.py](media/testing/validation/treatment-urls.png) | clean code |
  | [views.py](media/testing/validation/treatment-views.png) | clean code |

</details>


[Back to the top](#table-of-content)

## Fixed Bugs

<details>
  <summary> Custom IsStaffMember permission not working on generics.ListAPIView:</summary>

  - Issue: 
  
    The ProfileList view should be accessed by staff members only. This is because only staff members can see all the profiles, while each client cannot see the other clients (each client can only access their own profile).
    
    This was working only in the ClientProfileDetail view (RetrieveUpdateAPIView), but not in the ProfileList (ListAPIView)

![Original code](media/bugs/isstaff_permission_bug.png)

As we can see the user 'admin' has the attribute isStaff set to 'false':

![isStaff attribute for admin](media/bugs/isstaff_permission_bug_1.png)

But they can access the ProfileList:

![Profile list accessed by admin](media/bugs/isstaff_permission_bug_2.png)

While they cannot access the client profile, as expected, since the user 'admin' is not part of the staff, so they should not be able to see the client profiles:

![clientProfileDeatail cannot be accessed by admin](media/bugs/isstaff_permission_bug_3.png)


  - Fix:

  After throubleshooting I could identify that the issue is caused by the use of ListAPIView.

  As we see from the Django REST framework documentation: https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions

  We can create a custom permission by overriding the BasePermission. Although we have 2 methos to do so:

  has_permission (global) and has_object_permission (object-level)

  The IsStaffMember was initially overriding just the has_object_permission, which is used at object level views, such as the RetrieveUpdateAPIView. While the ListApiView checks for global permissions.

  To fix this issue I had to override the has_permission method as well:
  ![Final code](media/bugs/isstaff_permission_fix.png)

  After this fix, our user 'admin' cannot access the clients list anymore:
  ![Original code](media/bugs/isstaff_permission_fix_1.png)
  

</details>


<details>
  <summary>Deployed site giving error 400 Bad Request</summary>

  - Issue: When trying to acess the deployed app, I was receiving erro 400 bad request.

  - Fix: After turning on debug mode I could see that heroku was not in "ALLOWED_HOSTS". Even though I added it when I first deployed the project, I must have removed it by accident. After adding it again the error was fixed.

</details>

 
## Unfixed Bugs

There are currently 0 known unfixed bugs

[Back to the top](#table-of-content)

________

Back to [main README](readme.md)