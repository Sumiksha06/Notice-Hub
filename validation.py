def validate_email(email):
    """
    Validates if the email is a valid Gmail address ending with @gmail.com.
    """
    # Simple check for @gmail.com suffix
    if not email.lower().endswith("@gmail.com"):
        return False, "Email must be a valid Gmail address (ending with @gmail.com)."
    
    # Check if there is a prefix before @gmail.com
    prefix = email.split('@')[0]
    if not prefix:
        return False, "Invalid Gmail address format."
    
    return True, ""

def validate_password(password):
    """
    Validates if the password is at least 6 characters long and 
    contains only letters and numbers (no special characters).
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    
    if not password.isalnum():
        return False, "Password should contain only letters and numbers (no special characters)."
    
    return True, ""
