from typing import List, Optional, TypedDict

# Types for the external API responses


class MaksupalveluntarjoajanTunnus(TypedDict):
    tunnus: Optional[str]
    tyyppi: Optional[str]


class MaksupalveluntarjoajanLupa(TypedDict):
    valtio: Optional[str]
    lakipykala: Optional[str]


class Maksupalveluntarjoaja(TypedDict):
    valtio: Optional[str]
    tunnukset: Optional[List[MaksupalveluntarjoajanTunnus]]
    nimi: Optional[str]
    postiosoite1: Optional[str]
    postiosoite2: Optional[str]
    postinumero: Optional[str]
    postitp: Optional[str]
    luvat: Optional[List[MaksupalveluntarjoajanLupa]]


class Maksupalveluntarjoajaryhma(TypedDict):
    maksupalveluntarjoajat: Optional[List[Maksupalveluntarjoaja]]


ExternalApiResponse = List[Maksupalveluntarjoajaryhma]
