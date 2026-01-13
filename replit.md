# Discord Video Edit Bot

## Overview
A Discord bot that edits videos and photos. Users can send commands to the bot to process videos with various effects, concatenate videos, and download videos from URLs.

## Project Structure
- `discordBot.py` - Main bot entry point
- `combiner.py` - Video concatenation logic
- `func_helper.py` - Helper functions for task handling
- `config.json` - Bot configuration (from config.json.template)
- `editor/` - Video editing modules
  - `videoEditor.py` - Main video editor
  - `addSounds.py` - Sound effects
  - `captions.py` - Caption processing
  - `datamosh.py` - Datamosh effects
  - `download.py` - Video download functionality
  - `ytp.py` - YouTube Poop style effects
- `editor/sounds/` - Sound effect files
- `editor/fonts/` - Font files for captions
- `editor/images/` - Image assets (watermarks, etc.)

## Requirements
- Python 3.11+
- ffmpeg
- sox
- yt-dlp (installed via pip)

## Configuration
The bot requires a `DISCORD_TOKEN` secret to be set. The token is read from:
1. Environment variable `DISCORD_TOKEN` (preferred)
2. `config.json` file (`discord_token` field)

Other settings are configured in `config.json`:
- `working_directory` - Temp directory for processing
- `discord_tagline` - Bot status message
- `message_search_count` - How many messages to search for attachments
- `command_chain_limit` - Max command chain length
- `max_concat_count` - Max videos to concatenate

## Commands
See COMMANDS.md for full command documentation.

## Running
The bot runs as a background console application via the "Discord Bot" workflow.
