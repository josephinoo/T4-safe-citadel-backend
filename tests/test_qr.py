from datetime import datetime
from uuid import uuid4

from src.models import Qr, Visit


class TestQr:
    # Tests that a Qr object can be created successfully with custom parameters
    def test_create_qr_with_custom_parameters(self):
        # Create custom parameters for Qr object
        id = uuid4()
        created_date = datetime.now()
        code = "custom_code"
        visit = Visit()

        # Create Qr object with custom parameters
        qr = Qr(id=id, created_date=created_date, code=code, visit=visit)

        # Assert that Qr object is created successfully with custom parameters
        assert qr.id == id
        assert qr.created_date == created_date
        assert qr.code == code
        assert qr.visit == visit

    # Tests that a Qr object can be associated with a Visit object
    def test_associate_qr_with_visit(self):
        # Create Qr and Visit objects
        qr = Qr()
        visit = Visit()

        # Associate Qr object with Visit object
        qr.visit = visit

        # Assert that Qr object is associated with Visit object
        assert qr.visit == visit

    # Tests that a Qr object can generate a unique code on creation
    def test_generate_unique_code_on_creation(self):
        # Create two Qr objects with unique codes
        qr1 = Qr(code=str(uuid4()))
        qr2 = Qr(code=str(uuid4()))

        # Assert that the codes of the two Qr objects are unique
        assert qr1.code != qr2.code

    # Tests that a Qr object can be associated with a Visit object with a custom date
    def test_associate_qr_with_visit_with_custom_date(self):
        # Create custom date for Visit object
        date = datetime.now()

        # Create Qr and Visit objects with custom date
        qr = Qr()
        visit = Visit(date=date)

        # Associate Qr object with Visit object
        qr.visit = visit

        # Assert that Qr object is associated with Visit object with custom date
        assert qr.visit == visit
        assert qr.visit.date == date

    # Tests that a Qr object can be associated with a Visit object with additional information
    def test_associate_qr_with_visit_with_additional_information(self):
        # Create additional information for Visit object
        additional_info = {"key": "value"}

        # Create Qr and Visit objects with additional information
        qr = Qr()
        visit = Visit(additional_info=additional_info)

        # Associate Qr object with Visit object
        qr.visit = visit

        # Assert that Qr object is associated with Visit object with additional information
        assert qr.visit == visit
        assert qr.visit.additional_info == additional_info
