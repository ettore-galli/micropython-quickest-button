import asyncio

import utime as time  # type: ignore[import-not-found]
from machine import Pin  # type: ignore[import-not-found]

from led.base import (
    BasePin,
    BaseTime,
    SpecialPins,
)


class HardwareTime(BaseTime):
    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    def ticks_ms(self) -> int:
        return time.ticks_ms()


class HardwarePin(BasePin):
    OUT: int = 1
    IN: int = 0

    def __init__(self, pin_id: int | SpecialPins, mode: int) -> None:
        self._pin: Pin = Pin(pin_id, mode)

    def on(self) -> None:
        self._pin.on()

    def off(self) -> None:
        self._pin.off()

    def value(self) -> int:
        return self._pin.value()


class HardwareInformation:
    def __init__(
        self,
        led_pin: int | SpecialPins,
        led_pins: list[int],
        led_button_pins: list[int],
        reset_button_pin: int,
    ) -> None:
        self.led_pin: int | SpecialPins = led_pin
        self.led_pins: list[int] = led_pins
        self.led_button_pins: list[int] = led_button_pins
        self.reset_button_pin: int = reset_button_pin


def get_default_hardware_information() -> HardwareInformation:
    return HardwareInformation(
        led_pin=0,
        led_pins=[10, 11, 12, 13, 14],
        led_button_pins=[2, 3, 4, 5, 6],
        reset_button_pin=7,
    )
