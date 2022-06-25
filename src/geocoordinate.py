# __future__ must be imported first; this enables type hint to return current class
from __future__ import annotations
from typing import Union, TypeVar
from customexceptions import InvalidArgument
from math import isclose, trunc


IntegerorFloat = Union[int, float]
GeoCoordinateorFloat = Union[TypeVar('GeoCoordinate'), float]


class GeoCoordinate:
    """GeoCoordinate is representation of coordinates in Earth's Coordinate system."""
    # CLASS DEFAULTS
    __validate_arguments: bool = True
    __comparison_tolerance: dict = {'abs_tol': 0.000001}  # NOQA Not used in computations, only for comparison

    def __init__(self, degrees: int, minutes: int,
                 seconds: IntegerorFloat, negative=False):
        """Initializes an instance of GeoCoordinate

        Args:
            degrees (int): Any positive integer (or zero)
            minutes (int): Any positive integer (or zero) of less than 60.
            seconds (IntegerorFloat): Any positive number of less than 60.
            negative (bool): Describes the hemisphere. Defaults to False.
        """
        # Enabled validation by default.
        if GeoCoordinate.__validate_arguments:
            GeoCoordinate.__func_validate_arguments(
                degrees, minutes, seconds, negative)
        # Required to apply correction before assigning arguments to instance variables
        self._degrees, \
            self._minutes, \
            self._seconds, \
            self._negative \
            = GeoCoordinate.__correction(
                degrees, minutes, seconds, negative)
        # Used for computation and presentation
        self._sign_factor, self._sign = (-1,
                                         '-') if self._negative else (1, '')

    #---------------------------------------------#
    #--------------CLASS PROPERTIES---------------#

    @property
    def degrees(self) -> int:
        return self._degrees

    @property
    def minutes(self) -> int:
        return self._minutes

    @property
    def seconds(self) -> float:
        return self._seconds

    @property
    def sign_factor(self) -> int:
        return self._sign_factor

    @property
    def negative(self) -> bool:
        return self._negative

    @property
    def sign(self) -> str:
        return self._sign

    #---------------------------------------------#
    #-----------------PRESENTATION----------------#

    def __repr__(self):
        # Returns the classname(degrees, minutes, seconds, negative: bool)
        return f"{self.__class__.__name__}({self._degrees}, {self._minutes}, {self._seconds}, negative={self._negative})"

    def __str__(self):
        # Returns conventional display of coodinates.
        # Hemisphere may be indicated by (or lack of) '-' sign.
        return f"{self._sign}{self._degrees}\u00b0 {self._minutes}' {self._seconds}\""

    def __float__(self):
        # Converts a GeoCoordinate to a floating point number representation
        # of coordinates.
        # Basically also called 'Decimal Degrees'.
        # It is rounded to 8 digits, enough for precision of less than 1 cm at any point.
        return round((self._degrees + self._minutes/60 + self._seconds/3600)
                     * self._sign_factor, 8)

    #---------------------------------------------#
    #---------BASIC ARITHMETIC OPERATIONS---------#

    def __add__(self, other) -> GeoCoordinate:
        return self.cast(float(self) + float(other))

    def __radd__(self, other) -> GeoCoordinate:
        return self.cast(float(other) + float(self))

    def __sub__(self, other) -> GeoCoordinate:
        return self.cast(float(self) - float(other))

    def __rsub__(self, other) -> GeoCoordinate:
        return self.cast(float(other) - float(self))

    def __mul__(self, other) -> GeoCoordinate:
        return self.cast(float(self) * float(other))

    def __rmul__(self, other) -> GeoCoordinate:
        return self.cast(float(other) * float(self))

    def __truediv__(self, other) -> GeoCoordinate:
        return self.cast(float(self) / float(other))

    def __rtruediv__(self, other) -> GeoCoordinate:
        return self.cast(float(other) / float(self))

    #---------------------------------------------#
    #-------------COMPARISON OPERATIONS-----------#

    @classmethod
    def get_comparison_tolerance(cls) -> dict:
        """Get a dict containing comparison tolerance, absolute and relative.

        Returns:
            dict: Current tolerance in making comparisons.
        """
        return cls.__comparison_tolerance

    @classmethod
    def set_comparison_tolerance(cls, abs_tol: float, rel_tol: float = 1e-09) -> None:
        """Set comparison tolerance, may specify either or
        both absolute and relative tolerance.

        Args:
            abs_tol (float): Is the number of significant places when instance is represented
                             as float.
            rel_tol (float, optional): It is better to leave this default, probable makes no 
                                       significance yet. Might remove setting option for 
                                       this in the future. Defaults to 1e-09.
        """
        cls.__comparison_tolerance['rel_tol'] = rel_tol
        cls.__comparison_tolerance['abs_tol'] = abs_tol

    def __eq__(self, other) -> bool:
        if isclose(float(self), float(other), **GeoCoordinate.__comparison_tolerance):
            return True
        else:
            return False

    def __lt__(self: GeoCoordinate, other: GeoCoordinate) -> bool:
        if not isclose(float(self), float(other),
                       **GeoCoordinate.__comparison_tolerance) and float(self) > float(other):
            return True
        else:
            return False

    def __gt__(self: GeoCoordinate, other: GeoCoordinate) -> bool:
        if not isclose(float(self), float(other),
                       **GeoCoordinate.__comparison_tolerance) and float(self) > float(other):
            return True
        else:
            return False

    def __ge__(self: GeoCoordinate, other: GeoCoordinate) -> bool:
        if self == other or self > other:
            return True
        else:
            False

    def __le__(self: GeoCoordinate, other: GeoCoordinate) -> bool:
        if self == other or self < other:
            return True
        else:
            False

    #---------------------------------------------#
    #----------------CLASS METHODS----------------#

    @classmethod
    def validation_status(cls) -> bool:
        """Show validation if enabled/disabled for all class and its subclass.

        Returns:
            bool: True if enabled, False otherwise.
        """
        return cls.__validate_arguments

    @classmethod
    def enable_validation(cls) -> None:
        """Class method to enable validation for all class and its subclass."""
        cls.__validate_arguments = True

    @classmethod
    def disable_validation(cls) -> None:
        """Class method to disable validation for all class and its subclass."""
        cls.__validate_arguments = False

    @staticmethod
    def __func_validate_arguments(degrees: int, minutes: int, seconds: IntegerorFloat, negative: bool):
        """Raise exception if any of the arguments is invalid.

        This static method is called in '__init__()' if class-level variable '_validate_arguments' is True.
        To optimize code for performance, you may choose to disable the validation by setting _validate_arguments to False.
        Use GeoCoordinate.enable_validation() or GeoCoordinate.disable_validation() accordingly.

        This function ensures that arguments passed onto this class is acceptable and will not cause errors in computations.

        Any argument that does not satisfy the following, will raise an Error:
        1. degrees and minutes types passed types must be integers only.
        2. degrees, minutes, and seconds values must not be negative.
        3. minutes and seconds values passed must not be >= 60.
        4. if positional arguments are all zero, then negative must not be negative.

        Args:
            degrees (int): Any positive integer (or zero)
            minutes (int): Any positive integer (or zero) of less than 60.
            seconds (IntegerorFloat): Any positive number of less than 60.
            negative (bool): Describes the hemisphere.

        Raises:
            InvalidArgument: If any of the conditions were not met.
        """
        if isinstance(degrees, float) or isinstance(minutes, float):
            raise InvalidArgument(
                "Accepts only integer values as argument for degrees and minutes.")
        if degrees < 0 or minutes < 0 or seconds < 0:
            raise InvalidArgument(
                "Positional arguments can only be postive numbers. If you mean to pass negative coordinates, use negative=False keyword.")
        if minutes >= 60 or seconds >= 60:
            raise InvalidArgument(
                "Values for minutes and seconds argument must not be greater than or equal to 60.")
        if ((degrees, minutes, seconds) == (0, 0, 0)) and negative:
            raise InvalidArgument("Coordinates at zero must not be negative.")

    #---------------------------------------------#
    #-------------CONVERSION METHODS--------------#

    @classmethod
    def cast(cls, float_coordinate: IntegerorFloat) -> GeoCoordinate:
        """Cast a decimal degrees or a float (or just an integer) 
        representation of coordinates to GeoCoordinate type.

        Args:
            float_coordinate (IntegerorFloat): Negative values accepted.

        Returns:
            GeoCoordinate: A GeoCoordinate type.
        """
        degrees = trunc(float_coordinate)
        minutes = (float_coordinate - trunc(float_coordinate)) * 60
        seconds = (minutes - trunc(minutes)) * 60
        negative = True if float_coordinate < 0 else False
        return GeoCoordinate(abs(degrees), abs(trunc(minutes)), abs(seconds), negative)

    #---------------------------------------------#
    #-----------------CORRECTION------------------#
    @staticmethod
    def __correction(degrees, minutes, seconds, negative):
        """Applies required correction to seconds or minutes if it is
        equal to 60.

        Args:
            degrees (int): Any positive integer (or zero)
            minutes (int): Any positive integer (or zero) of less than 60.
            seconds (IntegerorFloat): Any positive number of less than 60.
            negative (bool): Describes the hemisphere.

        Returns:
            tuple: Returns corrected version of arguments in '__init__()'.
        """
        # multiply abs_tol by 3600 to make it equivalent to seconds
        if isclose(seconds, 60, abs_tol=GeoCoordinate.__comparison_tolerance['abs_tol']*3600):
            minutes += 1
            seconds = 0
        if minutes >= 60:
            minutes = 0
            degrees += 1
        return degrees, minutes, seconds, negative


if __name__ == '__main__':
    pass
