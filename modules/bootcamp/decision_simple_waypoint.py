"""
BOOTCAMPERS TO COMPLETE.

Travel to designated waypoint.
"""

from .. import commands
from .. import drone_report


from .. import drone_status
from .. import location
from ..private.decision import base_decision


class DecisionSimpleWaypoint(base_decision.BaseDecision):
    """
    Travel to the designed waypoint.
    """

    def __init__(self, waypoint: location.Location, acceptance_radius: float) -> None:
        """
        Initialize all persistent variables here with self.
        """
        self.waypoint = waypoint
        print(f"Waypoint: {waypoint}")

        self.acceptance_radius = acceptance_radius

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Add your own
        self.start_simulator = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

    def run(
        self, report: drone_report.DroneReport, landing_pad_locations: "list[location.Location]"
    ) -> commands.Command:
        """
        Make the drone fly to the waypoint.

        You are allowed to create as many helper methods as you want,
        as long as you do not change the __init__() and run() signatures.

        This method will be called in an infinite loop, something like this:

        ```py
        while True:
            report, landing_pad_locations = get_input()
            command = Decision.run(report, landing_pad_locations)
            put_output(command)
        ```
        """
        # Default command
        command = commands.Command.create_null_command()

        # ============
        # ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
        # ============

        # Do something based on the report and the state of this class...

        distance_to_waypoint = self.distance(report)

        if self.start_simulator and report.status == drone_status.DroneStatus.HALTED:
            command = commands.Command.create_set_relative_destination_command(
                self.waypoint.location_x - report.position.location_x,
                self.waypoint.location_y - report.position.location_y,
            )
            self.start_simulator = False
        elif (
            report.status == drone_status.DroneStatus.HALTED
            and distance_to_waypoint <= self.acceptance_radius
        ):
            command = commands.Command.create_land_command()
        elif report.status == drone_status.DroneStatus.HALTED:
            self.start_simulator = True

        # ============
        # ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
        # ============

        return command

    def distance(self, report: drone_report.DroneReport) -> float:
        """
        Find the distance between the reported position and the waypoint
        """
        x = report.position.location_x
        y = report.position.location_y

        x_w = self.waypoint.location_x
        y_w = self.waypoint.location_y
        return (((x - x_w) ** 2) + ((y - y_w) ** 2)) ** 0.5
