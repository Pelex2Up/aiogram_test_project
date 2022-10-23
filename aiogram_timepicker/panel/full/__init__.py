from aiogram.utils.callback_data import CallbackData

# setting timepicker_callback prefix and parts
timepicker_callback = CallbackData('full_timepicker', 'act', 'hour', 'minute')

_default = {
    'up': '↑',
    'down': '↓',
    'select': 'Подтвердить',
    'cancel': 'Cancel',
    'empty': ' ',
    'hour_format': '{0:02}ч',
    'minute_format': '{0:02}м',
}

from .timepicker import TimePicker
from .utils import default
