class DemandFunction:
    """
    The demand function is a map of the price of a product to its slaes.

    The demand function must give the quantity of the product
    that will be sold by any agent in the market at a given price
    """

    def get_sales(price: float) -> int:
        """
        Calculates the quantity of the product that will be sold at a given price

        Parameters
        __________
        price : float
            The current price of the product set by some agent

        Returns
        _______
        int
            The quantity of the product that will be sold at the given price

        Raises
        ______
        NotImplementedError
            If concrete class does not override method.
        """

        raise NotImplementedError
