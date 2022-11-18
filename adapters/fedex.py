from datetime import datetime

import schemas
from enums import StandardizedTrackingStages

fedex_tracking_stages = {
    # have to be extended with https://developer.fedex.com/api/en-us/guides/api-reference.html#trackingstatuscodes
    "OC": StandardizedTrackingStages.CREATED,
    "PU": StandardizedTrackingStages.PICKED_UP,
    "OD": StandardizedTrackingStages.OUT_FOR_DELIVERY,
    "IT": StandardizedTrackingStages.IN_TRANSIT,
    "DL": StandardizedTrackingStages.DELIVERED,
    "DE": StandardizedTrackingStages.EXCEPTION,
    "SE": StandardizedTrackingStages.EXCEPTION,
}


def fedex_tracking_response_adapter(data: dict) -> schemas.TrackingResponse:
    def process_checkpoint(data: dict) -> schemas.Checkpoint:
        scan_location = data.get("scanLocation", {})
        return schemas.Checkpoint(
            description=data.get("eventDescription"),
            location=schemas.Location(
                city=scan_location.get("city"),
                country=scan_location.get("countryName"),
                postal_code=scan_location.get("postalCode"),
                state=scan_location.get("stateOrProvinceCode")
            )
        )

    track_results = data.get("output", {}).get("completeTrackResults", [])[0].get("trackResults", [])[0]
    checkpoints = map(process_checkpoint, track_results.get("scanEvents"))
    status = track_results.get("latestStatusDetail").get("code")
    tracking_stage = fedex_tracking_stages.get(status, "UNKNOWN. CONTACT ADMINISTRATOR")
    estimated_delivery_end_time = track_results.get("estimatedDeliveryTimeWindow", {}).get("window", {}).get("ends", "")
    delivery_date = ""
    delivery_date_present = list(
            filter(lambda x: x.get("type") == "ACTUAL_DELIVERY",
                   track_results.get("dateAndTimes", []))
    )
    if delivery_date_present:
        delivery_date = delivery_date_present[0].get("dateTime")
    adapted = schemas.TrackingResponse(
        carrier="fedex",
        description=track_results.get("latestStatusDetail").get("description"),
        checkpoints=list(checkpoints),
        status=status,
        time=str(datetime.now()),
        tracking_stage=tracking_stage,
        delivered=tracking_stage == StandardizedTrackingStages.DELIVERED,
        delivery_date=delivery_date,
        estimated_delivery=estimated_delivery_end_time or delivery_date,
        tracking_number=track_results.get("trackingNumberInfo", {}).get("trackingNumber"),
    )
    return adapted
