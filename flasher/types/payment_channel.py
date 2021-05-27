from __future__ import annotations

import typing as t
import dataclasses


@dataclasses.dataclass(frozen=True)
class PaymentChannel:
    """
    Currently available channel data can be stored here
    """
    name: str
    channel_id: int
    options: t.Dict[str, str] = None
    version: int = 2

    def option_keys(self) -> t.List[str]:
        return list(self.options.keys())

    def has_option(self) -> bool:
        return self.options is not None


@dataclasses.dataclass(frozen=True)
class Payment:
    """
    ready-to-use channel data will be stored here
    """
    name: str
    channel_id: int
    option: t.Optional[str]
    version: int

    @staticmethod
    def from_channel(channel: PaymentChannel, selected_option: t.Optional[t.Union[int, str]] = None) -> Payment:
        type_ = type(selected_option)

        if type_ == int:
            return Payment(channel.name, channel.channel_id,
                           channel.options[channel.option_keys()[selected_option]], channel.version)
        elif type_ == str:
            return Payment(channel.name, channel.channel_id, channel.options[selected_option], channel.version)

        return Payment(channel.name, channel.channel_id, None, channel.version)
