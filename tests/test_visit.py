import datetime
from uuid import uuid4

import pytest

from src.models import Guard, Qr, Resident, Visit, Visitor, VisitState


class TestVisit:
    # Tests that a new Visit object can be created with all required parameters
    @pytest.mark.asyncio
    async def test_create_visit_with_required_parameters(self):
        # Create required parameters for Visit object
        date = datetime.datetime.now()
        qr = Qr()
        visitor = Visitor()
        guard = Guard()
        resident = Resident()

        # Create Visit object with required parameters
        visit = Visit(date=date, qr=qr, visitor=visitor, guard=guard, resident=resident)

        # Assert that Visit object is created successfully
        assert visit.date == date
        assert visit.qr == qr
        assert visit.visitor == visitor
        assert visit.guard == guard
        assert visit.resident == resident

    # Tests that the to_dict() method returns a dictionary containing all attributes of the Visit object
    @pytest.mark.asyncio
    async def test_to_dict_method_returns_all_attributes(self):
        # Create Visit object with attributes
        visit = Visit()
        visit.id = uuid4()
        visit.created_date = datetime.datetime.now()
        visit.date = datetime.datetime.now()
        visit.register_date = datetime.datetime.now()
        visit.state = VisitState.PENDING
        visit.additional_info = {"key": "value"}
        visit.qr_id = uuid4()
        visit.visitor_id = uuid4()
        visit.guard_id = uuid4()
        visit.resident_id = uuid4()

        # Call to_dict() method
        visit_dict = visit.to_dict()

        # Assert that the dictionary contains all attributes of the Visit object
        assert visit_dict["id"] == visit.id
        assert visit_dict["created_date"] == visit.created_date
        assert visit_dict["date"] == visit.date
        assert visit_dict["register_date"] == visit.register_date
        assert visit_dict["state"] == visit.state
        assert visit_dict["additional_info"] == visit.additional_info
        assert visit_dict["qr_id"] == visit.qr_id
        assert visit_dict["visitor_id"] == visit.visitor_id
        assert visit_dict["guard_id"] == visit.guard_id
        assert visit_dict["resident_id"] == visit.resident_id

    # Tests that the state attribute of the Visit object can be updated
    @pytest.mark.asyncio
    async def test_update_state_attribute(self):
        # Create Visit object with initial state
        visit = Visit()
        visit.state = VisitState.PENDING

        # Update state attribute
        visit.state = VisitState.REGISTERED

        # Assert that the state attribute is updated
        assert visit.state == VisitState.REGISTERED

    # Tests that the Visit object can be associated with a QR code, a visitor, a guard, and a resident
    @pytest.mark.asyncio
    async def test_associate_with_qr_visitor_guard_resident(self):
        # Create Visit object
        visit = Visit()

        # Create QR, Visitor, Guard, and Resident objects
        qr = Qr()
        visitor = Visitor()
        guard = Guard()
        resident = Resident()

        # Associate Visit object with QR, Visitor, Guard, and Resident objects
        visit.qr = qr
        visit.visitor = visitor
        visit.guard = guard
        visit.resident = resident

        # Assert that the Visit object is associated with the QR, Visitor, Guard, and Resident objects
        assert visit.qr == qr
        assert visit.visitor == visitor
        assert visit.guard == guard
        assert visit.resident == resident
