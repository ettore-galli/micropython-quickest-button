from collections.abc import Callable

from led.base import (
    DEFAULT_LIGHT_BLINK_INFORMATION,
    BaseLedControlService,
    BasePin,
    BaseTime,
    LightBlinkInformation,
)
from led.hardware import HardwareInformation


class LedControlService(BaseLedControlService):
    def __init__(
        self,
        time: BaseTime,
        pin_class: type[BasePin],
        hardware_information: HardwareInformation,
        light_blink_information_retriever: Callable[[], LightBlinkInformation],
    ) -> None:

        self.time: BaseTime = time
        self.pin_class: type[BasePin] = pin_class

        self.hardware_information = (
            hardware_information
            if hardware_information is not None
            else HardwareInformation()
        )

        self.leds = [
            self.pin_class(pin, self.pin_class.OUT)
            for pin in self.hardware_information.led_pins
        ]

        self.light_blink_information_retriever = light_blink_information_retriever

    async def blink_loop(self) -> None:
        pass

    async def led_loop(self) -> None:
        info: LightBlinkInformation = self.light_blink_information_retriever()

        while True:
            for led in self.leds:
                led.off()
            for led in self.leds:
                led.on()
                await self.time.sleep(info.flash_duration)

                led.off()
                await self.time.sleep(info.intra_flash_delay)

            await self.time.sleep(info.intra_loop_delay)


def retrieve_light_blink_information() -> LightBlinkInformation:
    return DEFAULT_LIGHT_BLINK_INFORMATION
