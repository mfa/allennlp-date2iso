"""
  Date Generator
    This code creates data for our date translation model
  Original version:
    https://github.com/datalogue/keras-attention/blob/master/data/generate.py
"""
import csv
import datetime
import random
from pathlib import Path

import babel
import click
from babel.dates import format_date
from faker import Faker
from tqdm import tqdm

DATA_FOLDER = Path(__file__).resolve().parent / "data"

fake = Faker()
Faker.seed(230517)
random.seed(230517)

FORMATS = [
    "short",
    "medium",
    "long",
    "full",
    "d MMM YYY",
    "d MMMM YYY",
    "dd MMM YYY",
    "d MMM, YYY",
    "d MMMM, YYY",
    "dd, MMM YYY",
    "d MM YY",
    "d MMMM YYY",
    "MMMM d YYY",
    "MMMM d, YYY",
    "dd.MM.YY",
]


def create_date(locales, is_validation):
    """
    Creates some fake dates
    :returns: tuple containing
              1. human formatted string
              2. machine formatted string
              3. date object.
    """

    # add more out-of-range dates to validation
    weight = 0.5 if is_validation else 0.1
    if random.random() < weight:
        start_date = datetime.datetime(1, 1, 1, 0, 0)
        end_date = datetime.datetime(2100, 12, 31, 23, 59)
    else:
        # training-data
        # get dates from January 1, 1940 until today
        start_date = datetime.datetime(1940, 1, 1, 0, 0)
        end_date = datetime.datetime(2039, 12, 31, 23, 59)

    dt = fake.date_time_ad(start_datetime=start_date, end_datetime=end_date).date()

    # wrapping this in a try catch because
    # the locale 'vo' and format 'full' will fail
    try:
        human = format_date(
            dt, format=random.choice(FORMATS), locale=random.choice(locales)
        )

        case_change = random.randint(0, 3)  # 1/2 chance of case change
        if case_change == 1:
            human = human.upper()
        elif case_change == 2:
            human = human.lower()

        machine = dt.isoformat()
    except AttributeError as e:
        return None, None, None

    return human, machine, dt


def create_dataset(dataset_name, n_examples, all_languages, is_validation):
    locales = {}
    locales["important"] = ["en_US", "en_GB", "de_DE", "fr_FR", "es_ES"]
    locales["all"] = babel.localedata.locale_identifiers()

    with open(dataset_name, "w") as fp:
        writer = csv.DictWriter(
            fp, delimiter="\t", fieldnames=["input", "target"], quoting=csv.QUOTE_NONE
        )

        for index in tqdm(range(n_examples)):
            if all_languages:
                _locales = locales[random.choice(list(locales.keys()))]
            else:
                _locales = locales["important"]
            h, m, _ = create_date(_locales, is_validation)
            if h is not None:
                writer.writerow({"input": h, "target": m})


@click.command()
@click.option("--train-size", "-t", default=500000)
@click.option("--validation-size", "-v", default=1000)
@click.option("--all/--no-all", "all_languages", default=False)
@click.option("--overwrite/--no-overwrite", default=False)
def main(train_size, validation_size, all_languages, overwrite):
    suffix = "_all" if all_languages else ""
    train_filename = DATA_FOLDER / f"training_{train_size}{suffix}.csv"
    validation_filename = DATA_FOLDER / f"validation_{validation_size}{suffix}.csv"

    if not overwrite:
        if train_filename.exists():
            click.echo(f"{train_filename} exists.")
        if validation_filename.exists():
            click.echo(f"{validation_filename} exists.")
        if train_filename.exists() or validation_filename.exists():
            return

    click.echo("creating dataset")

    create_dataset(train_filename, train_size, all_languages, False)
    create_dataset(validation_filename, validation_size, all_languages, True)
    click.echo("dataset created.")


if __name__ == "__main__":
    main()
