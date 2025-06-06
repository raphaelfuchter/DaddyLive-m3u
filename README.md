# DaddyLive TV
DaddyLive is a platform that offers live TV and sports streaming across selected categories. Users can stream and watch live TV directly through their browser without the need for an account or subscription.

For added flexibility, this repository provides an M3U playlist featuring DaddyLive's channels. With this, you can load the streams into any IPTV application that supports M3U-formatted playlists, however this repo will only provide the playlist format for Tivimate. Figure out how to format it for other applications yourself.

You can view the full list of channels provided by DaddyLive [here](https://daddylive.dad/24-7-channels.php). 

**Notes:**

* Adult channels have been omitted (you goon).

* At the time of compiling this list, a few streams were down so if they existed in TVPass, they were used as a substitute, otherwise they were removed entirely.
# Instructions
Clone the project.
```
git clone https://github.com/vinny307/daddylive-m3u.git
```
cd into it and run **generate_auth_list.py**. This will compile each streams channel key, authTs, authRnd, and authSig.
```
cd daddylive-m3u
python3 generate_auth_list.py
```
This will take a minute enumerate. Do not interrupt it.

When it finishes, run **generate_signature_urls.py** to compile all of the stream signatures into URLs that are used to unlock the decryption keys.
```
python3 generate_signature_urls.py
```
run **curl.py** to curl each URL. This is essentially what your browser does anytime you load a stream on the daddylive website.
```
python3 curl.py
```
This should begin returning HTTP/2 200 for every source. Do not interrupt it.

The signature URLs generated refresh after a certain interval so if you wait too long to perform this curl, you'll likely encounter HTTP/2 403. If that happens, start over from generate_auth_list.py.

# Playlist
That's it. All streams should now be decrypted.

Load the URLs below into Tivimate as an "M3U Playlist."
  
   **Playlist:** `https://raw.githubusercontent.com/vinny307/daddylive-m3u/refs/heads/main/tivimate_playlist.m3u8`  
   **EPG URL:** `https://raw.githubusercontent.com/vinny307/daddylive-m3u/refs/heads/main/epg.xml`  **DOES NOT WORK. Looking into it.**

# Disclaimer:

This repository has no control over the streams, links, or the legality of the content provided by daddylive.dad (including all mirror sites). It is the end user's responsibility to ensure the legal use of these streams, and we strongly recommend verifying that the content complies with the laws and regulations of your country before use.

