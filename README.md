# Email Reminder Scheduler

A Python-based scheduler that sends automated email reminders for visa appointments and residence permit expirations.

## Overview

This application monitors upcoming visa appointments and residence permit expiration dates, sending email reminders at exactly 3, 2, and 1 months before the target dates. It runs daily at a specified time (default: 8 AM) to check and send necessary reminders. The application is designed to run as a background service.

## Features

- Automated daily checks for upcoming deadlines
- Email reminders sent at 3, 2, and 1 months before target dates
- Handles both visa appointments and residence permit expiration reminders
- Robust scheduling system with fail-safe mechanisms
- Detailed logging for monitoring and debugging

## Requirements

- Python 3.10+

## Installation

1. Clone the repository
```bash
git clone <repository-url>
```

2. Install dependencies:
- with `uv`:
    - run `uv sync` to install packages and setup the environment.
- with pip:
    - Setup and activate `venv` (Optional, but recommended)
        - run `python -m venv .venv`
    - run `pip install -r requirements.txt`.

3. Configure environment variables:
    - Rename `.env.example` to `.env`
    - Update the `.env` file with your actual configuration data

## Configuration

The application requires the following configurations:

1. Database configuration for accessing reminder data
2. Email service configuration (Brevo API credentials)
3. Logging configuration
4. Scheduler timing settings (default: 8 AM daily)

## Usage

### Development
- with `uv` 
```bash
uv run main.py
```
- with python directly
```bash
python main.py
```

### Deployment
Run as a background service using systemd (see [Running](#running) section)

The scheduler will:
- Run continuously
- Check for reminders daily at the configured time
- Send email reminders when appropriate
- Log all activities

## Logging

The application maintains detailed logs including:
- Scheduler start/stop events
- Task execution details
- Email sending status
- Error messages and exceptions

## Running

1.  Create a systemd service file at `/etc/systemd/system/vf-email-scheduler.service`. Use the following config as a starting point. Replace relevant parts with actual data.

```bash
[Unit]
Description=Visaflow Email reminders for Visa and Residence Permit
After=network.target
After=nss-user-lookup.target

[Service]
User=your_user
Group=your_user
WorkingDirectory=/path/to/your/script
Environment=PYTHONPATH=/path/to/your/script
EnvironmentFile=/path/to/your/script/.env
ExecStart=/path/to/your/script/.venv/bin/python3 /path/to/your/script/main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```