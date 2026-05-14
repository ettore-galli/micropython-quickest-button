import asyncio

from led.base import (
    LED_PIN_15,
    AccessPointInformation,
)
from led.engine import LedBlinkerEngine
from led.hardware import (
    ACCESS_POINT_INFORMATION,
    HardwareInformation,
    HardwarePin,
    HardwareTime,
)
from led.light_service import LightService, retrieve_light_blink_information

hardware_information: HardwareInformation = HardwareInformation(led_pin=LED_PIN_15)

access_point_information: AccessPointInformation = ACCESS_POINT_INFORMATION

light_service = LightService(
    time=HardwareTime(),
    pin_class=HardwarePin,
    hardware_information=hardware_information,
    light_blink_information_retriever=retrieve_light_blink_information,
)

if __name__ == "__main__":
    control_demo = LedBlinkerEngine(
        time=HardwareTime(),
        light_service=light_service,
    )
    asyncio.run(control_demo.main())
