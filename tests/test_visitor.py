import pytest

from src.models import Visit, Visitor


class TestVisitor:
    # Tests that a new Visitor object can be created with the required parameters
    @pytest.mark.asyncio
    async def test_create_visitor_with_required_parameters(self):
        # Arrange
        name = "John Doe"

        # Act
        visitor = Visitor(name=name)

        # Assert
        assert visitor.name == name

    # Tests that the name attribute of the Visitor object can be updated
    @pytest.mark.asyncio
    async def test_update_name_attribute(self):
        # Arrange
        visitor = Visitor(name="John Doe")

        # Act
        visitor.name = "Jane Smith"

        # Assert
        assert visitor.name == "Jane Smith"

    # Tests that the Visitor object can be associated with a Visit object
    @pytest.mark.asyncio
    async def test_associate_with_visit(self):
        # Arrange
        visitor = Visitor(name="John Doe")
        visit = Visit()

        # Act
        visitor.visits.append(visit)

        # Assert
        assert visit in visitor.visits

    # Tests that the __repr__() method returns a string representation of the Visitor object
    @pytest.mark.asyncio
    async def test_repr_method_returns_string_representation(self):
        # Arrange
        visitor_name = "John Doe"
        visitor = Visitor(name=visitor_name)

        # Act
        repr_str = repr(visitor)

        # Assert
        assert repr_str == f"Visitor(id={visitor.id}, name={visitor_name})"

    # Tests that the __admin_repr__() method returns a string representation of the Visitor object suitable for the admin interface
    @pytest.mark.asyncio
    async def test_admin_repr_method_returns_string_representation(self):
        # Arrange
        visitor_name = "John Doe"
        visitor = Visitor(name=visitor_name)

        # Act
        admin_repr_str = await visitor.__admin_repr__(None)

        # Assert
        assert (
            admin_repr_str == visitor_name
        ), f"Expected {visitor_name}, but got {admin_repr_str}"
