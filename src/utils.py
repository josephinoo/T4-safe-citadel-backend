import itertools
import uuid

from fastapi import Response, status
from sqlalchemy.orm import Session

from . import models


def verify_qr_code(db: Session, qr_id: str, user_id: uuid.UUID):
    """
    Verify a QR code record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        qr_id (str): ID of the QR code.

    Returns:
        QR: Verified QR instance.
    """
    user = db.query(models.User).filter_by(id=user_id).first()
    if user is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    qr = db.query(models.Qr).filter_by(id=qr_id).first()
    if qr is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    visit = db.query(models.Visit).filter_by(qr_id=qr_id, user_id=user_id).first()
    if visit is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return visit


def grouped_dict(it) -> dict:
    """
    Group a list of dictionaries by a key.
    """
    grouped = {k: list(g) for k, g in itertools.groupby(it, lambda t: t.state)}
    return grouped
