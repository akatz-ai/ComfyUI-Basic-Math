NODE_NAME = "Basic Math ➕"  # Can be changed to any desired prefix

NODE_POSTFIX = "| Basic"

# Base class for all nodes
class BaseNode:
    CATEGORY = NODE_NAME
    
    @classmethod
    def get_category(cls):
        return cls.CATEGORY
    
class PrimitiveNode(BaseNode):
    CATEGORY = f"{NODE_NAME}/Primitives"
    
class ArithmeticNode(BaseNode):
    CATEGORY = f"{NODE_NAME}/Arithmetic"
    
class BooleanNode(BaseNode):
    CATEGORY = f"{NODE_NAME}/Boolean"
    
class ConversionNode(BaseNode):
    CATEGORY = f"{NODE_NAME}/Conversion"
    
class UtilityNode(BaseNode):
    CATEGORY = f"{NODE_NAME}/Utility"
    
class ConstantsNode(BaseNode):
    CATEGORY = f"{NODE_NAME}/Constants"
    
class DebugNode(BaseNode):
    CATEGORY = f"{NODE_NAME}/Debug"
    
    