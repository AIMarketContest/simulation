class DemandFunction:
    """
    The demand function is a map of the price of a product to its slaes.
    
    The demand function must give the quantity of the product 
    that will be sold by any agent in the market at a given price
    """
    def get_sales(price : float) -> int:
        raise NotImplementedError