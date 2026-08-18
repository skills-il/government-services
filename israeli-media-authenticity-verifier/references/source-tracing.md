# Source and context tracing

This layer catches the dominant real-world case: authentic media that is old, from another
place, or from a game or simulation, just relabeled. Poynter's guidance on war imagery is
that it is "often ... generated with artificial intelligence or else it's old footage
misrepresented as if it's new" (https://www.poynter.org/fact-checking/2026/fake-images-iran-war-how-spot-them/).
So even when every other layer is null, this layer often decides the verdict.

## Reverse-image search

Search the still (or a representative frame from a video) across more than one engine,
because their indexes differ AND because they answer different questions. Pick by job:

- **TinEye first, for earliest appearance.** This is the layer's actual goal. Per TinEye,
  "TinEye does not typically find similar images (that is, a different image with the same
  subject); it finds image matches including those that have been cropped, edited or
  resized" (https://help.tineye.com/article/233-how-does-tineye-work). That match-not-similar
  behaviour, plus sorting by oldest, is what surfaces a recycled original.
- **Yandex Images**, strong on scene matching and on Middle Eastern and Eastern European
  geography.
- **Google Lens**, for identifying a landmark, object or place. It is a semantic
  "similar things" surface: good for "where is this", weak for "when was this first posted".
- **Bing Visual Search** last; it has drifted toward shopping.
- **Search the caption as TEXT.** For content circulating inside Israel, pasting the Hebrew
  or Arabic caption into X or Telegram search often beats any image engine, because the
  same wording is copied along the forwarding chain.

The goal is the EARLIEST appearance, not just any appearance. An image that "appears
online" today but traces to a 2023 article is recycled, not current.

## Video: there is no reverse-video search

State this plainly to the user rather than letting them hunt for a site that takes an MP4.
This has been the practitioner position for years and still is, though the citation itself is
older than the current tool landscape, so present it as the working state of the art rather
than a freshly measured fact. Bellingcat's video-verification guide put it this way: "Currently, there are no freely available tools that allow you to reverse
search an entire video clip the same way we can with image files, but we can do the next
best thing by reverse image searching thumbnails and screenshots"
(https://www.bellingcat.com/resources/how-tos/2017/06/30/advanced-guide-verifying-video-content/).

The substitute workflow:
1. Extract keyframes with `scripts/extract_frames.py --keyframes` (or take 3-5 spread
   screenshots by hand on a phone).
2. Reverse-search several of them, not one. A single frame is often too generic to match.
3. For browser users, the InVID/WeVerify plugin does keyframe extraction plus one-click
   reverse search across engines. Use the maintained project pages,
   https://github.com/AFP-Medialab/invid-verification-plugin or
   https://weverify.eu/verification-plugin/. Its advanced tools require registration
   restricted to journalists, fact-checkers and researchers; the basic keyframe and
   reverse-search path does not.

## Telegram: the platform hands you provenance for free

Telegram is unusually generous to a verifier, and a forwarded Telegram item should be worked
here before anything else:

- **Read the "Forwarded from" chain back** to the earliest visible channel.
- **Open the channel without an account** at `t.me/s/<channel>`, which renders a public
  channel's posts in a browser.
- **Cite the permalink** `t.me/<channel>/<id>`. Message IDs increase over time, so
  neighbouring posts let you bracket when a post appeared even when the timestamp is
  disputed.
- **Look at the channel itself**: creation date and subscriber growth separate an
  established desk from a channel spun up for one influence campaign.
- Caveat: "Forwarded from X" proves a hop, not an origin, and the earliest copy you can see
  is a floor, not proof of the source.

## Stripped forwards and screenshots of screenshots

This is the dominant intake shape, so treat it as its own lane rather than a footnote:

- **Crop the chat chrome before searching.** Bubbles, status bars and keyboards defeat
  image matching. Search the content rectangle only.
- **Read the chat UI as evidence.** WhatsApp's "Forwarded many times" label means the item
  has travelled a long chain, which is a strong prior for viral content and is visible with
  no tooling. Telegram's forwarded-from header, visible timestamps and sender identifiers
  are all evidence about the item's travel, even when the file's own metadata is gone.
- **OCR the visible caption and search that text**, per the caption note above.
- **Note the generation of recompression.** A soft, blocky, small image that claims to be
  last night's original probably is not the original.

## Geolocation (where), with named tools

"Compare it against maps" is a method description, not a method. Use the tools:

- **Google Earth Pro** for satellite comparison, including its historical-imagery time
  slider, which is how you check whether a building or road in the frame existed on the
  claimed date (https://support.google.com/earth/answer/148094).
- **Mapillary** (mapillary.com) for street-level ground truth where satellite view cannot
  resolve a shopfront or a signpost.
- **Overpass Turbo** (https://overpass-turbo.eu/) to query OpenStreetMap for a feature
  combination you can see, for example a mosque next to a petrol station on a dual
  carriageway.
- **Bellingcat's geolocation guide** as the standing reference for the method itself
  (https://www.bellingcat.com/resources/how-tos/2015/07/25/searching-the-earth-essential-geolocation-tools-for-verification/).

What to compare, with the Israeli specifics this skill should own:
- Signage: Hebrew vs Arabic vs Farsi script is often the fastest disqualifier of a claimed
  location, and generators garble all three.
- Vehicle plates: plate colour and format differ between Israeli and Palestinian Authority
  registration. Do not assert a scheme from memory, since these have changed over time.
  Compare the plates in frame against current photographs of vehicles in the claimed location.
- Street furniture and liveries: Egged and Dan bus liveries, Israeli traffic-sign shapes,
  building style (concrete, boiler and solar water heater on the roof).
- Skyline: minaret versus synagogue versus the specific Tel Aviv or Haifa ridge line.

## Chronolocation (when), with named tools

- **SunCalc** (https://www.suncalc.org/) shows the sun's position for a given place and
  time, and can be worked backwards from a shadow's direction and length to a plausible time
  of day. This is the actual chronolocation move; nobody computes solar azimuth by hand.
- **Weather records** for the claimed day versus the weather visible in the frame.
- **Seasonal cues** (foliage, clothing, whether it is a fast day or a holiday) versus the
  claimed date.
- A caveat on EXIF-based map tools (pic2map and similar): they only work when GPS EXIF
  survived, which on forwarded social media it essentially never does. Do not treat their
  blank result as a finding.

## Putting it together

- Earliest appearance predates the claimed event: verdict trends "authentic but
  miscaptioned" (real media, false caption).
- No prior appearance anywhere, plus synthetic visual tells: trends "AI-generated".
- No prior appearance, no tells, no provenance: likely "inconclusive". Say so.

Always separate the media from its caption. A genuine photo with a false "this is X
right now" caption is disinformation even though the pixels are real.

## Face search is out of bounds

Do not put a face into a face-recognition or face-search engine (PimEyes and similar) at any
point in this layer, and decline requests to. Running a face through recognition search is
itself processing a biometric identifier, which Israel's Privacy Protection Law classifies as
"מידע בעל רגישות מיוחדת" (https://www.nevo.co.il/law_html/law01/087_001.htm), the strictest
category; a legitimate verification purpose does not change what the act is.

The permitted substitute, which answers the real question anyway: reverse-search the WHOLE
image rather than a cropped face, and compare the result against photographs the claimed
person published themselves, from verified accounts or news archives.
