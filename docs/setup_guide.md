## SETUP

1. **Setup Python 3.10:**
   Ensure you have Python 3.10 installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Clone the Repository:**
   Use the following command to clone the repository:
   ```shell
   git clone https://github.com/TechSage369/RED-OFFICE-GOOGLE-INTEGRATION.git
   ```

3. **Install Dependencies:**
   ```shell
   pip install -r requirement.txt
   ```
4. **CLI Commands:**
Here's the corrected version of the CLI commands section in Markdown format:


# Initialize Credentials

please follow this link till credential creation and save to json file

[Python quickstart  |  Google Calendar  |  Google for Developers](https://developers.google.com/calendar/api/quickstart/python)


`After getting credential`

---

## Setup Credentials

To initialize your credentials, provide the credential file name. You will receive the key in the terminal (also can specify output file[optional]), which you should keep safe for later use as API_KEY.

```bash
py main.py init-cred credential_filename -o outputfilename
```

You can also use optional parameters to specify a custom key (e.g., `Lb-9cbIFCUCFcKSrWqRyEvEYuHAOB6pfMLpmHbrdnNA=`) and mention the output file path to save the key. `Fernet key 128-bit base64-encoded `

```bash
py main.py init-cred credential_filename -o outputfilename -k YOUR_SECRET_KEY
```

Make sure to replace `credential_filename` with the name of your credential file and `outputfilename` with the desired output file path.

