import datetime
from datetime import timedelta

from sqlalchemy.orm import Session

# Start the scheduler
from .models import Visit, VisitState  # replace with your own models


def check_visit_expiry(session: Session):
    try:
        current_time = datetime.datetime.now()
        pending_visits = (
            session.query(Visit).filter(Visit.state == VisitState.PENDING).all()
        )
        print(pending_visits)
        for visit in pending_visits:
            # If the visit is pending and it's been 24 hours since the QR code was created
            if visit.date + timedelta(hours=24) < current_time:
                # Update the state of the visit to expired
                visit.state = VisitState.CANCELLED
        session.commit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        session.close()
