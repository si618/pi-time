"""Computational related functions."""

from pi_time import settings


def average_speed_per_hour(start, finish, distance,
                           unit_of_measurement=settings.METRIC):
    """
    Calculates average speed per hour.

    :param start: Starting time. Must be before finish time.
    :type start: datetime
    :param finish: Finishing time. Must be after start time.
    :type finish: datetime
    :param distance: Distance travelled. Must be greater than zero.
    :type distance: int or float
    :param unit_of_measurement: Unit of measurement. Defaults to metric.
    :type unit_of_measurement: str
    :returns: Average speed per hour in specified unit of measurement.
    :rtype: float
    """
    if unit_of_measurement == settings.METRIC:
        return average_kilometres_per_hour(start, finish, distance)
    elif unit_of_measurement == settings.IMPERIAL:
        return average_miles_per_hour(start, finish, distance)
    else:
        raise ValueError("Unknown unit of measurement '%s'" %
                         unit_of_measurement)


def average_speed_per_second(start, finish, distance):
    """
    Calculates average speed per second.

    :param start: Starting time. Must be before finish time.
    :type start: datetime
    :param finish: Finishing time. Must be after start time.
    :type finish: datetime
    :param distance: Distance travelled. Must be greater than zero.
    :type distance: int or float
    :returns: Average speed per second in specified unit of measurement.
    :rtype: float
    """
    if start is None or finish is None:
        return None
    if finish <= start:
        raise ValueError("Start time must be before finish time!")
    if distance <= 0:
        raise ValueError("Track distance must be greater than zero!")
    delta = finish - start
    avg_per_second = float(distance) / delta.seconds
    return avg_per_second


def average_kilometres_per_hour(start, finish, metres):
    """
    Calculates average kilometres per hour.

    :param start: Starting time. Must be before finish time.
    :type start: datetime
    :param finish: Finishing time. Must be after start time.
    :type finish: datetime
    :param metres: Metres travelled. Must be greater than zero.
    :type metres: int or float
    :returns: Average kilometres per hour.
    :rtype: float
    """
    avg_per_second = average_speed_per_second(start, finish, metres)
    if avg_per_second is None:
        return None
    # Shortcut 3,600 seconds in a hour / 1,000 metres in a kilometre
    avg_km_per_hour = avg_per_second * 3.6
    return round(avg_km_per_hour, 4)


def average_miles_per_hour(start, finish, yards):
    """
    Calculates average miles per hour.

    :param start: Starting time. Must be before finish time.
    :type start: datetime
    :param finish: Finishing time. Must be after start time.
    :type finish: datetime
    :param yards: Yards travelled. Must be greater than zero.
    :type yards: int or float
    :returns: Average miles per hour.
    :rtype: float
    """
    avg_per_second = average_speed_per_second(start, finish, yards)
    if avg_per_second is None:
        return None
    avg_miles_per_hour = avg_per_second * 2.04545455
    return round(avg_miles_per_hour, 4)
