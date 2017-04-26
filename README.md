# steemwc
Word Cloud generator for Steemit

Basic syntax:

  python3 steemwc [date]

Where [date] = a date in YYYY-MM-DD format. Minor regex testing is done to ensure the date is accurate.

Output is a PNG file labeled "steemwc-[date].png" using words from the top 100 Steemit posts (by number of votes) on the date provided.

Requires the following python3 libraries:

  beautifulsoup4
  steemdata
  pymongo
  Pillow
  wordcloud
