# Roles
SUPERVISOR = "Supervisor"
FIELD_MANAGER = "Field Manager"
FINANCE_OFFICER = "Finance Office"
PROJECT_MANAGER = "Project Manager"
GENERAL_MANAGER = "General Manager"
######## End of Roles ############

# Types
ISP = 'ISP'
OFC = 'OFC'
OSP = 'OSP'
FINANCIAL = 'Financial'
WAREHOUSE = 'Warehouse'
POWER = 'Power'
MAINTENANCE = 'Maintenance'
WORKSHOP = 'Workshop'
ADMINISTRATOR = 'Administrator'
SECURITY = 'Security'
TRANSPORT = 'Transport'
MISCELLANEOUS = 'Miscellaneous'

TYPE_CHOICES = [
        (ISP, ISP),
        (OFC, OFC),
        (OSP, OSP),
        (FINANCIAL, FINANCIAL),
        (WAREHOUSE, WAREHOUSE),
        (POWER, POWER),
        (MAINTENANCE, MAINTENANCE),
        (WORKSHOP, WORKSHOP),
        (ADMINISTRATOR, ADMINISTRATOR),
        (SECURITY, SECURITY),
        (TRANSPORT, TRANSPORT),
        (MISCELLANEOUS, MISCELLANEOUS)
    ]

INTEGRITY_ERROR_MESSAGE = "The record you tried to add is a duplicate or contains duplicate values" \
                          " for unique fields."

INVALID_FORM_MESSAGE = "The form values are invalid or duplicate for unique fields."
