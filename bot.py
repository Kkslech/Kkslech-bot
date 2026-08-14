name: KKSLech Bot

on:
  schedule:
    - cron: '*/15 * * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run bot
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHANNEL: ${{ secrets.TELEGRAM_CHANNEL }}
        run: python bot.py

      - name: Commit updated posted_links.json
        run: |
          git config --global user.name "kkslech-bot"
          git config --global user.email "bot@users.noreply.github.com"
          git add posted_links.json
          git diff --staged --quiet || git commit -m "Update posted links"
          git push
