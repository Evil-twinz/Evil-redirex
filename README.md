# Evil-redirex

![evilredirex](https://github.com/user-attachments/assets/f7b9b9d0-d3e5-4d91-b5d6-820d85746d28)

EvilRedirex is a Python tool for detecting open redirects and XSS vulnerabilities in web applications. It automates vulnerability scanning by testing URLs with various payloads to identify exploitable parameters.
Features

    1.Open Redirect Detection: Identifies URLs vulnerable to open redirects.
    2.XSS Vulnerability Detection: Detects parameters susceptible to cross-site scripting (XSS) attacks.
    3.Threaded Scanning: Processes multiple tests simultaneously for faster results.
    4.Selenium Integration: Uses a headless browser for advanced vulnerability detection.

Installation

    pip install evilredirex

Usage
Command-Line Options
 evilredirex --help

Example Usage:

    1.Test a single URL:
            evilredirex -u "http://example.com"
            
    2.Test URLs from a file:
            cat urls.txt | evilredirex
            
    3.Silent mode:
            evilredirex -u "http://example.com" --silent

Requirements

Ensure the following are installed on your system:

    Python 3.6+
    ChromeDriver
    Required Python libraries (automatically installed with pip install evilredirex).
