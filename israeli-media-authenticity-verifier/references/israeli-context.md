# Israeli context: the war-misinformation landscape and reporting channels

## Why this skill is Israeli-specific

The June 2025 Iran-Israel conflict put media manipulation at the center of an Israeli
security event. Per eWeek, "this marks what experts call the first major conflict where
generative AI is shaping the information battlefield"
(https://www.eweek.com/news/ai-deepfake-surge-iran-israel-footage/). Carnegie described it
as AI-generated content that "has taken disinformation to an industrial level"
(https://carnegieendowment.org/research/2025/07/iran-israel-ai-war-propaganda-is-a-warning-to-the-world?lang=en).

Concrete patterns from that period that this skill should expect:
- Fake videos of missile damage in Tel Aviv and at Ben Gurion Airport, some traced to
  Iran-linked sources (eWeek).
- Flight-simulator clips shared as real airstrikes, reaching over 21 million views before
  removal (eWeek).
- Recycled strike footage, video-game clips, and deepfakes flagged by the verification
  group Geoconfirmed (eWeek). The recycled and miscaptioned category was large, so always
  run the source-tracing layer.

Earlier, in April 2025, an Israeli broadcast aired a manipulated AI clip and the anchor
stopped it on air: "These are not Gallant's words but AI trying to insert messages about
the U.S. and the Houthis"
(https://www.getclarity.ai/ai-deepfake-blog/iranian-deepfake-of-israeli-defense-minister-airs-live----and-how-clarity-caught-it-instantly).
Impersonation of public figures is a live threat, not a hypothetical.

## Hebrew WhatsApp and Telegram triage

The dominant way Israelis meet a fake is a forwarded clip with no metadata. Because the
forward strips provenance and EXIF, start from source tracing and visual inspection rather
than provenance. Ask for the original file if you can get it. Treat Hebrew and Arabic text
in the image as a high-value inspection target (garbled script is a strong tell).

## Israeli verification outlets

Before publishing a verdict, check whether an Israeli outlet already addressed the item:
- FakeReporter (fakereporter.net), an Israeli disinformation watchdog with crowdsourced
  flagging of suspect images and video.
- International geolocation collectives (Geoconfirmed-style) that covered the conflict.

## Live security incident: authoritative source first

When the media is about something supposedly happening right now (an attack, an alert), the
user's first action should be the primary source, not forensics: the Home Front Command
(Pikud HaOref) official app and alerts, and established news desks. Authenticating a forward
takes time; confirming against an authority does not. Run verification in parallel, but tell
the user not to re-share before the authority confirms.

## Reporting channels (scope each correctly)

- Cyber incidents, including suspicious messages and AI-impersonation attempts: Israel's
  National Cyber Directorate runs the CERT 119 hotline. As the Times of Israel reported, 119
  "is the cybersecurity hotline Israelis can now call if they are concerned that they are
  under cyberattack ... a 24/7 free service where anyone can report a cyberattack or
  suspicion of attack and get immediate help"
  (https://www.timesofisrael.com/dial-119-for-hacker-alert/). This is a reasonable first
  call for an impersonation or suspicious-message incident that is not purely a bank-fraud
  transaction.
- Harm to a minor online, including AI-generated impersonation, voices, or videos: Israel's
  105 hotline (Child Online Protection Bureau), reachable by calling 105
  (https://www.gov.il/en/departments/units/105_call_center). Use 105 only when the target
  is a minor; do not route every deepfake victim here.
- Impersonation fraud to steal money (someone posing as a bank, a credit card company, the
  Bank of Israel, or the police): the Bank of Israel warns the public about exactly this
  pattern (https://www.boi.org.il/en/information-and-service-to-the-public/consumer-enquiries-and-inspections/warning-to-the-public-with-regard-to-fraud-by-impersonating-the-bank-of-israel-or-commercial-banks/).
  Tell the user to contact their bank's fraud line, and to report the cyber incident to the
  119 hotline.
- General crime or an immediate threat to safety: contact the Israel Police.

Do not over-promise. This skill helps the user assess and document the media and points
them to the right channel. It does not file reports or contact authorities.
