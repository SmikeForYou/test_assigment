from enum import Enum


class StandardizedTrackingStages:
    CREATED = "CREATED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    SHIPMENT_VOIDED = "SHIPMENT_VOIDED"
    EXCEPTION = "EXCEPTION"