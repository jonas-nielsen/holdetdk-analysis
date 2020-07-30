# holdetdk-analysis

This small app attempts to do a few statistics that are not available in the normal Premier League app for Holdet.dk (www.holdet.dk). The app is partly done as an exercise in end-to-end software dev.

Holdet.dk is a online manager-game provided by Danish company Swush. It's very similar to the Premier League Fantasy Manager.

Since I'd prefer not to include datasets in the repo, all datasets is are fetches from Holdet.dk's open API.

Requirements:
- Python 3

Some slight improvements that I hope to do:
- Gather user-specific data from Holdet.dk's API (to let you know how you're doing) - this will probably local authenticatino from the user.
- Include more detailed stats, such as Goals, Assists, Red/Yellow cards, clean sheets, etc.
- Tag on other sources of data - e.g. expected goals, total passes etc. from other sources.
- Containerize app and deploy it.