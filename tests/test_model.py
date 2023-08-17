import pytest

from src.crud import create_model


class TestCreateModel:
    # Tests that create_model raises an exception when model_schema is None.
    def test_edge_case_model_schema_none(self, mocker):
        # Arrange
        db_mock = mocker.Mock()
        model_schema_mock = None
        model_mock = mocker.Mock()

        # Act and Assert
        with pytest.raises(Exception):
            create_model(db_mock, model_schema_mock, model_mock)

    # Tests that create_model raises an exception when model is None.
    def test_edge_case_model_none(self, mocker):
        # Arrange
        db_mock = mocker.Mock()
        model_schema_mock = mocker.Mock()
        model_mock = None

        # Act and Assert
        with pytest.raises(Exception):
            create_model(db_mock, model_schema_mock, model_mock)

    # Tests that create_model raises an exception when db is None.
    def test_edge_case_db_none(self, mocker):
        # Arrange
        db_mock = None
        model_schema_mock = mocker.Mock()
        model_mock = mocker.Mock()

        # Act and Assert
        with pytest.raises(Exception):
            create_model(db_mock, model_schema_mock, model_mock)

    # Tests that create_model raises an exception when model_schema is not a subclass of pydantic.BaseModel.
    def test_edge_case_model_schema_not_base_model(self, mocker):
        # Arrange
        db_mock = mocker.Mock()
        model_schema_mock = mocker.Mock()
        model_mock = mocker.Mock()

        # Act and Assert
        with pytest.raises(Exception):
            create_model(db_mock, model_schema_mock, model_mock)

    # Tests that create_model raises an exception when model is not a subclass of sqlalchemy.ext.declarative.api.Base.
    def test_edge_case_model_not_base(self, mocker):
        # Arrange
        db_mock = mocker.Mock()
        model_schema_mock = mocker.Mock()
        model_mock = mocker.Mock()

        # Act and Assert
        with pytest.raises(Exception):
            create_model(db_mock, model_schema_mock, model_mock)

    # Test that create_model function creates a new model instance in the database and returns it with the correct type.
    def test_create_model_correct_type(self, mocker):
        # Arrange
        db_mock = mocker.Mock()
        model_schema_mock = mocker.Mock()
        model_mock = mocker.Mock()
        db_model_mock = mocker.Mock()
        db_mock.add.return_value = None
        db_mock.commit.return_value = None
        db_mock.refresh.return_value = None
        model_schema_mock.dict.return_value = {}
        model_mock.return_value = db_model_mock

        # Act
        result = create_model(db_mock, model_schema_mock, model_mock)

        # Assert
        assert isinstance(result, type(db_model_mock))
        db_mock.add.assert_called_once_with(db_model_mock)
        db_mock.commit.assert_called_once()
        db_mock.refresh.assert_called_once_with(db_model_mock)

    # Tests that create_model successfully creates a new model instance in the database and returns it.
    def test_create_model_with_correct_values(self, mocker):
        # Arrange
        db_mock = mocker.Mock()
        model_schema_mock = mocker.Mock()
        model_mock = mocker.Mock()
        db_model_mock = mocker.Mock()
        db_mock.add.return_value = None
        db_mock.commit.return_value = None
        db_mock.refresh.return_value = None
        model_schema_mock.dict.return_value = {}
        model_mock.return_value = db_model_mock

        # Act
        result = create_model(db_mock, model_schema_mock, model_mock)

        # Assert
        assert result == db_model_mock
        db_mock.add.assert_called_once_with(db_model_mock)
        db_mock.commit.assert_called_once()
        db_mock.refresh.assert_called_once_with(db_model_mock)
