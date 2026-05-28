import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database import engine, SessionLocal, Base
from backend.models import Ticket

with open("models/classifier.pkl", "rb") as f:
    classifier = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
    
Base.metadata.create_all(bind=engine)

app = FastAPI()

class TicketRequest(BaseModel):
    student_name: str
    complaint: str
    

@app.get("/")
def home():
    return {"message": "AI Hostel Complaint System Running"}

@app.post("/submit_ticket")
def submit_ticket(ticket: TicketRequest):

    db: Session = SessionLocal()

    
    complaint_vector = vectorizer.transform([ticket.complaint])
    predicted_category = classifier.predict(complaint_vector)[0]
    # Retrieve relevant policy
    # retrieved_policy = retrieve_policy(ticket.complaint)
    priority = "Medium"

    if predicted_category in ["Plumbing", "Electrical"]:
        priority = "High"
    new_ticket = Ticket(
        student_name=ticket.student_name,
        complaint=ticket.complaint,
        category=predicted_category,
        priority=priority
    )
    response_message = (
        f"Your complaint has been classified as "
        f"{predicted_category} and marked as "
        f"{priority} priority. "
        # f"Relevant policy: {retrieved_policy}"
    )


    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket submitted successfully",
        "ticket_id": new_ticket.id,
        "category": predicted_category,
        "priority": priority,
        # "policy": retrieved_policy,
        "response": response_message
    }
@app.get("/tickets")
def get_tickets():

    db: Session = SessionLocal()

    tickets = db.query(Ticket).all()

    return tickets