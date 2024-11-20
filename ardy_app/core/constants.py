# core/constants.py

USER_TYPES = [('Customer', 'Customer'), ('Consultant', 'Consultant'),
            ('Interior Designer', 'Interior Designer'), ('Construction', 'Construction'),
            ('Maintainance', 'Maintainance'),('Smart_Home', 'Smart_Home'), ('Admin', 'Admin'),]

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
    ('Cancelled', 'Cancelled')
]

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