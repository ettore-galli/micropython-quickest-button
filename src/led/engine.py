import asyncio
import sys

from led.base import (
    BaseLightService,
    BaseTime,
)
from led.light_service import LightService


class LedBlinkerEngine:
    LED_ON: int = 1
    LED_OFF: int = 0

    def __init__(
        self,
        time: BaseTime,
        light_service: LightService,
    ) -> None:
        self.time: BaseTime = time

        self.light_service: BaseLightService = light_service

    def log(self, message: str) -> None:
        sys.stdout.write(f"{self.time.ticks_ms()}: {message}\n")

    async def main(self) -> None:
        await asyncio.gather(
            self.light_service.led_loop(),
        )
