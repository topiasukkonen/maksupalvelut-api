from typing import Optional
import requests

from .types import ExternalApiResponse, Maksupalveluntarjoaja
from .app import app

MAVE_API_URL = "http://api.boffsaopendata.fi/mave/api/v1/maksupalveluntarjoajat"


def fetch_payment_service_providers() -> Optional[ExternalApiResponse]:
    """Fetches payment service provider data from the MaVe API.

    Returns:
        Optional[ExternalApiResponse]: The payment service provider data or None if an error occurred.
    """
    try:
        app.logger.info("Fetching data from the MaVe API...")
        response = requests.get(MAVE_API_URL)
        response.raise_for_status()
        app.logger.info("Successfully fetched data from the API.")
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching data from the MaVe API: {e}")
        return None
    except ValueError as e:
        app.logger.error(f"Error parsing JSON response from the API: {e}")
        return None


def create_business_id_index(
    data: Optional[ExternalApiResponse],
) -> dict[str, Maksupalveluntarjoaja]:
    """Creates a search index based on business IDs (Y-tunnus).

    Args:
        data (Optional[ExternalApiResponse]): The payment service provider data.

    Returns:
        dict[str, Maksupalveluntarjoaja]: The search index.
    """
    index: dict[str, Maksupalveluntarjoaja] = {}
    if not data:
        app.logger.warning("No data provided to create business ID index.")
        return index

    for group in data:
        for company in group.get("maksupalveluntarjoajat", []):
            for identifier in company.get("tunnukset", []):
                if identifier.get("tyyppi") == "Y-tunnus" and identifier.get("tunnus"):
                    index[identifier["tunnus"]] = company
                    break

    app.logger.info(f"Created business ID index with {len(index)} entries.")
    return index


def create_name_index(
    data: Optional[ExternalApiResponse],
) -> dict[str, Maksupalveluntarjoaja]:
    """Creates a search index based on company names.

    Args:
        data (Optional[ExternalApiResponse]): The payment service provider data.

    Returns:
        dict[str, Maksupalveluntarjoaja]: The search index.
    """
    index: dict[str, Maksupalveluntarjoaja] = {}
    if not data:
        app.logger.warning("No data provided to create name index.")
        return index

    for group in data:
        for company in group.get("maksupalveluntarjoajat", []):
            if company.get("nimi"):
                index[company["nimi"]] = company

    app.logger.info(f"Created name index with {len(index)} entries.")
    return index
