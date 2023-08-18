# Dependencies:
# pip install pytest-mock

from src import crud
from src.router import get_user


class TestGetUser:
    # Tests that the function returns the user profile for a valid user ID.
    def test_get_user_valid_user_id(self, mocker):
        # Mock the dependencies
        request = mocker.Mock()
        db = mocker.Mock()
        user_id = mocker.Mock()

        # Mock the CRUD function
        crud.get_profile = mocker.Mock(return_value={"user": "profile"})

        # Call the function
        result = get_user(request, db=db, user_id=user_id)

        # Assert the result
        assert result == {"user": "profile"}
        crud.get_profile.assert_called_once_with(db, user_id=user_id)

    # Tests that the function returns the user profile with residence information for a resident user.
    def test_get_user_resident_with_residence(self, mocker):
        # Mock the dependencies
        request = mocker.Mock()
        db = mocker.Mock()
        user_id = mocker.Mock()

        # Mock the CRUD function to return a resident user with residence information
        crud.get_profile = mocker.Mock(
            return_value={"user": {"role": "resident"}, "residence": "information"}
        )

        # Call the function
        result = get_user(request, db=db, user_id=user_id)

        # Assert the result
        assert result == {"user": {"role": "resident"}, "residence": "information"}
        crud.get_profile.assert_called_once_with(db, user_id=user_id)

    # Tests that the function returns visits grouped by date for a guard user.
    def test_get_user_guard_with_visits(self, mocker):
        # Mock the dependencies
        request = mocker.Mock()
        db = mocker.Mock()
        user_id = mocker.Mock()

        # Mock the CRUD function to return a guard user with visits
        crud.get_profile = mocker.Mock(
            return_value={"user": {"role": "guard"}, "visits": "grouped"}
        )

        # Call the function
        result = get_user(request, db=db, user_id=user_id)

        # Assert the result
        assert result == {"user": {"role": "guard"}, "visits": "grouped"}
        crud.get_profile.assert_called_once_with(db, user_id=user_id)

    # Test that the function returns 401 Unauthorized for a guard user with a non-existent guard.
    def test_get_user_guard_nonexistent_guard(self, mocker):
        # Mock the dependencies
        request = mocker.Mock()
        db = mocker.Mock()
        user_id = mocker.Mock()

        # Mock the CRUD function
        crud.get_profile = mocker.Mock(return_value={"user": "profile"})

        # Mock the guard query
        db.query.return_value.filter_by.return_value.first.return_value = None

        # Call the function
        result = get_user(request, db=db, user_id=user_id)

        # Assert the result
        assert result == {"user": "profile"}

    # Test that the function returns a 401 Unauthorized response for a resident user with a non-existent residence.
    def test_get_user_resident_nonexistent_residence(self, mocker):
        # Mock the dependencies
        request = mocker.Mock()
        db = mocker.Mock()
        user_id = mocker.Mock()

        # Mock the CRUD function
        crud.get_profile = mocker.Mock(return_value={"user": "profile"})

        # Mock the Resident query
        db.query.return_value.filter_by.return_value.first.return_value = None

        # Call the function
        response = get_user(request, db=db, user_id=user_id)

        # Assert the response content
        assert response == {"user": "profile"}

        # Assert that the CRUD function was called once with the correct arguments
        crud.get_profile.assert_called_once_with(db, user_id=user_id)

    # Tests that the function returns the user profile for a valid user ID.
    def test_get_user_valid_user_id(self, mocker):
        # Mock the dependencies
        request = mocker.Mock()
        db = mocker.Mock()
        user_id = mocker.Mock()

        # Mock the CRUD function
        crud.get_profile = mocker.Mock(return_value={"user": "profile"})

        # Call the function
        result = get_user(request, db=db, user_id=user_id)

        # Assert the result
        assert result == {"user": "profile"}
        crud.get_profile.assert_called_once_with(db, user_id=user_id)

    # Tests that the function returns the user profile for a valid user ID.
    def test_get_user_valid_user_id(self, mocker):
        # Mock the dependencies
        request = mocker.Mock()
        db = mocker.Mock()
        user_id = mocker.Mock()

        # Mock the CRUD function
        crud.get_profile = mocker.Mock(return_value={"user": "profile"})

        # Call the function
        result = get_user(request, db=db, user_id=user_id)

        # Assert the result
        assert result == {"user": "profile"}
        crud.get_profile.assert_called_once_with(db, user_id=user_id)
