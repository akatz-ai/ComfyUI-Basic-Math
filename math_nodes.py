import math
import re
from .tools import VariantSupport, SmartType, ByPassTypeTuple, any_type
from .base_node import NODE_POSTFIX, ArithmeticNode, BooleanNode, ConversionNode, UtilityNode, ConstantsNode, PrimitiveNode

# Create a NUMBER type that accepts both INT and FLOAT
NUMBER = SmartType("INT,FLOAT")
ANY=SmartType("INT,FLOAT,STRING,BOOLEAN")

@VariantSupport()
class IntegerInput(PrimitiveNode):
    """
    Output an integer value.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff, "step": 1}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("INT",)
    FUNCTION = "output"

    def output(self, value):
        return (value,)

@VariantSupport()
class FloatInput(PrimitiveNode):
    """
    Output a float value.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0, "min": -999999999999.0, "max": 999999999999.0, "step": 0.001}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("FLOAT",)
    FUNCTION = "output"

    def output(self, value):
        return (value,)
      
@VariantSupport()
class PreciseFloatInput(PrimitiveNode):
    """
    Output a precise float value.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0, "min": -999999999999.0, "max": 999999999999.0, "step": 0.0000000001}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("FLOAT",)
    FUNCTION = "output"

    def output(self, value):
        return (value,)

@VariantSupport()
class BooleanInput(PrimitiveNode):
    """
    Output a boolean value.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)
    FUNCTION = "output"

    def output(self, value):
        return (value,)

@VariantSupport()
class StringInput(PrimitiveNode):
    """
    Output a string value.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("STRING", {"default": "",}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "output"

    def output(self, value):
        return (value,)


@VariantSupport()
class ToInt(ConversionNode):
    """
    Convert any value to integer.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (any_type,),
            },
            "optional": {
                "round_method": (["round", "floor", "ceil", "trunc"], {"default": "round"}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("INT",)
    FUNCTION = "convert"

    def convert(self, any, round_method="round"):
        try:
            # Try to convert to float first, then to int
            if isinstance(any, (int, float)):
                float_val = float(any)
            else:
                float_val = float(str(any))
            
            if round_method == "round":
                return (round(float_val),)
            elif round_method == "floor":
                return (math.floor(float_val),)
            elif round_method == "ceil":
                return (math.ceil(float_val),)
            elif round_method == "trunc":
                return (math.trunc(float_val),)
        except:
            return (0,)

@VariantSupport()
class ToFloat(ConversionNode):
    """
    Convert any value to float.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (any_type,),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("FLOAT",)
    FUNCTION = "convert"

    def convert(self, any):
        try:
            if isinstance(any, (int, float)):
                return (float(any),)
            else:
                return (float(str(any)),)
        except:
            return (0.0,)

@VariantSupport()
class ToString(ConversionNode):
    """
    Convert any value to string.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (any_type,),   
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "convert"

    def convert(self, any):
        return (str(any),)

@VariantSupport()
class ToBool(ConversionNode):
    """
    Convert any value to boolean with optional invert.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (any_type,),
            },
            "optional": {
                "invert": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)
    FUNCTION = "convert"

    def convert(self, any, invert=False):
        try:
            result = bool(any)
        except:
            # If conversion fails, assume it's something (True)
            result = True

        if invert:
            result = not result

        return (result,)

@VariantSupport()
class BasicMath(ArithmeticNode):
    """
    Basic mathematical operations between two numbers.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": (NUMBER, {"default": 0.0}),
                "b": (NUMBER, {"default": 0.0}),
                "operation": (["+", "-", "*", "/", "//", "%", "**", "min", "max"],),
            },
        }

    RETURN_TYPES = (NUMBER,)
    RETURN_NAMES = ("NUMBER",)
    FUNCTION = "calculate"
    OUTPUT_IS_LIST = (False,)

    def calculate(self, a, b, operation):
        # Determine if we should return int or float based on input types and operation
        is_int_operation = isinstance(a, int) and isinstance(b, int) and operation != "/"
        
        try:
            if operation == "+":
                result = a + b
            elif operation == "-":
                result = a - b
            elif operation == "*":
                result = a * b
            elif operation == "/":
                if b == 0:
                    return (float('inf') if a > 0 else float('-inf'),)
                result = a / b
                is_int_operation = False  # Division always returns float
            elif operation == "//":
                if b == 0:
                    return (float('inf') if a > 0 else float('-inf'),)
                result = a // b
            elif operation == "%":
                if b == 0:
                    return (float('nan'),)
                result = a % b
            elif operation == "**":
                result = a ** b
                # Power can return float even with int inputs
                if not isinstance(result, int):
                    is_int_operation = False
            elif operation == "min":
                result = min(a, b)
            elif operation == "max":
                result = max(a, b)
            
            # Return as int if both inputs were int and operation preserves int type
            if is_int_operation and isinstance(result, (int, float)) and result == int(result):
                return (int(result),)
            else:
                return (float(result),)
        except:
            return (float('nan'),)

@VariantSupport()
class IntMath(ArithmeticNode):
    """
    Basic mathematical operations between two integers.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("INT", {"default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff, "step": 1}),
                "b": ("INT", {"default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff, "step": 1}),
                "operation": (["+", "-", "*", "//", "%", "**", "min", "max", "&", "|", "^", "<<", ">>"],),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("INT",)
    FUNCTION = "calculate"

    def calculate(self, a, b, operation):
        try:
            if operation == "+":
                return (a + b,)
            elif operation == "-":
                return (a - b,)
            elif operation == "*":
                return (a * b,)
            elif operation == "//":
                if b == 0:
                    return (0,)
                return (a // b,)
            elif operation == "%":
                if b == 0:
                    return (0,)
                return (a % b,)
            elif operation == "**":
                return (a ** b,)
            elif operation == "min":
                return (min(a, b),)
            elif operation == "max":
                return (max(a, b),)
            elif operation == "&":
                return (a & b,)
            elif operation == "|":
                return (a | b,)
            elif operation == "^":
                return (a ^ b,)
            elif operation == "<<":
                return (a << b,)
            elif operation == ">>":
                return (a >> b,)
        except:
            return (0,)

@VariantSupport()
class UnaryMath(ArithmeticNode):
    """
    Unary mathematical operations on a single number.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (NUMBER, {"default": 0.0}),
                "operation": (["abs", "neg", "sqrt", "sin", "cos", "tan", "log", "log10", "exp", "floor", "ceil", "round"],),
            },
        }

    RETURN_TYPES = (NUMBER,)
    RETURN_NAMES = ("NUMBER",)
    FUNCTION = "calculate"
    OUTPUT_IS_LIST = (False,)

    def calculate(self, value, operation):
        # Determine return type based on operation and input
        preserve_int = isinstance(value, int) and operation in ["abs", "neg"]
        
        try:
            if operation == "abs":
                result = abs(value)
            elif operation == "neg":
                result = -value
            elif operation == "sqrt":
                result = math.sqrt(abs(value))
                preserve_int = False
            elif operation == "sin":
                result = math.sin(value)
                preserve_int = False
            elif operation == "cos":
                result = math.cos(value)
                preserve_int = False
            elif operation == "tan":
                result = math.tan(value)
                preserve_int = False
            elif operation == "log":
                result = math.log(abs(value)) if value != 0 else float('-inf')
                preserve_int = False
            elif operation == "log10":
                result = math.log10(abs(value)) if value != 0 else float('-inf')
                preserve_int = False
            elif operation == "exp":
                result = math.exp(value)
                preserve_int = False
            elif operation == "floor":
                result = math.floor(value)
                preserve_int = isinstance(value, int)
            elif operation == "ceil":
                result = math.ceil(value)
                preserve_int = isinstance(value, int)
            elif operation == "round":
                result = round(value)
                preserve_int = isinstance(value, int)
            
            if preserve_int:
                return (int(result),)
            else:
                return (float(result),)
        except:
            return (float('nan'),)

@VariantSupport()
class MathConstants(ConstantsNode):
    """
    Common mathematical constants.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "constant": (["pi", "e", "tau", "inf", "nan"],),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("FLOAT",)
    FUNCTION = "get_constant"

    def get_constant(self, constant):
        if constant == "pi":
            return (math.pi,)
        elif constant == "e":
            return (math.e,)
        elif constant == "tau":
            return (math.tau,)
        elif constant == "inf":
            return (float('inf'),)
        elif constant == "nan":
            return (float('nan'),)

@VariantSupport()
class NumberRound(UtilityNode):
    """
    Round a number to specified decimal places.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (NUMBER, {"default": 0.0}),
                "decimals": ("INT", {"default": 2, "min": 0, "max": 10, "step": 1}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("FLOAT",)
    FUNCTION = "round_number"
    OUTPUT_IS_LIST = (False,)

    def round_number(self, value, decimals):
        result = round(value, decimals)
        # If input was int and decimals is 0, return int
        if isinstance(value, int) and decimals == 0:
            return (int(result),)
        else:
            return (float(result),)

@VariantSupport()
class NumberClamp(UtilityNode):
    """
    Clamp a number between minimum and maximum values.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (NUMBER, {"default": 0.0}),
                "min_value": (NUMBER, {"default": 0.0}),
                "max_value": (NUMBER, {"default": 1.0}),
            },
        }

    RETURN_TYPES = (NUMBER,)
    RETURN_NAMES = ("NUMBER",)
    FUNCTION = "clamp"
    OUTPUT_IS_LIST = (False,)

    def clamp(self, value, min_value, max_value):
        result = max(min_value, min(max_value, value))
        # If all inputs are int, return int
        if all(isinstance(x, int) for x in [value, min_value, max_value]):
            return (int(result),)
        else:
            return (float(result),)

@VariantSupport()
class NumberLerp(UtilityNode):
    """
    Linear interpolation between two values.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": (NUMBER, {"default": 0.0}),
                "b": (NUMBER, {"default": 1.0}),
                "t": (NUMBER, {"default": 0.5}),
            },
        }

    RETURN_TYPES = (NUMBER,)
    RETURN_NAMES = ("NUMBER",)
    FUNCTION = "lerp"
    OUTPUT_IS_LIST = (False,)

    def lerp(self, a, b, t):
        result = a + t * (b - a)
        # Lerp usually returns float due to multiplication
        # Only return int if result is whole number and inputs were int
        if all(isinstance(x, int) for x in [a, b, t]) and result == int(result):
            return (int(result),)
        else:
            return (float(result),)

@VariantSupport()
class NumberInRange(UtilityNode):
    """
    Check if a number is within a range.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": (NUMBER, {"default": 0.0}),
                "min_value": (NUMBER, {"default": 0.0}),
                "max_value": (NUMBER, {"default": 1.0}),
                "inclusive": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)
    FUNCTION = "check_range"

    def check_range(self, value, min_value, max_value, inclusive):
        if inclusive:
            return (min_value <= value <= max_value,)
        else:
            return (min_value < value < max_value,)

@VariantSupport()
class NumberComparison(BooleanNode):
    """
    Compare two numbers and return a boolean result.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": (NUMBER, {"default": 0.0}),
                "b": (NUMBER, {"default": 0.0}),
                "operation": (["==", "!=", "<", ">", "<=", ">="],),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)
    FUNCTION = "compare"

    def compare(self, a, b, operation):
        if operation == "==":
            return (a == b,)
        elif operation == "!=":
            return (a != b,)
        elif operation == "<":
            return (a < b,)
        elif operation == ">":
            return (a > b,)
        elif operation == "<=":
            return (a <= b,)
        elif operation == ">=":
            return (a >= b,)

@VariantSupport()
class IntegerComparison(BooleanNode):
    """
    Compare two integers and return a boolean result.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("INT", {"default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff, "step": 1}),
                "b": ("INT", {"default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff, "step": 1}),
                "operation": (["==", "!=", "<", ">", "<=", ">="],),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)
    FUNCTION = "compare"

    def compare(self, a, b, operation):
        if operation == "==":
            return (a == b,)
        elif operation == "!=":
            return (a != b,)
        elif operation == "<":
            return (a < b,)
        elif operation == ">":
            return (a > b,)
        elif operation == "<=":
            return (a <= b,)
        elif operation == ">=":
            return (a >= b,)

@VariantSupport()
class FloatComparison(BooleanNode):
    """
    Compare two floats and return a boolean result.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0, "min": -999999999999.0, "max": 999999999999.0, "step": 0.001}),
                "b": ("FLOAT", {"default": 0.0, "min": -999999999999.0, "max": 999999999999.0, "step": 0.001}),
                "operation": (["==", "!=", "<", ">", "<=", ">="],),
            },
            "optional": {
                "tolerance": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.0001}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)  
    FUNCTION = "compare"

    def compare(self, a, b, operation, tolerance=0.0):
        # Handle floating point comparison with optional tolerance
        if tolerance > 0 and operation in ["==", "!="]:
            equal = abs(a - b) <= tolerance
            if operation == "==":
                return (equal,)
            else:  # !=
                return (not equal,)
        
        if operation == "==":
            return (a == b,)
        elif operation == "!=":
            return (a != b,)
        elif operation == "<":
            return (a < b,)
        elif operation == ">":
            return (a > b,)
        elif operation == "<=":
            return (a <= b,)
        elif operation == ">=":
            return (a >= b,)

@VariantSupport()
class StringComparison(BooleanNode):
    """
    Compare and manipulate strings with various operations.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("STRING", {"multiline": False}),
                "b": ("STRING", {"multiline": False}),
                "operation": (["a == b", "a != b", "a IN b", "a MATCH REGEX(b)", "a BEGINSWITH b", "a ENDSWITH b"],),
                "case_sensitive": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)
    FUNCTION = "compare"

    def compare(self, a, b, operation, case_sensitive):
        if not case_sensitive:
            a = a.lower()
            b = b.lower()

        if operation == "a == b":
            return (a == b,)
        elif operation == "a != b":
            return (a != b,)
        elif operation == "a IN b":
            return (a in b,)
        elif operation == "a MATCH REGEX(b)":
            try:
                return (re.match(b, a) is not None,)
            except:
                return (False,)
        elif operation == "a BEGINSWITH b":
            return (a.startswith(b),)
        elif operation == "a ENDSWITH b":
            return (a.endswith(b),)

@VariantSupport()
class BooleanLogic(BooleanNode):
    """
    Boolean logic operations.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "a": ("BOOLEAN",),
                "b": ("BOOLEAN",),
                "operation": (["AND", "OR", "XOR", "NAND", "NOR", "XNOR"],),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)
    FUNCTION = "logic_operation"

    def logic_operation(self, a, b, operation):
        if operation == "AND":
            return (a and b,)
        elif operation == "OR":
            return (a or b,)
        elif operation == "XOR":
            return (a ^ b,)
        elif operation == "NAND":
            return (not (a and b),)
        elif operation == "NOR":
            return (not (a or b),)
        elif operation == "XNOR":
            return (not (a ^ b),)

@VariantSupport()
class BooleanUnary(BooleanNode):
    """
    Unary boolean operations.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("BOOLEAN",),
                "operation": (["NOT", "IDENTITY"],),
            },
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("BOOLEAN",)
    FUNCTION = "unary_operation"

    def unary_operation(self, value, operation):
        if operation == "NOT":
            return (not value,)
        elif operation == "IDENTITY":
            return (value,)

MATH_NODE_CLASS_MAPPINGS = {
    "IntegerInput": IntegerInput,
    "FloatInput": FloatInput,
    "PreciseFloatInput": PreciseFloatInput,
    "BooleanInput": BooleanInput,
    "StringInput": StringInput,
    "ToInt": ToInt,
    "ToFloat": ToFloat,
    "ToString": ToString,
    "ToBool": ToBool,
    "BasicMath": BasicMath,
    "IntMath": IntMath,
    "UnaryMath": UnaryMath,
    "MathConstants": MathConstants,
    "NumberRound": NumberRound,
    "NumberClamp": NumberClamp,
    "NumberLerp": NumberLerp,
    "NumberInRange": NumberInRange,
    "NumberComparison": NumberComparison,
    "IntegerComparison": IntegerComparison,
    "FloatComparison": FloatComparison,
    "StringComparison": StringComparison,
    "BooleanLogic": BooleanLogic,
    "BooleanUnary": BooleanUnary,
}

MATH_NODE_DISPLAY_NAME_MAPPINGS = {
    "IntegerInput": f"Integer {NODE_POSTFIX}",
    "FloatInput": f"Float {NODE_POSTFIX}",
    "PreciseFloatInput": f"Precise Float {NODE_POSTFIX}",
    "BooleanInput": f"Boolean {NODE_POSTFIX}",
    "StringInput": f"String {NODE_POSTFIX}",
    "ToInt": f"To Int {NODE_POSTFIX}",
    "ToFloat": f"To Float {NODE_POSTFIX}",
    "ToString": f"To String {NODE_POSTFIX}",
    "ToBool": f"To Bool {NODE_POSTFIX}",
    "BasicMath": f"Basic Math {NODE_POSTFIX}",
    "IntMath": f"Int Math {NODE_POSTFIX}",
    "UnaryMath": f"Unary Math {NODE_POSTFIX}",
    "MathConstants": f"Math Constants {NODE_POSTFIX}",
    "NumberRound": f"Number Round {NODE_POSTFIX}",
    "NumberClamp": f"Number Clamp {NODE_POSTFIX}",
    "NumberLerp": f"Number Lerp {NODE_POSTFIX}",
    "NumberInRange": f"Number In Range {NODE_POSTFIX}",
    "NumberComparison": f"Number Comparison {NODE_POSTFIX}",
    "IntegerComparison": f"Integer Comparison {NODE_POSTFIX}",
    "FloatComparison": f"Float Comparison {NODE_POSTFIX}",
    "StringComparison": f"String Comparison {NODE_POSTFIX}",
    "BooleanLogic": f"Boolean Logic {NODE_POSTFIX}",
    "BooleanUnary": f"Boolean Unary {NODE_POSTFIX}",
}