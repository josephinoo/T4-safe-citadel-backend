import datetime
from datetime import timedelta

from sqlalchemy.orm import Session

# Start the scheduler
from src.config.database import get_session

from .models import Visit, VisitState  # replace with your own models


def check_visit_expiry():
    try:
        # Get a session
        db: Session = get_session

        # Current time
        current_time = datetime.datetime.now()

        # Get all the pending visits
        pending_visits = db.query(Visit).filter(Visit.state == VisitState.PENDING)

        for visit in pending_visits:
            # If the visit is pending and it's been 24 hours since the QR code was created
            if visit.created_date + timedelta(hours=24) < current_time:
                # Update the state of the visit to expired
                visit.state = VisitState.EXPIRED

        # Commit the changes
        db.commit()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        db.close()
