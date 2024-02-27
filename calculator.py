class Calculator:
    """
    A class for performing various statistical calculations.

    This class provides static methods for calculating the mean, median,
    and sum of the newest N elements in a list of numerical values. It is
    designed to support the processing of financial instrument data but can
    be used in any context where such statistical calculations are needed.
    """

    @staticmethod
    def calculate_mean(values):
        """
        Calculate the mean (average) of a list of values.

        Parameters:
        - values (list of float): A list of numerical values.

        Returns:
        - float: The mean of the list of values. Returns None if the list is empty.
        """
        return sum(values) / len(values) if values else None

    @staticmethod
    def calculate_median(values):
        """
        Calculate the median of a list of values.

        The median is the middle value in a list sorted in ascending order.
        For a list with an even number of elements, it is the average of the
        two middle values.

        Parameters:
        - values (list of float): A list of numerical values.

        Returns:
        - float: The median of the list of values. If the list is empty, returns None.
        """
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0 if n else None
        else:
            return sorted_values[mid] if n else None

    @staticmethod
    def sum_newest(values, n=10):
        """
        Calculate the sum of the newest (most recent) N elements in a list.

        This method assumes the list of values is in chronological order,
        with the most recent values last. It sorts the values in descending
        order before summing the newest N elements.

        Parameters:
        - values (list of float): A list of numerical values.
        - n (int): The number of newest elements to sum.

        Returns:
        - float: The sum of the newest N elements in the list.
        """
        return sum(sorted(values, reverse=True)[:n])

