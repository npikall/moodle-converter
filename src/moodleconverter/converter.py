from icecream import ic

def construct_power(power: str) -> str:
    """
    Convert a power operation 'base^exponent' into 'pow(base, exponent)'.
    """
    base, exponent = power.split("^", 1)
    return f"pow({base}, {exponent})"

def handle_power_operators(tokens: list[str]) -> list[str]:
    for idx, token in enumerate(tokens):
        if "^" in token:
            tokens[idx] = construct_power(token)
    return tokens

def harmonize_whitespaces(formula: str, ops: list[str] = ["+", "-", "*", "/"]) -> str:
    formula = formula.replace(" ", "")  # Remove all spaces
    # Add spaces around operators
    for op in ops:
        formula = formula.replace(op, f" {op} ")
    return formula

def remove_package_prefixes(formula: str, pkgs: list[str]) -> str:
    for pkg in pkgs:
        formula = formula.replace(f"{pkg}.", "")
    return formula

def tokenize_formula(formula: str) -> list[str]:
    return formula.split(" ")

def untokenize_formula(tokens: list[str]) -> str:
    return " ".join(tokens)


def python_to_moodle(
    formula: str,
    variable_map: dict[str, str] = None,
    constants_map: dict[str, str] = None,
) -> str:
    """
    Convert a Python formula into a Moodle-compatible formula.

    Parameters:
    - formula (str): The Python formula to convert.
    - variable_map (dict): Mapping of variable names to Moodle variables.
    - constants_map (dict): Mapping of constants to their Moodle equivalents.

    Returns:
    - str: The Moodle-compatible formula.
    """
    # Step 1: Preprocess the formula
    mformula = formula.replace("**", "^")  # Replace power operator
    mformula = harmonize_whitespaces(mformula)
    mformula = remove_package_prefixes(mformula, ["math", "np"])

    tokens = tokenize_formula(mformula)

    # Step 2: Handle power operators
    tokens = handle_power_operators(tokens)

    mformula = untokenize_formula(tokens)
    mformula = harmonize_whitespaces(mformula, ["+", "-", "*", "/", "(", ")", ","])
    tokens = tokenize_formula(mformula)
    
    # Step 3: Replace variables with Moodle syntax
    if variable_map:
        for var, mvar in variable_map.items():
            for idx, token in enumerate(tokens):
                if token == var:  # Replace only exact matches
                    tokens[idx] = f"{{{mvar}}}"

    # Step 4: Replace constants with integer or scientific values
    if constants_map:
        for const, mconst in constants_map.items():
            for idx, token in enumerate(tokens):
                if token == const:  # Replace only exact matches
                    mconst = mconst.replace("_", "")  # Remove underscores
                    if "e" in mconst:  # Handle scientific notation
                        mantissa, exponent = mconst.split("e")
                        mconst = f"{mantissa} * pow(10, {exponent})"
                    tokens[idx] = mconst  # Replace the token with the formatted constant

    # Step 5: Reconstruct the formula
    mformula = " ".join(tokens)
    mformula = mformula.replace("_", "")  # Remove any stray underscores

    # Step 6: 
    mformula = mformula.replace(" ", "")  # Remove all spaces
    for op in ["+", "-", "*", "/"]:
        mformula = mformula.replace(op, f" {op} ")
    return mformula