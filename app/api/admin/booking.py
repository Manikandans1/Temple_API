from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.booking import Booking, BookingStatusEnum, booking_services
from app.models.booking_person import BookingPerson
from app.models.service import Service
from app.schemas.booking import BookingSchema, BookingResponseSchema
from typing import List
from app.models.temple import Temple
from sqlalchemy.orm import joinedload
import stripe
import os

router = APIRouter()

# Set Stripe API Key (Replace with actual key)
STRIPE_SECRET_KEY = "sk_test_51QMRv3Fj439McXMca9tS2CfJlcUqH5OkoHa9sZQl9DW4bIkYn6vxVuinkQU4vQnUzXq87H2ipaEfOdh0HNJXXKRw0082y7oiW6"
STRIPE_WEBHOOK_SECRET = "whsec_8c7e13bb6d52e4b0c8d0f5c07947ed4e4501d2ad6ca4beacbd3c600319fc231c"
stripe.api_key = STRIPE_SECRET_KEY

@router.post("/bookings/", response_model=BookingResponseSchema)
def create_booking(
    booking_data: BookingSchema,
    db: Session = Depends(get_db),
):
    temple = db.query(Temple).filter(Temple.id == booking_data.temple_id).first()
    if not temple:
        raise HTTPException(status_code=404, detail="Temple not found")
    
    services = db.query(Service).filter(Service.id.in_(booking_data.services)).all()
    if not services:
        raise HTTPException(status_code=404, detail="One or more services not found")

    total_price = sum(service.price for service in services)

    booking = Booking(
        temple_id=booking_data.temple_id,
        user_id=None,
        total_price=total_price,
        video_type=booking_data.video_type,
        status=BookingStatusEnum.PENDING
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    for service in services:
        db.execute(booking_services.insert().values(booking_id=booking.id, service_id=service.id))

    for person in booking_data.persons:
        new_person = BookingPerson(
            booking_id=booking.id,
            name=person.name,
            gothram=person.gothram,
            rasi=person.rasi,
            nakshatra=person.nakshatra
        )
        db.add(new_person)
    
    db.commit()
    return booking

# @router.post("/bookings/{booking_id}/pay")
# def initiate_payment(booking_id: int, db: Session = Depends(get_db)):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()
#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking not found")

#     if booking.status == BookingStatusEnum.CONFIRMED:
#         return {"message": "Booking is already confirmed."}

#     payment_intent = stripe.PaymentIntent.create(
#         amount=int(booking.total_price * 100),
#         currency="usd",
#         payment_method_types=["card", "upi"],
#     )

#     booking.payment_id = payment_intent.id
#     db.commit()
#     db.refresh(booking)

#     return {"client_secret": payment_intent.client_secret, "payment_intent_id": payment_intent.id}



@router.post("/bookings/{booking_id}/pay")
async def create_payment_intent(booking_id: str, data: dict):
    try:
        amount = data.get("amount")
        currency = data.get("currency")
        payment_method_types = data.get("payment_method_types", ["card"])

        if not amount or not currency:
            raise HTTPException(status_code=400, detail="Missing required fields")

        # 🔹 Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=payment_method_types,
        )

        return {"client_secret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/api/bookings/{booking_id}/pay")
# async def create_payment_intent(booking_id: str, data: dict):
#     try:
#         amount = data["amount"]
#         currency = data["currency"]
#         payment_method_types = data["payment_method_types"]

#         intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency=currency,
#             payment_method_types=payment_method_types,
#         )

#         return {"client_secret": intent.client_secret}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        payment_id = payment_intent["id"]

        booking = db.query(Booking).filter(Booking.payment_id == payment_id).first()
        if booking:
            booking.status = BookingStatusEnum.CONFIRMED
            db.commit()
            db.refresh(booking)

    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        payment_id = payment_intent["id"]
        
        booking = db.query(Booking).filter(Booking.payment_id == payment_id).first()
        if booking:
            booking.status = BookingStatusEnum.FAILED
            db.commit()
    
    return {"status": "success"}

@router.get("/temple/{temple_id}/bookings", response_model=List[BookingResponseSchema])
def get_bookings(temple_id: int, db: Session = Depends(get_db)):
    bookings = db.query(Booking).options(joinedload(Booking.persons)).filter(Booking.temple_id == temple_id).all()
    return bookings

@router.put("/bookings/{booking_id}/status")
def update_booking_status(
    booking_id: int, 
    status: BookingStatusEnum, 
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.status = status
    db.commit()
    db.refresh(booking)
    return {"message": f"Booking ID {booking_id} status updated to {status.value}"}






# from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request
# from sqlalchemy.orm import Session
# from app.db.database import get_db
# from app.models.booking import Booking, BookingStatusEnum, booking_services
# from app.models.booking_person import BookingPerson
# from app.models.service import Service
# from app.schemas.booking import BookingSchema, BookingResponseSchema
# from typing import List
# from app.models.temple import Temple
# from sqlalchemy.orm import joinedload
# import stripe
# import os

# app = FastAPI()
# router = APIRouter()

# # Set Stripe API Key (Replace with actual key)
# STRIPE_SECRET_KEY = "sk_test_51QMRv3Fj439McXMca9tS2CfJlcUqH5OkoHa9sZQl9DW4bIkYn6vxVuinkQU4vQnUzXq87H2ipaEfOdh0HNJXXKRw0082y7oiW6"
# STRIPE_WEBHOOK_SECRET = "whsec_8c7e13bb6d52e4b0c8d0f5c07947ed4e4501d2ad6ca4beacbd3c600319fc231c"
# stripe.api_key = STRIPE_SECRET_KEY

# ### ✅ 1. Create Booking (Initial Status: PENDING) ###
# @router.post("/bookings/", response_model=BookingResponseSchema)
# def create_booking(
#     booking_data: BookingSchema,
#     db: Session = Depends(get_db),
# ):
#     temple = db.query(Temple).filter(Temple.id == booking_data.temple_id).first()
#     if not temple:
#         raise HTTPException(status_code=404, detail="Temple not found")
    
#     services = db.query(Service).filter(Service.id.in_(booking_data.services)).all()
#     if not services:
#         raise HTTPException(status_code=404, detail="One or more services not found")

#     total_price = sum(service.price for service in services)

#     booking = Booking(
#         temple_id=booking_data.temple_id,
#         user_id=None,
#         total_price=total_price,
#         video_type=booking_data.video_type,
#         status=BookingStatusEnum.PENDING
#     )
#     db.add(booking)
#     db.commit()
#     db.refresh(booking)

#     for service in services:
#         db.execute(booking_services.insert().values(booking_id=booking.id, service_id=service.id))

#     for person in booking_data.persons:
#         new_person = BookingPerson(
#             booking_id=booking.id,
#             name=person.name,
#             gothram=person.gothram,
#             rasi=person.rasi,
#             nakshatra=person.nakshatra
#         )
#         db.add(new_person)
    
#     db.commit()
#     return booking

# ### ✅ 2. Initialize Stripe Payment ###
# @router.post("/bookings/{booking_id}/pay")
# def initiate_payment(booking_id: int, db: Session = Depends(get_db)):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()
#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking not found")

#     if booking.status == BookingStatusEnum.CONFIRMED:
#         return {"message": "Booking is already confirmed."}

#     # Create Stripe Payment Intent
#     payment_intent = stripe.PaymentIntent.create(
#         amount=int(booking.total_price * 100),  # Convert to cents
#         currency="usd",
#         payment_method_types=["card", "upi"],
#     )

#     # Store Payment Intent ID in the database
#     booking.payment_id = payment_intent.id
#     db.commit()
#     db.refresh(booking)

#     return {"client_secret": payment_intent.client_secret, "payment_intent_id": payment_intent.id}

# ### ✅ 3. Stripe Webhook (Automatic Booking Confirmation After Payment) ###
# @router.post("/webhook")
# async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
#     payload = await request.body()
#     sig_header = request.headers.get("stripe-signature")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid payload")
#     except stripe.error.SignatureVerificationError:
#         raise HTTPException(status_code=400, detail="Invalid signature")

#     if event["type"] == "payment_intent.succeeded":
#         payment_intent = event["data"]["object"]
#         payment_id = payment_intent["id"]

#         # Find the booking using payment_id
#         booking = db.query(Booking).filter(Booking.payment_id == payment_id).first()
#         if booking:
#             booking.status = BookingStatusEnum.CONFIRMED
#             db.commit()

#     elif event["type"] == "payment_intent.payment_failed":
#         payment_intent = event["data"]["object"]
#         payment_id = payment_intent["id"]

#         # Find the booking and mark it as FAILED
#         booking = db.query(Booking).filter(Booking.payment_id == payment_id).first()
#         if booking:
#             booking.status = BookingStatusEnum.FAILED
#             db.commit()
    
#     return {"status": "success"}

# ### ✅ 4. Get Bookings for a Temple ###
# @router.get("/temple/{temple_id}/bookings", response_model=List[BookingResponseSchema])
# def get_bookings(temple_id: int, db: Session = Depends(get_db)):
#     bookings = db.query(Booking).options(joinedload(Booking.persons)).filter(Booking.temple_id == temple_id).all()
#     return bookings

# ### ✅ 5. Manually Update Booking Status (For Admin Use) ###
# @router.put("/bookings/{booking_id}/status")
# def update_booking_status(
#     booking_id: int, 
#     status: BookingStatusEnum, 
#     db: Session = Depends(get_db)
# ):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()
#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking not found")

#     booking.status = status
#     db.commit()
#     db.refresh(booking)
#     return {"message": f"Booking ID {booking_id} status updated to {status.value}"}

# app.include_router(router)


# @router.put("/api/bookings/{booking_id}/confirm")
# def confirm_booking(booking_id: int, db: Session = Depends(get_db)):
#     booking = db.query(Booking).filter(Booking.id == booking_id).first()
    
#     if not booking:
#         raise HTTPException(status_code=404, detail="Booking not found")

#     if booking.status != BookingStatusEnum.PENDING:
#         raise HTTPException(status_code=400, detail="Booking is already confirmed or failed")

#     # Update booking status to CONFIRMED
#     booking.status = BookingStatusEnum.CONFIRMED
#     db.commit()
    
#     return {"message": f"Booking ID {booking_id} is confirmed successfully!"}

# app.include_router(router)
