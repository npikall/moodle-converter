import moodleconverter.converter as mc
import pytest  # noqa


def test_removeWhitespaces():
    mock_input = "  a + b  "
    expected_output = "a+b"
    assert mc.remove_whitespaces(mock_input) == expected_output


def test_setPowerOperator():
    mock_input = "x**2"
    expected_output = "x^2"
    assert mc.set_power_operator(mock_input) == expected_output


def test_setScientificNotation():
    mock_input = "1e2"
    expected_output = "1 * pow(10, 2)"
    assert mc.set_scientific_notation(mock_input) == expected_output


def test_tokensToPowerOperator():
    mock_input = ["1e2", "x^2", "test"]
    expected_output = ["1 * pow(10, 2)", "x^2", "test"]
    assert mc.tokens_to_power_operator(mock_input) == expected_output


def test_constructPower():
    mock_input = "base^exponent"
    expected_output = "pow(base, exponent)"
    assert mc.construct_power(mock_input) == expected_output


def test_harmonizeWhitespaces():
    mock_input = " (a + b) / (x**2)"
    expected_output = "(a + b) / (x *  * 2)"
    assert mc.harmonize_whitespaces(mock_input) == expected_output


def test_removePackagePrefixes():
    mock_input = "math.sqrt(x) + np.log(y)"
    expected_output = "sqrt(x) + log(y)"

    assert (
        mc.remove_package_prefixes(mock_input, ["math", "np"])
        == expected_output
    )


def test_tokenizeFormula():
    mock_input = "a + b"
    invalid_input = "a+b"
    expected_output = ["a", "+", "b"]
    assert mc.tokenize_formula(mock_input) == expected_output
    assert mc.tokenize_formula(invalid_input) != expected_output


def test_untokenizeFormula():
    mock_input = ["a", "+", "b"]
    expected_output = "a+b"
    assert mc.untokenize_formula(mock_input) == expected_output


def test_tokenToPowerOperator():
    mock_input = ["a", "+", "b", "x^y"]
    expected_output = ["a", "+", "b", "pow(x, y)"]
    assert mc.token_to_power_operator(mock_input) == expected_output


def test_swapVariables():
    mock_input = ["rho", "v", "t"]
    variables_map = {"rho": "x"}
    expected_output = ["{x}", "v", "t"]
    assert mc.swap_variables(mock_input, variables_map) == expected_output


def test_swapConstants():
    mock_input = ["rho", "v", "t"]
    constants_map = {"rho": "123"}
    expected_output = ["123", "v", "t"]
    assert mc.swap_constants(mock_input, constants_map) == expected_output


def test_pythonToMoodle():
    mock_input = "rho * (ds**2/(4 * rs**2)) *(((2 * h * c**2)/(lam**5)) / (math.exp((h * c)/(lam * k * T)) - 1)) * 1e24"
    constants_map = {
        "h": "6.626e-34",
        "c": "299_792_458",
        "lam": "1",
        "k": "1.381e-23",
    }
    variable_map = {
        "rho": "rho",
        "ds": "ds",
        "rs": "rs",
        "T": "T",
    }
    expected_output = "{rho}*(pow({ds},2)/(4*pow({rs},2)))*(((2*6.626*pow(10,-34)*pow(299792458,2))/(pow(1,5)))/(exp((6.626*pow(10,-34)*299792458)/(1*1.381*pow(10,-23)*{T}))-1))*1*pow(10,24)"
    assert (
        mc.python_to_moodle(mock_input, variable_map, constants_map)
        == expected_output
    )
