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
@click.argument("name")
def auth():
    "Authenticate against Twitter."
    click.echo("reset")

@cli.command()
def reset():
    "Reset training."
    click.echo("reset")

@cli.command()
def train():
    "Train from source material."
    click.echo("reset")

@cli.command()
@click.option("--random-exit", default=0,
    help="Randomly exit instead of running. 1/INTEGER chance of succeeding.")
@click.option("--random-delay", is_flag=True,
    help="Run with a random delay.")
@click.option("--dry-run", is_flag=True,
    help="Dry run. Do not post.")
@click.argument("name")
def run(name, random_exit, random_delay, dry_run):
    "Run the bot."
    if random_exit:
        roll = random.randint(1, random_exit)
        if roll != 1:
            click.secho("Randomly exiting!", fg="green")
            return
    click.secho("Getting text...", fg="green")
    bot = mimicbot.Bot(name)
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
