from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, TypeAlias

Incomplete: TypeAlias = Any

SpecialPins: TypeAlias = str


rpi_logger = print


class BaseTime(ABC):
    @abstractmethod
    async def sleep(self, seconds: float) -> None:
        _ = seconds

    @abstractmethod
    def ticks_ms(self) -> int:
        return 0


class BasePin(ABC):
    OUT: int = 1
    IN: int = 0

    def __init__(self, pin_id: int | SpecialPins, mode: int) -> None:
        _ = pin_id, mode

    @abstractmethod
    def on(self) -> None:
        pass

    @abstractmethod
    def off(self) -> None:
        pass

    @abstractmethod
    def value(self) -> int:
        pass


class LightBlinkInformation:
    def __init__(
        self,
        number_of_flashes: int,
        flash_duration: float,
        intra_flash_delay: float,
        intra_loop_delay: float,
    ) -> None:
        self.number_of_flashes: int = number_of_flashes
        self.flash_duration: float = flash_duration
        self.intra_flash_delay: float = intra_flash_delay
        self.intra_loop_delay: float = intra_loop_delay


DEFAULT_LIGHT_BLINK_INFORMATION = LightBlinkInformation(
    number_of_flashes=3, flash_duration=0.1, intra_flash_delay=0.2, intra_loop_delay=0.8
)


class BaseLedControlService(ABC):
    def __init__(
        self,
        light_blink_information_retriever: Callable[[], LightBlinkInformation],
    ) -> None:
        self.light_blink_information_retriever = light_blink_information_retriever

    @abstractmethod
    async def led_loop(self) -> None:
        pass
