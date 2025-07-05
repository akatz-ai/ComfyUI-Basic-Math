
class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""
    def __ne__(self, __value: object) -> bool:
        return False

class ByPassTypeTuple(tuple):
    """A special class that will return additional "AnyType" strings beyond defined values.
    Credit to Trung0246
    """
    def __getitem__(self, index):
        if index > len(self) - 1:
            return AnyType("*")
        return super().__getitem__(index)

def MakeSmartType(t):
    if isinstance(t, str):
        return SmartType(t)
    return t

class SmartType(str):
    def __ne__(self, other):
        if self == "*" or other == "*":
            return False
        selfset = set(self.split(','))
        otherset = set(other.split(','))
        return not selfset.issubset(otherset)

def VariantSupport():
    def decorator(cls):
        if hasattr(cls, "INPUT_TYPES"):
            old_input_types = getattr(cls, "INPUT_TYPES")
            def new_input_types(*args, **kwargs):
                types = old_input_types(*args, **kwargs)
                for category in ["required", "optional"]:
                    if category not in types:
                        continue
                    for key, value in types[category].items():
                        if isinstance(value, tuple):
                            types[category][key] = (MakeSmartType(value[0]),) + value[1:]
                return types
            setattr(cls, "INPUT_TYPES", new_input_types)
        if hasattr(cls, "RETURN_TYPES"):
            old_return_types = cls.RETURN_TYPES
            setattr(cls, "RETURN_TYPES", tuple(MakeSmartType(x) for x in old_return_types))
        if hasattr(cls, "VALIDATE_INPUTS"):
            # Reflection is used to determine what the function signature is, so we can't just change the function signature
            raise NotImplementedError("VariantSupport does not support VALIDATE_INPUTS yet")
        else:
            def validate_individual(input_types, inputs):
                for key, value in input_types.items():
                    if isinstance(value, SmartType):
                        continue
                    if "required" in inputs and key in inputs["required"]:
                        expected_type = inputs["required"][key][0]
                    elif "optional" in inputs and key in inputs["optional"]:
                        expected_type = inputs["optional"][key][0]
                    else:
                        expected_type = None
                    if expected_type is not None and MakeSmartType(value) != expected_type:
                        return f"Invalid type of {key}: {value} (expected {expected_type})"
                return True
            def validate_inputs(input_types):
                inputs = cls.INPUT_TYPES()

                if not isinstance(input_types, list):
                    return validate_individual(input_types, inputs)

                for input_type in input_types:
                    response = validate_individual(input_type, inputs)
                    if isinstance(response, str):
                        return response

                return True
                
            setattr(cls, "VALIDATE_INPUTS", validate_inputs)
        return cls
    return decorator

# Create a global any_type instance for use in nodes
any_type = AnyType("*")

