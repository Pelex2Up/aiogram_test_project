from aiogram.utils.callback_data import CallbackData


# setting timepicker_callback prefix and parts
timepicker_callback = CallbackData('minute_timepicker', 'act', 'minute')

_default = {
    'select': 'Select',
    'back': 'Back',
    'cancel': 'Cancel',
    'empty': ' ',
    'minute_format': '{0:02}',
    'minute_unavailable_format': '{0:02}',
    'minute_current_format': '({0:02})',
}

from .timepicker import TimePicker
from .utils import default
