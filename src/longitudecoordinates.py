from __future__ import annotations
from geocoordinate import GeoCoordinate
from customexceptions import InvalidArgument, InvalidSign, OutOfRange


class Longitude(GeoCoordinate):
    SIGNS = ('E', 'W', 'GM')
    __validate = True

    def __init__(self, degrees, minutes, seconds, sign='GM'):
        # Validate arguments ahead of any assignments
        if self.__validate:
            self.__fvalidate(degrees, minutes, seconds, sign)
        self.__sign = sign
        negative = True if self.__sign == 'W' else False
        super().__init__(degrees, minutes, seconds, negative)

    @property
    def sign(self):
        return self.__sign

    #---------------------------------------------#
    #-----------------PRESENTATION----------------#

    def __repr__(self):
        return f"{self.__class__.__name__}({self.degrees}, {self.minutes}, {self.seconds}, sign='{self.__sign}')"

    def __str__(self):
        return f"{self.degrees:02}\u00b0 {self.minutes:02}' {self.seconds:06.3f}\" {self.__sign}"

    @classmethod
    def longitude_validation(cls):
        return cls.__fvalidate

    @classmethod
    def enable_longitude_validation(cls):
        """Enables validation for Longitude"""
        cls.__validate = True

    @classmethod
    def disable_longitude_validation(cls):
        """Disables validation for Longitude"""
        cls.__validate = False

    @staticmethod
    def __fvalidate(degrees, minutes, seconds, sign):
        """Raises exception if argument does not seem to be valid for Longitude.

        This extends GeoCoordinate's argument validation
        by adding conditions specific to Longitude only.

        Args:
            degrees (int): Any positive integer (or zero)
            minutes (int): Any positive integer (or zero) of less than 60.
            seconds (IntegerorFloat): Any positive number of less than 60.
            sign (str): Describes the hemisphere.

        Raises:
            InvalidSign: Raised if sign argument does not conform with Latitude signs.
            OutOfRange: Raised if decimal degrees equivalent exceeds 90, positive or negative.
        """
        if sign not in Longitude.SIGNS:
            raise InvalidSign(Longitude.SIGNS,
                              f"Only the following signs are accepted: {Longitude.SIGNS}")
        if degrees > 180 or (degrees == 180 and (minutes != 0 or seconds != 0)):
            raise OutOfRange("Longitude cannot be more than 180 degrees.")
        if ((degrees, minutes, seconds) != (0, 0, 0)) and sign == 'GM':
            raise InvalidArgument(
                "Please indicate explicitly hemisphere sign for East and West.")

    @classmethod
    def cast(cls, float_coordinate) -> Longitude:
        """Cast a decimal degrees or a float (or just an integer) 
        representation of coordinates to GeoCoordinate type.

        Args:
            float_coordinate (IntegerorFloat): Negative values accepted.

        Returns:
            Latitude: A GeoCoordinate type.
        """
        geo = super().cast(float_coordinate)
        if (geo.degrees, geo.minutes, geo.seconds) == (0, 0, 0):
            sign = 'GM'
        else:
            sign = 'W' if geo.negative else 'E'
        return Longitude(geo.degrees, geo.minutes, geo.seconds, sign)


if __name__ == '__main__':
    y = Longitude.cast(-1)
    print(type(y) == GeoCoordinate)
