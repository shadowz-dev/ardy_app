ardy-app is a Project where:

- There are multiple users types(Customer,Interior Designers, Consultants, Construction, Smart Home...etc).
- Each user type other than customer can have multiple sub-users for employees.
- Users can register and apply with additional required details for customer type.
- Customer users are uploading and adding their land detailes to get quotation from other users types.
- Customer will choose a consultant to start.
- all user types other than customer can be suggested to the customer while choosing.
- Consultant user will receive a notification and prepare initial quotation for the customer.
- Once quotation approved from customer consultant will prepare required drawings and submit it for customer revisions.
- Chat option between each customer and other user types shall be available as p2p communication.
- once finished customer can select the constcution company for the next step and so on.


__________________________________________________________________________________________________

created core model including
- Custom User model with Custom types
- knox and allauth for django and permissions for handling.
- urls for the app.



__________________________________________________________________________________________________

Remaining to be added 

3. Land Details and Project Module
Models:
Define LandDetail and Project models.
Link Project to CustomerProfile and add fields to track the current project phase.
Forms and Serializers:
Set up serializers for LandDetail and Project.
Views:
Implement views to allow customers to create and view their projects.
Use Django REST Framework’s generic views for basic CRUD operations.
Permissions:
Restrict view access so only customers can create projects, and others can only view or act based on their role.
4. Quotation Management Module
Models:
Define a Quotation model linked to Project and the Consultant.
Track fields like status (pending, approved, rejected).
Serializers and Views:
Create serializers and views for Quotation creation and approval.
Notifications:
Integrate Django signals to notify customers when a new quotation is available.
Permissions:
Set up view permissions for consultants to create/update quotations and for customers to approve/reject them.
5. Drawing and Document Management Module
Models:
Create a Drawing model linked to Project to store uploaded files.
Add a Revision model to track customer revision requests.
Views:
Implement views to allow consultants to upload drawings and customers to submit revision requests.
Permissions:
Restrict access to allow consultants to upload and customers to request revisions.
6. p2p Communication Module (Chat)
Models:
Define ChatRoom and Message models for handling p2p communication between users.
Views:
Use Django Channels for real-time messaging.
Set up WebSocket consumers to handle live communication.
Permissions:
Enforce p2p restrictions to allow customers to communicate only with one user type at a time.
Example of a WebSocket consumer:

python
Copy code
from channels.generic.websocket import WebsocketConsumer
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        # Handle message data and send response back to users
7. Project Phase Management Module
Models:
Add a Phase model to track the current project stage.
Views:
Implement endpoints for customers to transition project phases and select new user types.
Notifications:
Set up notifications when phases change, using signals to inform relevant users.
Permissions:
Phase-based access control to limit access to each stage’s relevant users.
8. Notifications and Activity Log Module
Models:
Define Notification and ActivityLog models.
Views:
Create views to retrieve notifications and logs.
Permissions:
Ensure users can only see notifications related to their projects.
9. Admin Module
Django Admin Customizations:
Customize Django admin to manage all app data, monitor user activity, and handle support.
Use django-admin to create views for managing user profiles, projects, and project phases.