import os 

def get_application_root_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

path_input = f"{get_application_root_path()}\input"
path_output = f"{get_application_root_path()}\output"

ext_scripts = [
    ".py", ".pyo", ".pyw", ".pyz",  # Python
    ".js", ".mjs", ".cjs",                 # JavaScript
    ".java", ".class", ".jar",             # Java
    ".c", ".h",                            # C
    ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx",  # C++
    ".cs",                                 # C#
    ".go",                                 # Go
    ".rs",                                 # Rust
    ".rb",                                 # Ruby
    ".php", ".phtml", ".phar",             # PHP
    ".pl", ".pm", ".t",                    # Perl
    ".swift",                              # Swift
    ".kt", ".kts",                         # Kotlin
    ".sh", ".bash", ".zsh", ".ksh",        # Shell Scripts
    ".html", ".htm", ".xhtml",             # HTML
    ".css"                                 # CSS
]