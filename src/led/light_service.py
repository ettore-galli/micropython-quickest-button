from collections.abc import Callable

from machine import Pin  # type: ignore[import-not-found]

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

        self.leds: list[Pin] = []
        self.response_buttons: list[Pin] = []

        for idx, (button, led) in enumerate(
            self.hardware_information.button_to_led_mapping.items()
        ):
            self.leds.append(self.pin_class(led, self.pin_class.OUT))

            response_button = self.pin_class(
                button, self.pin_class.IN, self.pin_class.PULL_UP
            )

            response_button.irq(
                trigger=self.pin_class.IRQ_FALLING,
                handler=self.response_button_handler_builder(led_id=idx),
            )

            self.response_buttons.append(response_button)

        self.reset_button = self.pin_class(
            self.hardware_information.reset_button_pin,
            self.pin_class.IN,
            self.pin_class.PULL_UP,
        )

        self.reset_button.irq(
            trigger=self.pin_class.IRQ_FALLING, handler=self.reset_button_handler
        )

        self.light_blink_information_retriever = light_blink_information_retriever

        self.led_is_lit: bool = False

    def reset_button_handler(self, _: Pin) -> None:
        for led in self.leds:
            led.off()
            self.led_is_lit = False

    def response_button_handler_builder(self, led_id: int) -> Callable[[Pin], None]:
        def handler(_: Pin) -> None:
            if not self.led_is_lit:
                self.leds[led_id].on()
                self.led_is_lit = True

        return handler

    async def blink_loop(self) -> None:
        pass

    async def led_loop(self) -> None: ...


def retrieve_light_blink_information() -> LightBlinkInformation:
    return DEFAULT_LIGHT_BLINK_INFORMATION
