import math
from .tools import VariantSupport, SmartType
from .base_node import NODE_POSTFIX, ArithmeticNode, BooleanNode, ConversionNode, UtilityNode, ConstantsNode, PrimitiveNode

# Create a NUMBER type that accepts both INT and FLOAT
NUMBER = SmartType("INT,FLOAT")

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
    RETURN_NAMES = ("value",)
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
    RETURN_NAMES = ("value",)
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
    RETURN_NAMES = ("value",)
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
    RETURN_NAMES = ("value",)
    FUNCTION = "output"

    def output(self, value):
        return (value,)

@VariantSupport()
class IntToType(ConversionNode):
    """
    Convert an integer to various types.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("INT", {"default": 0, "min": -0xffffffffffffffff, "max": 0xffffffffffffffff, "step": 1}),
                "output_type": (["INT", "FLOAT", "STRING", "BOOLEAN"],),
            },
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("value",)
    FUNCTION = "convert"

    def convert(self, value, output_type):
        if output_type == "INT":
            return (value,)
        elif output_type == "FLOAT":
            return (float(value),)
        elif output_type == "STRING":
            return (str(value),)
        elif output_type == "BOOLEAN":
            return (bool(value),)

@VariantSupport()
class FloatToType(ConversionNode):
    """
    Convert a float to various types.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0, "min": -999999999999.0, "max": 999999999999.0, "step": 0.001}),
                "output_type": (["INT", "FLOAT", "STRING", "BOOLEAN"],),
            },
            "optional": {
                "round_method": (["round", "floor", "ceil", "trunc"], {"default": "round"}),
            },
        }

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("value",)
    FUNCTION = "convert"

    def convert(self, value, output_type, round_method="round"):
        if output_type == "INT":
            if round_method == "round":
                return (round(value),)
            elif round_method == "floor":
                return (math.floor(value),)
            elif round_method == "ceil":
                return (math.ceil(value),)
            elif round_method == "trunc":
                return (math.trunc(value),)
        elif output_type == "FLOAT":
            return (value,)
        elif output_type == "STRING":
            return (str(value),)
        elif output_type == "BOOLEAN":
            return (bool(value),)

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

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("result",)
    FUNCTION = "calculate"

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
    RETURN_NAMES = ("result",)
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

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("result",)
    FUNCTION = "calculate"

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
    RETURN_NAMES = ("value",)
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

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("rounded",)
    FUNCTION = "round_number"

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

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("clamped",)
    FUNCTION = "clamp"

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

    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("result",)
    FUNCTION = "lerp"

    def lerp(self, a, b, t):
        result = a + t * (b - a)
        # Lerp usually returns float due to multiplication
        # Only return int if result is whole number and inputs were int
        if all(isinstance(x, int) for x in [a, b, t]) and result == int(result):
            return (int(result),)
        else:
            return (float(result),)

@VariantSupport()
class NumberRange(UtilityNode):
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
    RETURN_NAMES = ("in_range",)
    FUNCTION = "check_range"

    def check_range(self, value, min_value, max_value, inclusive):
        if inclusive:
            return (min_value <= value <= max_value,)
        else:
            return (min_value < value < max_value,)

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
    RETURN_NAMES = ("result",)
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
    RETURN_NAMES = ("result",)
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
    "IntToType": IntToType,
    "FloatToType": FloatToType,
    "BasicMath": BasicMath,
    "IntMath": IntMath,
    "UnaryMath": UnaryMath,
    "MathConstants": MathConstants,
    "NumberRound": NumberRound,
    "NumberClamp": NumberClamp,
    "NumberLerp": NumberLerp,
    "NumberRange": NumberRange,
    "BooleanLogic": BooleanLogic,
    "BooleanUnary": BooleanUnary,
}

MATH_NODE_DISPLAY_NAME_MAPPINGS = {
    "IntegerInput": f"Integer {NODE_POSTFIX}",
    "FloatInput": f"Float {NODE_POSTFIX}",
    "PreciseFloatInput": f"Precise Float {NODE_POSTFIX}",
    "BooleanInput": f"Boolean {NODE_POSTFIX}",
    "IntToType": f"Int to Type {NODE_POSTFIX}",
    "FloatToType": f"Float to Type {NODE_POSTFIX}",
    "BasicMath": f"Basic Math {NODE_POSTFIX}",
    "IntMath": f"Int Math {NODE_POSTFIX}",
    "UnaryMath": f"Unary Math {NODE_POSTFIX}",
    "MathConstants": f"Math Constants {NODE_POSTFIX}",
    "NumberRound": f"Number Round {NODE_POSTFIX}",
    "NumberClamp": f"Number Clamp {NODE_POSTFIX}",
    "NumberLerp": f"Number Lerp {NODE_POSTFIX}",
    "NumberRange": f"Number Range {NODE_POSTFIX}",
    "BooleanLogic": f"Boolean Logic {NODE_POSTFIX}",
    "BooleanUnary": f"Boolean Unary {NODE_POSTFIX}",
}