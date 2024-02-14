# Project Overlord

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/overlord-bot/Overlord.svg)](https://github.com/overlord-bot/Overlord/commits)
[![GitHub issues](https://img.shields.io/github/issues/overlord-bot/Overlord.svg)](https://github.com/overlord-bot/Overlord/issues)
[![GitHub stars](https://img.shields.io/github/stars/overlord-bot/Overlord.svg)](https://github.com/overlord-bot/Overlord/stargazers)

## Description

Project Overlord is a open source Python Discord bot made by students in Rensselaer Polytechnic Institute's RCOS (Rensselaer Center for Open Source).

The goal of this Discord bot is to help make students' lives easier by providing many different utility functions. The following bot modules and functionalities are in development:

- Degree/course planner
- Web crawler with many different search functions
- Chat management to help administer a Discord server
- Minigames inside of Discord
- Calendar to keep track of important events
- Polling to create surveys
- Dockerizing the application

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

In order to run this project and start your own instance of this Discord bot, you will need to do the following:

- Create a [Discord Developer Account](https://discord.com/developers/applications)
- [Clone](https://github.com/overlord-bot/Overlord.git) the repository to your local machine
- Install Python 3.9
- Install the [requirements](https://github.com/overlord-bot/Overlord/blob/main/requirements.txt)
- Create a .env file in the root directory to store the following variables:
    - [TESTING_SERVER_ID](https://github.com/overlord-bot/Overlord/blob/main/bot.py#L19)
    - [DISCORD_TOKEN](https://github.com/overlord-bot/Overlord/blob/main/bot.py#L91)
- Run the [bot.py](bot.py) file

## Usage

For instructions on how to use the Discord bot's commands, please see the [cogs folder](https://github.com/overlord-bot/Overlord/tree/main/cogs) and click on individual modules. Most of these modules have examples on how to use the corresponding commands. 

In the future, we plan on merging the individual module instuctions into an "INSTRUCTIONS.md" file.

## Configuration

Currently, we do not have many configuration options, but we are planning on adding this capability for the bot. We understand that most Discord bots already available have settings/configurations to customize the experience for users, and we are fully committed to making this happen.

## Examples

This section will be expanded in the future when bot modules have matured more.

## Contributing

Guidelines for contributors, including instructions on how to submit bug reports, feature requests, or pull requests. 

Please review the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

### Why the MIT License?

We chose the [MIT License](LICENSE) because it is a permissive open-source license that allows users to use, modify, and distribute the project's code with minimal restrictions. The MIT License allows developers of all backgrounds to contribute to this project, as well as adapt this project for their own needs, without having to worry about complex problems from licensing issues. Additionally, the MIT License aligns with the [Rensselaer Center for Open Source's (RCOS)](https://handbook.rcos.io/#/README) philosophy of promoting collaboration and community-driven development.
