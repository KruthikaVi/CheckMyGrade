class TextSecurity:
    """This class with encrypt the test using Caesar cipher"""
    def __init__(self, shift):
        """COnstructor."""
        self.shifter=shift
        self.s=self.shifter%26
  
    def _convert(self, text,s):
        """return encrypted string."""
        result=""
        # text = text.strip()
        for ch in text:
            if ch.isalpha():
                if ch.isupper():
                    result += chr((ord(ch) + s - 65) % 26 + 65)
                else:
                    result += chr((ord(ch) + s - 97) % 26 + 97)
            elif ch.isdigit():
                result += chr((ord(ch) + s - 48) % 10 + 48)
            else:
                if 32 < ord(ch) < 127:  # Printable ASCII characters
                    result += chr((ord(ch) + s - 33) % 94 + 33)
                else:
                    result += ch
        return result
  
    def encrypt(self, text):
        """return encrypted string."""
        return self._convert(text,self.shifter)
        
    def decrypt(self, text):
        """return encrypted string."""
        return self._convert(text, -self.shifter) 

if __name__ == '__main__':
    cipher = TextSecurity(4)
    message = "Welcome%123"
    coded = cipher.encrypt(message)
    print('Secret: ', coded)
    answer = cipher.decrypt(coded)
    print('Message:', answer)