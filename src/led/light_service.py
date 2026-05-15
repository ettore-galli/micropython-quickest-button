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

        self.response_buttons = [
            self.pin_class(pin, self.pin_class.IN, self.pin_class.PULL_UP)
            for pin in self.hardware_information.led_button_pins
        ]

        self.reset_button = self.pin_class(
            self.hardware_information.reset_button_pin,
            self.pin_class.IN,
            self.pin_class.PULL_UP,
        )

        for response_button in self.response_buttons:
            response_button.irq(
                trigger=self.pin_class.IRQ_FALLING, handler=self.response_button_handler
            )

        self.reset_button.irq(
            trigger=self.pin_class.IRQ_FALLING, handler=self.reset_button_handler
        )

        self.light_blink_information_retriever = light_blink_information_retriever

    def reset_button_handler(self, pin: BasePin) -> None:
        print("AAAAAAAAAAAAA")
        print(pin)

    def response_button_handler(self, pin: BasePin) -> None:
        print("AAAAAAAAAAAAA")
        print(pin)

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
