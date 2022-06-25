from __future__ import annotations
from os import stat
from geocoordinate import GeoCoordinate
from customexceptions import InvalidArgument, InvalidSign, OutOfRange


class Latitude(GeoCoordinate):
    """Latiude class is representation of Latitude, which is distance in degrees from equator.

    It inherits some of the methods from GeoCoordinate class."""
    SIGNS = ('N', 'S', 'Equator')
    __validate = True

    def __init__(self, degrees, minutes, seconds, sign='Equator'):
        """Initializes instance for Latitude class.

        Args:
            degrees (int): Any positive integer (or zero) of less than 90.
            minutes (int): Any positive integer (or zero) of less than 60.
            seconds (IntegerorFloat): Any positive number of less than 60.
            sign (str, optional): Sign to indicate hemisphere. Defaults to 'Equator'.
        """
        # Validate arguments ahead of any assignments
        if self.__validate:
            self.__fvalidate(degrees, minutes, seconds, sign)
        # Assign 'sign' attribute for presentation
        self.__sign = sign
        # Assign bool equivalent to variable 'negative'
        negative = True if self.__sign == 'S' else False
        # Then pass it to super()
        super().__init__(degrees, minutes, seconds, negative)

    @property
    def sign(self):
        """Returns the sign of the coordinate."""
        return self.__sign

    #---------------------------------------------#
    #-----------------PRESENTATION----------------#

    def __repr__(self):
        return f"{self.__class__.__name__}({self.degrees}, {self.minutes}, {self.seconds}, sign='{self.__sign}')"

    def __str__(self):
        return f"{self.degrees:02}\u00b0 {self.minutes:02}' {self.seconds:06.3f}\" {self.__sign}"

    @classmethod
    def latitude_validation(cls):
        return cls.__fvalidate

    @classmethod
    def enable_latitude_validation(cls):
        """Enables validation for Latitude"""
        cls.__validate = True

    @classmethod
    def disable_latitude_validation(cls):
        """Disables validation for Latitude"""
        cls.__validate = False

    @staticmethod
    def __fvalidate(degrees, minutes, seconds, sign):
        """Raises exception if argument does not seem to be valid for Latitude.

        In addition to GeoCoordinate's argument validation, it extends parent validation
        by adding conditions specific to Latitude only.

        Args:
            degrees (int): Any positive integer (or zero)
            minutes (int): Any positive integer (or zero) of less than 60.
            seconds (IntegerorFloat): Any positive number of less than 60.
            sign (str): Describes the hemisphere.

        Raises:
            InvalidSign: Raised if sign argument does not conform with Latitude signs.
            OutOfRange: Raised if decimal degrees equivalent exceeds 90, positive or negative.
        """
        if sign not in Latitude.SIGNS:
            raise InvalidSign(Latitude.SIGNS,
                              f"Only the following signs are accepted: {Latitude.SIGNS}")
        if degrees > 90 or (degrees == 90 and (minutes != 0 or seconds != 0)):
            raise OutOfRange("Latitude cannot be more than 90 degrees.")
        if ((degrees, minutes, seconds) != (0, 0, 0)) and sign == 'Equator':
            raise InvalidArgument(
                "Please indicate explicitly hemisphere sign for North and South.")

    @classmethod
    def cast(cls, float_coordinate) -> Latitude:
        """Cast a decimal degrees or a float (or just an integer) 
        representation of coordinates to GeoCoordinate type.

        Args:
            float_coordinate (IntegerorFloat): Negative values accepted.

        Returns:
            Latitude: A GeoCoordinate type.
        """
        geo = super().cast(float_coordinate)
        if (geo.degrees, geo.minutes, geo.seconds) == (0, 0, 0):
            sign = 'Equator'
        else:
            sign = 'S' if geo.negative else 'N'
        return Latitude(geo.degrees, geo.minutes, geo.seconds, sign)


if __name__ == '__main__':
    x = Latitude(1, 0, 0, 'N')
    y = x - x
    print(x.degrees)
    print(x.minutes)
    print(x.seconds)
    print(x.sign)
    # from GeoCoordinates
    print(x.negative)
    print(x.sign_factor)
