# Discord Bot for HumanTech Center

This repository contains the code for a Discord bot developed for the HumanTech Center.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/humantech-discord-bot.git
   cd humantech-discord-bot
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory of the project.
2. Add your Discord bot token to the `.env` file:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

## Running the Bot

To start the bot, run the following command:
python main.py