# Quickstart: Google Sheet Service Account Prompt

## Prerequisites

- You must have a Google Cloud Project with a Service Account created.
- You should know the email address associated with your Service Account.

## Setup

1. Open your `.env` file in the root of the project.
2. Add the following line to configure your Service Account email:

```bash
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-service-account-email@your-project-id.iam.gserviceaccount.com
```

3. Start the bot as usual:

```bash
uv run cli bot run
```

4. When users initiate the onboarding process (e.g. by using the `/start` command), they will now receive instructions explicitly telling them to add your configured email as an "Editor" to their Google Sheet.
