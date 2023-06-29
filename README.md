# booking API
Django rest API for a booking system.

This is an SPI built using the Django REST framework and meant to be used as back-end for the Platinum web application.

[See deployed api](https://platinum-booking-api.herokuapp.com/)

[See the front end repository](https://github.com/EliSacch/platinum)

[See the deployed app](https://platinum.herokuapp.com/)

## Table of content

- [Project Planning](#project-planning)

- [Features](#features)
  - [Appointmments](#appointments)
  - [Treatments](#treatments)
  - [Profile](#profile)

- [Testing](#testing)

- [Deployment](#deployment)
  - [Live Website](#live-website)
  - [Local Deployment](#local-deployment)

- [Credits](#credits)
  - [Code](#code)
  - [Content](#content)

- [Technologies used](#technologies-used)

- [Acknowledgements](#acknowledgements)

## Project Planning

The web app was developed following the Agile methodology, utilizing the project functionality provided by GitHub
[Link to the project board](https://github.com/users/EliSacch/projects/6/)


[Back to the top](#table-of-content)

### Database Models

These are the models created for this project: User, Profile, Appointment, Treatment

- User:
The User model is provided by Django Allauth package.

The following Models are custom:

- Profile:
This custom model is linked to the User model. It is used to store the user profile information.

| Field name | Type | Notes |
|------------|------|-------|
| Owner | OneToOne field (User) | Instances can be added or removed only when we add or remove a User |
| Name | Charfield | Optional |
| Notes | Textfield | Optional |
| Image | ImageField | Provides a default image if left blank |
| Created_at | Datetimefield | Automatically set |
| Updated_at | Datetimefield | Authomatically set |


- Appointment:
It is a model that stores the appointment information. It is linked to the User model, so that each user can access his/her appointments information.

| Field name | Type | Notes |
|------------|------|-------|
| Owner | ForeignKey (User) | Appointments are deleted when the ForeignKey is deleted |
| Client_name | Charfield | Optional |
| Treatment | ForeignKey (Treatment) | The on_delete attribute is set to "Protect" because we want to preserve them |
| Date | DateField | |
| Time | IntegerField | The values can be selected from a preset list of options and they represent the appointment start time |
| End_time | IntegerField | The value is calculated automatically based on the time and treatment selected |
| Notes | TextField | Optional |
| Created_at | Datetimefield | Automatically set |
| Updated_at | Datetimefield | Authomatically set |


- Treatment:
To easily manage the services that can be booked, the staff memebers can create and manage them via the Treatment model.

| Field name | Type | Notes |
|------------|------|-------|
| Title | Charfield | Must be unique |
| Description | Textfield | Optional |
| Price | FloatField | |
| Duration | Integer Field | |
| Image | Imagefield | A default image is provided |
| Is_active | BooleanField | This field is meant to hide treatments that would have been cancelled, but that cannot be deleted because already related to one or more appointments |
| Created_at | Datetimefield | Automatically set |
| Updated_at | Datetimefield | Authomatically set |


![Model relationship diagram](media/models_relationships_diagram.png)

[Back to the top](#table-of-content)

__________

## Features 

### Appointments

Each user can create a new appointment for themselves. Users with a "Staff" role, can create an appointment for any user.

- __Serializers__

There are three serializers:
- BaseAppointmentSerializer: which creates the base for the other two.
This Base serializer contains the basic validation that it is then extended to the other two serializers.

The main validation checks to be performed when creating or editing an appointment are relatd to the date and time of the appointment, so that we can avoid: Overlapping appointments, appointments for a past date, (or too much in the future) and appointments in unavaiable days or time slots.

In particular, to avoid overlapping appointments we need the selected start time, and we need to retrieve the duration associated to the selected treatment:

Being able to perform this calculation is the main reason why I choose IntegerField as type for the time and duration.

- ClientAppointmentSerializer: It is the client side serilizer. Because clients can make appointment only for themselves, they owner is a Read only field, and they cannot add a client name (their username will be used instead). Clients also cannot make same day appointments, while staff members can, as long as they are at least 20 minutes in the future.

- StaffAppointmentSerializer: Staff members can select an existing user as owner, or theu can leave the owner field blank if they want to make an appointment for unregistered clients. In this case although they must enter a cient name.


- __Views__

- AppointmentList: This is the staff facing list/create view. It can be accessed from authenticated users who also have the is_staff value set to true (staff members). It shows all the appointments.

- MyAppointmentList: This is the client facing list/create view. It shows only the appointments belonging to the current user, for this reason the permissions are set as follow:

      permission_classes = [ permissions.IsAuthenticated, IsOwner]

- AppointmentDetail: This is the client facing detail/update/destroy view. Each user can access and manage only information related to his/her own appointments, for this reason the permissions are set as follow:

      permission_classes = [ permissions.IsAuthenticated, IsOwner]


- ClientAppointmentDetail: this is the staff facing detail/update/destroy view. Staff members can access and manafe all appointments, even if they are not the owner.

[Back to the top](#table-of-content)

### Treatments

- __Serializers__

There are two serializers for the Treatment model:

- TreatmentSerializer: this is the staff facing serializer,because it allows staff members to access information such as the creation and update time.

Here we also set the duration choices for the treatments. For a better user experience we don't want to allow any possible integer to be added as value, but we want to provide a reasonable amount of choices that reflect what the real business would offer. We also set the choice label to be a human friendly format, that shows the value as a time value instad of an integer.

- ClientFacingTreatmentSerializer: This is the client facing serializer, which does not have any validation since the only allowed method is read only. Clients cannot add or edit any information.


- __views__

- TreatmentList: This is the list/create view. Only staff members can create a treatment, this is why the permissions are set as follow:

    permission_classes = [ permissions.IsAuthenticatedOrReadOnly, IsStaffMemberOrReadOnly ]


- TreatmentDetail: this is the retrieve/update/destroy view for treatments. clients can acess only safe methods (Read only), while staff members can update or delete treatments.

In this view we override the destroy method, because we want to pass a custom message to inform the user in case they try to delete a treatment that was altready booked. Because this is not allowerd, so they are informed to set it as inactive.


### Profiles

When a user is registered, the user profile is automatically created.


- __Serializers__

We have three serializers; two of them related to the Profile model, while one is related to the User model, and it will be explained below.

- ProfileSerializer: This is the client facing serializer. Clients can access their profile image, which is not available to staff members.

- ClientSerializer: This is the staff facing serializer. It gives acces to two annotated field, to check the total count of appointments associated to a user, and if a user has any appointments for the current day.

It also gives access to the notes fields, so that staff members can store some client information, such as special products used.

- UserSerializer: This serializer gives access to the username and is_staff field of the User model. This serializer is used to allow staff members to change the role of other users, and give them the ability to acess the staff dashboard.

- __Views__

- ProfileList: This is a list only view for staff members. The creation is hnadled by the __post_save__ signal that reads when a user is created.

- ProfileDetail: This is the client facing profile list view. For this reason is uses the Profile serializer, so that it doesn't allow access to the profile notes, or appointment count.

- ClientProfileDetail: This is the retrieve/update view for staff members. It does not give access to the destroy method, because profiles are deleted when a user is deleted.

- SetIsStaff: This View can be accessed by staff members only, and it is needed to access the is_staff column of the User model. 

### Search, filter and ordering.

The search functionality is added to the following views:

- AppointmentList: Staff member can search for appointments by owner or client name.

- TreatmentList: Treatments can be searched by title.

- ProfileList: Users can be filtered by name or username.

The filter functionality is added to the following views:

- AppointmentList: Staff member can filter all appointments for a specific date.

- ProfileList: can also be ordered based on the appointments count.

__________

## Testing 

Check testing [here](testing.md)

______________

## Deployment

### Live website

To deply this project on Heroku I followed these steps:
  1. Access my Heroku account (or create one)
  2. Click on Add App
  3. Go to Settings > Config Vars
  4. Add the config KEY and VALUE from my env.py file
  5. Go to deploy tab
  6. Select GitHub as deploy method
  7. Select the relevant GitHub repository
  8. Click on deploy branch

### Local Deployment

For a local deployment follow these steps:
  - Create a new directory on your machine, where you want do deploy the files
  - Open the existing repository in GitHub
  - Go to the "Code" tab
  - Click on the "Code" button
  - Copy the HTTPS link
  - Open your terminal and run the command __git clone 'link'__
  - use the link just copied, without quotes, instead of 'link'

[Back to the top](#table-of-content)

_____________

## Credits 

### Code

- The code to check if a range of numbers overlap with another range of numbers (to check for overlapping appointments) is taken from [Stackoverflow](https://stackoverflow.com/questions/6821156/how-to-find-range-overlap-in-python)

- The code to get the date corresponding to six months from today is taken from [Stackoverflow](https://stackoverflow.com/questions/546321/how-do-i-calculate-the-date-six-months-from-the-current-date-using-the-datetime)

- The code to dispaly a foreignkey field name/title instead of the id (in serializer) is taken from [Stackoverflow](https://stackoverflow.com/questions/52491330/how-to-get-foreignkey-field-name-instead-of-id-in-django-rest-framework)

- The code to display an error message for ProtectedError instad of the Django 500 error page is taken from [Stackoverflow](https://stackoverflow.com/questions/44229783/catch-protected-error-and-show-its-message-to-the-user-instead-of-bare-500-code)


### Content

- The models relationship diagram was drawn using [Lucidchart](https://www.lucidchart.com/pages/)
- The default service picture is from Luis Quintero on [Unsplash](https://unsplash.com/es/@jibarox?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
  

[Back to the top](#table-of-content)

_____________

## Technologies used

Languages used:
  - Python

Frameworks and applications:
  - Django
  - Django-cloudinary-storage - To connect our Django project to Cloudinary
  - Pillow - To add image processing capabilities to our project
  - Django-allauth - for user authentication
  - Django-cors-headers - to allow in-browser requests to the Django api from other applications.
  - Django REST framework - To build the web API
  - Simplejwt - to use django web tokens

Database and storage:
  - PostgreSQL - Relational database system
  - Psycopg2 - PostgreSQL database adapter for the Python programming language
  - ElephantSQL - Host for the databased used by the live website
  - Cloudinary - To store the images and static files
  
[Back to the top](#table-of-content)

## Acknowledgements

A special thank to my mentor __Dick Vlaanderen__ for his precious feedback on this project.
