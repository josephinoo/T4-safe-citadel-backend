import uuid

from fastapi import Response, status
from sqlalchemy.orm import Session

from . import models


def verify_qr_code(session: Session, qr_id: str, user_id: uuid.UUID):
    """
    Verify a QR code record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        qr_id (str): ID of the QR code.

    Returns:
        QR: Verified QR instance.
    """
    resident = session.query(models.Resident)
    resident = resident.join(models.User).filter(models.User.id == user_id).first()
    if resident is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    qr = session.query(models.QR).filter_by(id=qr_id).first()
    if qr is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    visit = session.query(models.Visit).filter_by(qr_id=qr_id).first()
    return visit
