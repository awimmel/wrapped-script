A quick script I wrote to verify that Spotify Wrapped's results were accurate and to give me some more detailed insights into my data.

To start, you'll need to download your Spotify data. You can request to do that [here](https://support.spotify.com/us/article/data-rights-and-privacy-settings/). After you extact the `.zip`, copy any `StreamingHistory_music_<number>.json` files into the `resources/listening_history` directory.

With that, you can just run `python wrapped_checker.py` to get the stats in a more organized fashion. A quick summary will print to your terminal, and you will also get some `.csv` files in `resources/output`.

The script could definitely be cleaned up a lot, but I was just looking for a quick check.

Requirements:
- At least Python 3

