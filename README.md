# Safe Citadel API 

The Safe Citadel API is a RESTful service designed to provide secure, fast and reliable services for managing user data.

## Setup and Installation 

To get started with the Safe Citadel API, you'll need to set up a virtual environment and install the necessary dependencies. 

### Prerequisites 

You need to have Python 3.8 or later and pip installed on your system. 

### Instructions 

1. Clone the repository:

    ```bash
    git clone https://github.com/josephinoo/backend.git
    ```

2. Create a virtual environment and activate it:

    On Unix or MacOS:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

    On Windows:

    ```bash
    py -m venv env
    .\env\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Install Alembic for database migration:

    ```bash
    pip install alembic
    ```

5. Run the migrations:

    ```bash
    alembic upgrade head
    ```

## Usage

To start the server:

```bash
uvicorn main:app --reload
```

## Endpoints


## Tests

To run the test suite:

```bash
pytest
```

## Contributing

Please see our `CONTRIBUTING.md` for instructions on how to contribute to this project.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
