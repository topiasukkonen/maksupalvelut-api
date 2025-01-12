from flask import Response, jsonify

from .utils import (
    create_business_id_index,
    create_name_index,
    fetch_payment_service_providers,
)
from .app import app
from .types import Maksupalveluntarjoaja

# Fetch data and initialize indices
payment_service_providers_data = fetch_payment_service_providers()
business_id_index: dict[str, Maksupalveluntarjoaja] = create_business_id_index(
    payment_service_providers_data
)
name_index: dict[str, Maksupalveluntarjoaja] = create_name_index(
    payment_service_providers_data
)


@app.route("/licenses/<string:business_id>", methods=["GET"])
def get_licenses(business_id: str) -> tuple[Response, int]:
    """
    Returns the licenses of a payment service provider based on the business ID.

    Args:
        business_id (str): The business ID of the payment service provider.

    Returns:
        tuple[Response, int]: A JSON response containing the licenses or an error message.
    """
    company_data = business_id_index.get(business_id)
    if company_data is None:
        error_message = (
            f"Payment service provider with business ID '{business_id}' not found."
        )
        app.logger.warning(error_message)
        return jsonify({"error": error_message}), 404

    licenses = company_data.get("luvat")
    if licenses is None:
        error_message = f"Payment service provider with business ID '{business_id}' has no registered licenses."
        app.logger.warning(error_message)
        return jsonify({"error": error_message}), 404

    results = []
    for license_data in licenses:
        law_section = license_data.get("lakipykala")

        results.append(
            {"law_section": law_section, "country": license_data.get("valtio")}
        )

    app.logger.info(f"Successfully retrieved licenses for business ID '{business_id}'.")
    return jsonify(results), 200


@app.route("/contacts/<string:company_name>", methods=["GET"])
def get_contacts(company_name: str) -> tuple[Response, int]:
    """
    Returns the contact information of a payment service provider based on the company name.

    Args:
        company_name (str): The name of the payment service provider.

    Returns:
        tuple[Response, int]: A JSON response containing the contact information or an error message.
    """
    company_data = name_index.get(company_name)

    if company_data is None:
        error_message = (
            f"Payment service provider with name '{company_name}' not found."
        )
        app.logger.warning(error_message)
        return jsonify({"error": error_message}), 404

    contacts = {
        "postal_address": company_data.get("postiosoite1"),
        "postal_address_line_2": company_data.get("postiosoite2"),
        "postal_code": company_data.get("postinumero"),
        "post_office": company_data.get("postitp"),
        "country": company_data.get("valtio"),
    }
    app.logger.info(f"Successfully retrieved contacts for company '{company_name}'.")
    return jsonify(contacts), 200
