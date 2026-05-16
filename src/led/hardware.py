import asyncio
from collections.abc import Callable

import utime as time  # type: ignore[import-not-found]
from machine import Pin  # type: ignore[import-not-found]

from led.base import (
    BasePin,
    BaseTime,
)


class HardwareTime(BaseTime):
    async def sleep(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    def ticks_ms(self) -> int:
        return time.ticks_ms()


class HardwarePin(BasePin):
    OUT: int = 1
    IN: int = 0
    ON: int = 1
    OFF: int = 0

    def __init__(self, pin_id: int, mode: int, pull: int = -1) -> None:
        self.pin_id: int = pin_id
        self.mode: int = mode
        self.pull: int = pull
        self._pin: Pin = Pin(pin_id, mode, pull)
        self._pin.irq()

    def on(self) -> None:
        self._pin.on()

    def off(self) -> None:
        self._pin.off()

    def value(self) -> int:
        return self._pin.value()

    def is_on(self) -> bool:
        return self.value() == self.ON

    def id(self) -> int:
        return self._pin.id()

    def irq(
        self,
        handler: Callable[["BasePin"], None] | None = None,
        trigger: int = Pin.IRQ_FALLING,
    ) -> object:

        return self._pin.irq(
            handler=handler,
            trigger=trigger,
        )


class HardwareInformation:
    def __init__(
        self,
        led_pin: int,
        led_pins: list[int],
        button_pins: list[int],
        button_to_led_mapping: dict[int, int],
        reset_button_pin: int,
    ) -> None:
        self.led_pin: int = led_pin
        self.led_pins: list[int] = led_pins
        self.led_button_pins: list[int] = button_pins
        self.button_to_led_mapping = button_to_led_mapping
        self.reset_button_pin: int = reset_button_pin


def get_default_hardware_information() -> HardwareInformation:
    return HardwareInformation(
        led_pin=0,
        led_pins=[10, 11, 12, 13, 14],
        button_pins=[17, 18, 19, 20, 21],
        button_to_led_mapping={
            17: 14,
            18: 13,
            19: 12,
            20: 11,
            21: 10,
        },
        reset_button_pin=22,
    )
