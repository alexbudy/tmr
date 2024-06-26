from bisect import bisect_right

from flask import current_app
from app.constants import DIST_INTERVALS
from app.models.models import ActivityType, CooperPoints
from app.utils.utils import standardize_duration


class CooperPointsService:
    @staticmethod
    def get_points(
        activity: str | ActivityType, distance: int | float | str, duration: int | str
    ) -> float:
        """
        Get the number of cooper points for the given activity and distance
        Args:
            activity (str|ActivityType): activity type
            distance (int|float): distance in mi or yards
            duration (int|str): duration in seconds or time string in (hh:)?mm:ss
        """
        if type(activity) == ActivityType:
            activity = activity.value
        activity: str = activity.lower()

        duration: str = standardize_duration(duration)  # capped at 10:00:01
        if duration == "00:00:00":
            # can't receive points for no time
            return 0

        distance = float(distance)
        dist_intervals = DIST_INTERVALS[activity]
        distance_floor_idx = bisect_right(dist_intervals, distance)

        if distance_floor_idx == 0:
            return 0  # distance not long enough to gain cooper points

        distance_floor = dist_intervals[
            distance_floor_idx - 1
        ]  # highest distance <= provided

        cooper_point = CooperPoints.find_row(activity, distance_floor, duration)
        if not cooper_point:
            current_app.logger.error(
                f"Cooper point not found, should be found for {activity=}, {distance=}, {duration=}"
            )
            return 0

        return float(cooper_point.points)
