from enum import Enum as PythonEnum


class UserTypeEnum(PythonEnum):
    Admin = "admin"
    Customer = "customer"
    Provider = "provider"

class BookingStatusEnum(PythonEnum):
    Pending = "pending"
    Assigned = "assigned"
    Ongoing = "ongoing"
    Completed = "completed"
    Cancelled = "cancelled"
    Rejected = "rejected"