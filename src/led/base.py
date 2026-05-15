from abc import ABC, abstractmethod
from collections.abc import Callable

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
    PULL_UP: int = 1
    PULL_DOWN: int = 2
    IRQ_FALLING: int = 4
    IRQ_RISING: int = 8
    IRQ_LOW_LEVEL: int = 1
    IRQ_HIGH_LEVEL: int = 2

    def __init__(self, pin_id: int, mode: int, pull: int = -1) -> None:
        self.pin_id: int = pin_id
        self.mode: int = mode
        self.pull: int = pull

    @abstractmethod
    def on(self) -> None:
        pass

    @abstractmethod
    def off(self) -> None:
        pass

    @abstractmethod
    def value(self) -> int:
        pass

    @abstractmethod
    def id(self) -> int:
        pass

    @abstractmethod
    def irq(
        self,
        handler: Callable[["BasePin"], None] | None = None,
        trigger: int = (IRQ_FALLING | IRQ_RISING),
    ) -> object:
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
