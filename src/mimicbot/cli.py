import sys
import random
import time

import click

import mimicbot
from mimicbot import twitter

@click.group()
def cli():
    pass

@cli.command()
@click.argument("bot_name")
def create():
    "Create a bot."
    click.echo("create")

@cli.command()
@click.argument("bot_name")
def list():
    "List bots."
    click.echo("list")

@cli.command()
@click.argument("bot_name")
def delete():
    "Delete a bot."
    click.echo("delete")

@cli.command()
@click.argument("bot_name")
def auth():
    "Authenticate a bot against Twitter."
    click.echo("auth")

@cli.command()
@click.argument("bot_name")
def reset():
    "Reset a bot's training."
    click.echo("reset")

@cli.command()
@click.option("--csv-archive",
    help="Train from Twitter CSV tweet archive.")
@click.argument("bot_name")
def train(bot_name, csv_archive):
    "Train a bot from source material."
    bot = mimicbot.Bot(bot_name)
    bot.generator.train_csv(csv_archive)

@cli.command()
@click.option("--random-exit", default=0,
    help="Randomly exit instead of running. 1/INTEGER chance of succeeding.")
@click.option("--random-delay", is_flag=True,
    help="Run with a random delay.")
@click.option("--dry-run", is_flag=True,
    help="Dry run. Do not post.")
@click.argument("bot_name")
def run(bot_name, random_exit, random_delay, dry_run):
    "Run a bot."
    if random_exit:
        roll = random.randint(1, random_exit)
        if roll != 1:
            click.secho("Randomly exiting!", fg="green")
            return
    click.secho("Getting text...", fg="green")
    bot = mimicbot.Bot(bot_name)
    text = bot.get_text()
    click.secho("Got text...", fg="green")
    click.echo("%s" % text)
    if random_delay:
        seconds = random.randint(1, 60)
        click.secho("Sleeping for %ss..." % seconds, fg="green")
        time.sleep(seconds)
    if dry_run:
        click.secho("Dry run. Exiting...", fg="green")
    else:
        click.secho("Posting...", fg="green")
        client = twitter.Client(name)
        client.post(text)
