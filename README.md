# Maksupalvelut API

This project provides a simple API to retrieve information about payment service providers in Finland, based on data from the Finnish Financial Supervisory Authority's open data API (MaVe API).

## Functionality

The API supports the following functionalities:

*   **Retrieve Licenses by Business ID:**  Fetch a list of licenses held by a payment service provider, identified by their Finnish business ID (Y-tunnus).
*   **Retrieve Contact Information by Company Name:** Fetch the contact information of a payment service provider, identified by their name.

The API fetches the latest data from the [Finnish Financial Supervisory Authority's open data API](http://api.boffsaopendata.fi/mave/api/v1/maksupalveluntarjoajat) once when the API is run and saves it in memory for quick access.

## Project Structure

*   **`main.py`**: The entry point of the application. It initializes and runs the Flask application.
*   **`src/`**: Contains the source code of the application.
    *   **`app.py`**: Initializes the Flask application and configures logging.
    *   **`routes.py`**: Defines the API routes and their corresponding logic for retrieving data. It also fetches the initial data and creates in-memory indices for faster lookups.
    *   **`types.py`**: Defines type hints for data structures, improving code readability and maintainability.
    *   **`utils.py`**: Contains utility functions, such as fetching data from the external API and creating search indices.
*   **`tests/`**: Contains the test suite for the API endpoints.
    *   **`test_api.py`**:  Includes tests for the API endpoints, verifying successful responses and error handling.
*   **`README.md`**: This file, providing an overview and instructions for the project.
*   **`pyproject.toml`**: Contains the project's dependencies and build configuration for Poetry.

## Installation

Follow these steps to set up the project on your local machine:

1. **Prerequisites:**
    *   **Python 3.13 or higher:**
    *   **Poetry:**

2. **Clone the repository:**
    ```bash
    git clone [add repo]
    cd maksupalvelut-api
    ```

3. **Install dependencies:**
    Install the project dependencies using Poetry:

    ```bash
    poetry install
    ```

## Running the Application

To start the API, execute the following command from the project's root directory:

```bash
poetry run maksupalvelut-api
```

This command starts the Flask development server. By default, it will listen to `http://127.0.0.1:5000/`.

## API Endpoints

Once the application is running, you can access the following endpoints:

*   **Get Licenses by Business ID:**
    *   **Endpoint:** `/licenses/<business_id>`
    *   **Method:** `GET`
    *   **Description:** Retrieves a list of licenses for the payment service provider with the specified business ID.
    *   **Example:** `http://127.0.0.1:5000/licenses/2382421-3`
    *   **Response (Success - 200 OK):**
        ```json
        [
            {
                "country": "Suomi",
                "law_section": "UlkMLL 5 §"
            },
            {
                "country": "Suomi",
                "law_section": "MLL 1 § 2 mom 3 kohta, EBA ITS alakohta 5a)"
            },
            ...
        ]
        ```
    *   **Response (Not Found - 404 Not Found):**
        ```json
        {
          "error": "Payment service provider with business ID 'xyz' not found."
        }
        ```

*   **Get Contact Information by Company Name:**
    *   **Endpoint:** `/contacts/<company_name>`
    *   **Method:** `GET`
    *   **Description:** Retrieves the contact information for the payment service provider with the specified name.
    *   **Example:** `http://127.0.0.1:5000/contacts/AS%20SEB%20Pank`
    *   **Response (Success - 200 OK):**
        ```json
        {
            "country": "Viro",
            "post_office": "Tallinn",
            "postal_address": "Tornimäe 2",
            "postal_address_line_2": null,
            "postal_code": null
        }
        ```
    *   **Response (Not Found - 404 Not Found):**
        ```json
        {
          "error": "Payment service provider with name 'xyz' not found."
        }
        ```

## Running Tests

The project includes a suite of tests to verify the functionality of the API endpoints. To run the tests, use Poetry to execute `pytest`:

```bash
poetry run pytest
```

This command will execute the tests defined in the `tests/test_api.py` file within the project's virtual environment and report the results.