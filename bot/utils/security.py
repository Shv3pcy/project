"""Security module for SysBmi_Bot

Contains security-related utilities including injection protection.

t.me/SysBmi_Bot
"""

# List of potentially dangerous Python functions and modules that could be used for code injection
INJECTIONS_LIST = [
    # System access
    "eval", "exec", "__import__", 
    "os", "sys", "subprocess", "system", "open", 
    
    # Process management
    "startfile", "start", "call", 
    "popen", "popen2", "popen3", "popen4",
    "spawn", "spawnl", "spawnle", "spawnlp", "spawnlpe",
    "spawnv", "spawnve", "spawnvp", "spawnvpe",
    "execl", "execle", "execlp", "execlpe",
    "execv", "execve", "execvp", "execvpe",
    
    # Process control
    "fork", "forkpty", "waitpid", "wait", "wait3", "wait4", "waitid",
    "kill", "killpg", "abort",
    
    # File operations
    "open", "file", "fileinput", "fileno", "input", "read", "write",
    
    # Network operations
    "socket", "socketserver", "ssl", "requests", "urllib",
    
    # Database access
    "sqlite3", "mysql", "psycopg2", "pymongo",
    
    # Other potentially dangerous operations
    "pickle", "marshal", "shelve", "glob", "shutil"
]


def check_for_injections(text):
    """Check if text contains any potential code injection attempts
    
    Args:
        text (str): Text to check for injections
        
    Returns:
        bool: True if injection attempt detected, False otherwise
    """
    for injection in INJECTIONS_LIST:
        if injection in text:
            return True
    return False