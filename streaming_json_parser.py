class StreamingJsonParser:
    """
    A streaming JSON parser that processes JSON data incrementally.
    
    This parser handles a subset of JSON, where values consist solely of strings and objects.
    It can return the current state of the parsed JSON object at any point, even with incomplete data.
    String values can be partially returned, but keys are only included once their value type is determined.
    
    Note: This implementation assumes:
    - Only strings and objects are supported (no arrays, numbers, booleans, or null)
    - Escape sequences in strings aren't handled
    - Duplicate keys aren't supported
    """
    
    def __init__(self):
        """Initialize the parser with empty state."""
        self.buffer = ""
        self.result = {}
        self.state_stack = [self.result]  # Start with root object on stack
        self.current_key = None
        self.is_parsing_key = False
        self.is_parsing_string = False
        self.partial_string = ""
        
    def consume(self, buffer: str):
        """
        Consume a chunk of JSON data.
        
        Args:
            buffer: A string containing a chunk of JSON data.
        """
        self.buffer += buffer
        self._parse()
        
    def get(self):
        """
        Return the current state of the parsed JSON object.
        
        Returns:
            A Python dict representing the current state of the parsed JSON.
        """
        return self.result
        
    def _parse(self):
        """Parse the current buffer and update the internal state."""
        i = 0
        while i < len(self.buffer):
            char = self.buffer[i]
            
            # Handle string parsing
            if self.is_parsing_string:
                # Simple check for quote - the requirements mention escape sequences aren't expected
                if char == '"' and (i == 0 or self.buffer[i-1] != '\\'):
                    self.is_parsing_string = False
                    
                    if self.is_parsing_key:
                        self.current_key = self.partial_string
                        self.is_parsing_key = False
                        self.partial_string = ""
                    else:
                        # Add key-value pair to current object
                        self._add_to_current_object(self.current_key, self.partial_string)
                        self.current_key = None
                        self.partial_string = ""
                else:
                    self.partial_string += char
                i += 1
                continue
            
            # Handle object start
            if char == '{':
                if i == 0 or (self.current_key is None and len(self.state_stack) == 1):
                    # Root object - already on stack
                    i += 1
                    continue
                
                # Nested object
                new_obj = {}
                if self.current_key is not None:
                    self._add_to_current_object(self.current_key, new_obj)
                    self.state_stack.append(new_obj)
                    self.current_key = None
                i += 1
                continue
            
            # Handle object end
            if char == '}':
                if len(self.state_stack) > 1:
                    self.state_stack.pop()
                i += 1
                continue
                
            # Handle key start
            if char == '"' and not self.is_parsing_string:
                self.is_parsing_string = True
                if self.current_key is None:
                    self.is_parsing_key = True
                    self.partial_string = ""
                else:
                    self.partial_string = ""
                i += 1
                continue
                
            # Skip whitespace and separators
            if char in [' ', '\t', '\n', '\r', ':', ',']:
                i += 1
                continue
                
            i += 1
        
        # Handle partial string values at the end of buffer
        if self.is_parsing_string and not self.is_parsing_key and self.current_key is not None:
            self._add_to_current_object(self.current_key, self.partial_string)
        
        # Clear processed buffer
        # In a production environment, we might want to keep unprocessed data
        # but for this challenge's scope, clearing is fine
        self.buffer = ""
        
    def _add_to_current_object(self, key, value):
        """
        Add a key-value pair to the current object in the state stack.
        
        Args:
            key: The key string
            value: The value to add (string or dict)
        """
        current_obj = self.state_stack[-1]
        current_obj[key] = value