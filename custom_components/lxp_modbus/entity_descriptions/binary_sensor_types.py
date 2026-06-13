from ..constants.input_registers import *
from ..utils import get_bits

BINARY_SENSOR_TYPES = [
    {
        # True when the utility grid is physically present, regardless of whether
        # the inverter is currently grid-tied or intentionally islanding.
        # I_FAC (register 15) is the grid-input frequency in 0.01 Hz units.
        # It reads 0 when no grid AC is present and ~5000-6000 when the grid is live.
        "name": "Đã kết nối lưới điện",
        "register_type": "calculated",
        "depends_on": [I_FAC],
        "extract": lambda registers, entry: registers.get(I_FAC, 0) > 0,
        "device_class": "connectivity",
        "enabled": True,
        "visible": True,
        "device_group": "Lưới điện",
        "master_only": False,
    },
    {
        "name": "BMS cho phép sạc",
        "register": I_BMS_BAT_STATUS_INV,
        "register_type": "input",
        "extract": lambda value: get_bits(value, 0, 1) != 0,
        "device_class": None,
        "enabled": True,
        "visible": True,
        "device_group": "Pin",
        "master_only": True,
    },
    {
        "name": "BMS cho phép xả",
        "register": I_BMS_BAT_STATUS_INV,
        "register_type": "input",
        "extract": lambda value: get_bits(value, 1, 1) != 0,
        "device_class": None,
        "enabled": True,
        "visible": True,
        "device_group": "Pin",
        "master_only": True,
    },
    {
        "name": "BMS yêu cầu sạc",
        "register": I_BMS_BAT_STATUS_INV,
        "register_type": "input",
        "extract": lambda value: get_bits(value, 4, 1) != 0,
        "device_class": "problem",
        "enabled": True,
        "visible": True,
        "device_group": "Pin",
        "master_only": True,
    },
    {
        "name": "BMS yêu cầu sạc đầy",
        "register": I_BMS_BAT_STATUS_INV,
        "register_type": "input",
        "extract": lambda value: get_bits(value, 5, 1) != 0,
        "device_class": "problem",
        "enabled": True,
        "visible": True,
        "device_group": "Pin",
        "master_only": True,
    },

]
