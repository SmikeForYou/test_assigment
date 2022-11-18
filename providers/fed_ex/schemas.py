from typing import List

from pydantic import BaseModel


class AuthRequest(BaseModel):
    grant_type: str
    client_id: str
    client_secret: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str


class TrackingNumberInfo(BaseModel):
    trackingNumber: str


class TrackingInfo(BaseModel):
    trackingNumberInfo: TrackingNumberInfo


class TrackingRequest(BaseModel):
    trackingInfo: List[TrackingInfo]
    includeDetailedScans: bool = True

    @classmethod
    def by_tracking_number_only(cls, tracking_number: str) -> "TrackingRequest":
        return cls(includeDetailedScans=True,
                   trackingInfo=[
                       TrackingInfo(
                           trackingNumberInfo=TrackingNumberInfo(trackingNumber=tracking_number)
                       )
                   ])


class ReferenceInformation(BaseModel):
    type: str
    accountNumber: str
    value: str
    carrierCode: str


class TrackByReferenceRequest(BaseModel):
    referencesInformation: ReferenceInformation
    includeDetailedScans: bool = True

    @classmethod
    def by_tracking_number(cls,
                           tracking_number: str,
                           account_number: str,
                           type_: str,
                           carrier_code: str) -> "TrackByReferenceRequest":
        return cls(referencesInformation=ReferenceInformation(
            accountNumber=account_number,
            value=tracking_number,
            type=type_,
            carrierCode=carrier_code
        ))