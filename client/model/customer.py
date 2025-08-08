from pydantic import BaseModel, EmailStr


class Customer(BaseModel):
    title: str | None = None
    first_name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    mobile: str | None = None
    phone: str | None = None
    mobile_country_code: str | None = None
    phone_country_code: str | None = None
    receive_email_marketing: bool | None = None
    receive_sms_marketing: bool | None = None
