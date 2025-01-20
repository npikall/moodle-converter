# from icecream import ic


def remove_whitespaces(formula: str) -> str:
    return formula.replace(" ", "")


def set_power_operator(formula: str) -> str:
    return formula.replace("**", "^")


def set_scientific_notation(token: str) -> str:
    mantissa, exponent = token.split("e")
    # test if mantissa and exponent are integers
    if mantissa.isdigit() and exponent.isdigit():
        return f"{mantissa} * pow(10, {exponent})"
    else:
        return token


def tokens_to_power_operator(tokens: list[str]) -> list[str]:
    for idx, token in enumerate(tokens):
        if "e" in token:
            tokens[idx] = set_scientific_notation(token)
    return tokens


def construct_power(power: str) -> str:
    """
    Convert a power operation 'base^exponent' into 'pow(base, exponent)'.
    """
    base, exponent = power.split("^", 1)
    return f"pow({base}, {exponent})"


def token_to_power_operator(tokens: list[str]) -> list[str]:
    for idx, token in enumerate(tokens):
        if "^" in token:
            tokens[idx] = construct_power(token)
    return tokens


def harmonize_whitespaces(
    formula: str, ops: list[str] = ["+", "-", "*", "/"]
) -> str:
    formula = formula.replace(" ", "")  # Remove all spaces
    # Add spaces around operators
    for op in ops:
        formula = formula.replace(op, f" {op} ")
    return formula


def remove_package_prefixes(
    formula: str, pkgs: list[str] = ["math", "np", "sp"]
) -> str:
    for pkg in pkgs:
        formula = formula.replace(f"{pkg}.", "")
    return formula


def tokenize_formula(formula: str) -> list[str]:
    return formula.split(" ")


def untokenize_formula(tokens: list[str]) -> str:
    formula = " ".join(tokens)
    formula = formula.replace(" ", "")
    return formula


def swap_variables(tokens: str, variable_map: dict[str, str]) -> str:
    for var, mvar in variable_map.items():
        for idx, token in enumerate(tokens):
            if token == var:  # Replace only exact matches
                tokens[idx] = f"{{{mvar}}}"
    return tokens


def swap_constants(tokens: str, constants_map: dict[str, str]) -> str:
    for const, mconst in constants_map.items():
        for idx, token in enumerate(tokens):
            if token == const:  # Replace only exact matches
                mconst = mconst.replace("_", "")  # Remove underscores
                if "e" in mconst:  # Handle scientific notation
                    mantissa, exponent = mconst.split("e")
                    mconst = f"{mantissa} * pow(10, {exponent})"
                tokens[idx] = (
                    mconst  # Replace the token with the formatted constant
                )
    return tokens


def python_to_moodle(
    formula: str,
    variable_map: dict[str, str] = None,
    constants_map: dict[str, str] = None,
) -> str:
    # Preprocess formula
    mformula = remove_whitespaces(formula)
    mformula = set_power_operator(mformula)
    mformula = remove_package_prefixes(mformula)

    # Tokenize, convert to scientific notation and untokenize
    mformula = harmonize_whitespaces(
        mformula, ops=["+", "-", "*", "/", "(", ")"]
    )
    mformula = tokenize_formula(mformula)
    mformula = tokens_to_power_operator(mformula)
    mformula = token_to_power_operator(mformula)
    mformula = untokenize_formula(mformula)

    # Tokenize, replace variables and constants and untokenize
    mformula = harmonize_whitespaces(
        mformula, ops=["+", "-", "*", "/", "(", ")", ","]
    )
    mformula = tokenize_formula(mformula)
    if variable_map:
        mformula = swap_variables(mformula, variable_map)
    if constants_map:
        mformula = swap_constants(mformula, constants_map)

    mformula = untokenize_formula(mformula)
    return mformula
