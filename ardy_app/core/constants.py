# core/constants.py

USER_TYPES = [('Customer', 'Customer'), ('Consultant', 'Consultant'),
            ('Interior Designer', 'Interior Designer'), ('Construction', 'Construction'),
            ('Maintenance', 'Maintenance'),('Smart_Home', 'Smart_Home'), ('Admin', 'Admin'),]

SIGNUP_TYPE = [
    ("Manual", "Manual"),
    ("Google", "Google"),
    ("Apple", "Apple"),
]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    ('Rejected', 'Rejected'),
]

STATUS_PENDING = 'Pending'
STATUS_ACCEPTED = 'Accepted'
STATUS_IN_PROGRESS = 'In Progress'
STATUS_COMPLETED = 'Completed'
STATUS_CANCELLED = 'Cancelled'
STATUS_REJECTED = 'Rejected' # Added

BUILDING_CHOICES = [
    ('G+0', 'G+0'),
    ('G+1', 'G+1'),
    ('G+2', 'G+2'),
    ('G+3', 'G+3'),
    ('G+4', 'G+4'),
    ('G+5', 'G+5'),
    ('G+6', 'G+6'),
    ('G+7', 'G+7'),
    ('G+8', 'G+8'),
    ('Tower', 'Tower'),
]

UserOTP=[
    ('signup', 'Signup'),
    ('reset_password', 'Reset Password'),
    ('phone_verification', 'Phone Verification'),
]

SERVICE_PROVIDER_USER_TYPES_REQUIRING_APPROVAL = [
    'Consultant', 'Interior Designer', 'Construction', 'Maintenance', 'Smart_Home' # Match values from USER_TYPES
]

PAYMENT_CLAIM_STATUS_CHOICES = [
    ('PendingReview','Pending Review'),
    ('ApprovedByCustomer', 'Approved By Customer'), 
    ('ApprovedByArdy', 'Approved By Ardy'), 
    ('Paid', 'Paid'), 
    ('Rejected', 'Rejected')
]