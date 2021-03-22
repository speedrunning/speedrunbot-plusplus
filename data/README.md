# Bot Config

The bot can be configured via editing the `srbpp.json` configuration file, an
example of which can be seen in the included [example](srbpp.json.example).

## Configuration Parameters

- `token`
  - A string containing the bots token. Be very careful when sharing this, as
  anyone with this token can run code on the bot.
- `botmasters`
  - An array of discord user IDs in the form of integers. Users listed as
  botmasters have elevated bot permissions. Some of these permissions include
  the ability to pull code from this repository, and to reload cogs.
