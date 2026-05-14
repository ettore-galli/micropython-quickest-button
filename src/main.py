import asyncio

from led.engine import LedButtonControlEngine
from led.hardware import (
    HardwareInformation,
    HardwarePin,
    HardwareTime,
    get_default_hardware_information,
)
from led.light_service import LedControlService, retrieve_light_blink_information

hardware_information: HardwareInformation = get_default_hardware_information()

light_service = LedControlService(
    time=HardwareTime(),
    pin_class=HardwarePin,
    hardware_information=hardware_information,
    light_blink_information_retriever=retrieve_light_blink_information,
)

if __name__ == "__main__":
    control_demo = LedButtonControlEngine(
        time=HardwareTime(),
        light_service=light_service,
    )
    asyncio.run(control_demo.main())
