# Ticket AI

## Overview

This project is designed to monitor an email inbox, parse incoming emails, and generate tickets based on the email content using OpenAI's API. The project utilizes several Python libraries and modules to achieve this functionality.

## Requirements

The project dependencies are listed in the `requirements.txt` file. To install them, run:

```sh
pip install -r requirements.txt
```

## Project Structure

- `main.py`: The entry point of the application.
- `mail/`: Contains modules related to email handling.
    - `email_client.py`: Manages the connection to the email server and fetching emails.
    - `email_monitor.py`: Monitors the inbox for new emails.
    - `email_parser.py`: Parses the email content.
- `ai/`: Contains modules related to AI processing.
    - `open_ai_client.py`: Interacts with the OpenAI API to interpret email content.
- `ticket/`: Contains modules related to ticket management.
    - `ticket_manager.py`: Manages the creation of tickets from email content.
- `utils/`: Contains utility modules.
    - `excel_util.py`: Handles Excel file operations.

## Usage

1. **Environment Setup**: Create a `.env` file in the root directory with the following variables:
    
   ```env
    IMAP_SERVER=<your_imap_server>
    EMAIL_ACCOUNT=<your_email_account>
    EMAIL_PASSWORD=<your_email_password>
    OPENAI_API_KEY=<your_openai_api_key>
    OPENAI_API_VERSION=<your_openai_api_version>
    OPENAI_API_BASE=<your_openai_api_base>
    OPENAI_GPT35TURBO_MODEL=<your_openai_model>
    ```

2. **Running the Application**: Execute the `main.py` file to start the email monitoring and ticket generation process.
    
   ```sh
    python main.py
    ```
