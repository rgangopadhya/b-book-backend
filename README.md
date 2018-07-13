# Bottomless Book Overview

Bottomless Book is a tablet app designed for young children (tested with as young as 1 and as old as 5) and their parents to create their own stories. Children pick from a set of characters and 5 scenes with that character are provided. They then record their story, and can play it back later.

## Vision

Right now, Bottomless Book has 3 characters, with 5 scenes for each character. Eventually there will be more characters, with more scenes for each character. We intend to make it easy for artists to add new characters to the system.

Technically, the app should be saving data locally by default, with a cloud sync on-demand. This would improve performance. An immediate next step is to store the character and story data locally.

# Running this Project

Simply `dj server` if you have a postgres server conforming to `settings.py`

## Requirements

* [Anthony Leontiev's `dj` Django CLI](https://github.com/aleontiev/dj), which will install `pyenv` and `virtualenv` and provides a simple CLI to abstract away the fact that you're using a virtualenv.
