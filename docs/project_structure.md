
## Project Structure

The project is structured as follows:

- **red_office_google_integration**: All components are contained within this package.

  - **google-service**: This package manages credentials, generates tokens, and securely stores credentials in an encrypted file using a Fernet key. The package provides a `Cred` object when requested, allowing actions to be performed on it.

  - **calendar**: Contains methods for managing calendar events, such as creating, listing, deleting, and getting events.

  - **log**: Configuration file for logging settings.

  - **src**: Contains utility functions and project settings.

  - **tests**: Contains test cases.

  - **CLI_handler**: Directory containing CLI modules for calendar, sheet, and Gmail. These modules are imported into `main.py`, which handles arguments and performs operations based on the command type. For example, `py main.py calendar ...` is used to interact with the calendar module.

- **main.py**: The main entry point for the project. It interacts with the project through the CLI. `main.py` takes arguments via the CLI and calls the corresponding CLI packages based on the command type. It does not contain all commands but rather delegates them to the relevant modules, such as calendar. For example, `py main.py calendar ...` would be used to interact with the calendar CLI package.

- **Docs**: Contains documentation files. The documentation is built using MkDocs. File references and configurations are specified in `mkdocs.yml`. Running `mkdocs serve` in the base directory fetches all mentioned files, extracts docstrings, and presents them beautifully in localhost. HTML documentation files can also be generated if needed.

---
