import fire
import questionary



# Still need a cyc function

def get_user_risk_tolerance_port():
    """
    Get user information to determine risk tolerance
    """
    risk_tolerance = questionary.select("What's your risk tolerance", choices=["Low", "Medium", "High"]).ask()

    indexes = questionary.select("Of the following indexes, select the index that best reflects your current portfolio.", choices=["NASDAQ", "Russel", "S&P 500", "EAFE"]).ask()

    # crypto_benchmark = questionary.select("Would you like to benchmark your crypto against an index, a specific crypto, or a composite of cryptos?", choices=["Index", "Crypto", "Crypto Composite"]).ask()

    goals = questionary.text("Would you like to acomplish a dollar goal or a percentage return goal? (Start with a '$' if dollar goal and with '%' if percent goal").ask()

    invest_amount = int(questionary.text("How much would you like to invest?").ask())

    stock_portfolio = {}
    adding = True
    while adding:
        sp = questionary.text("Enter stock from stock portfolio: ").ask()
        sw = int(questionary.text("Enter Share Amount: ").ask())
        cont = questionary.confirm("Continue?").ask()
        stock_portfolio[sp] = sw
        if cont == False:
            adding = False

    user_dictionary = {"risk tolerance": risk_tolerance,
                        "index": indexes,
                        "Investment Goals": goals,
                        "Investment Amount": invest_amount,
                        "Stock Portfolio": stock_portfolio}

    return user_dictionary