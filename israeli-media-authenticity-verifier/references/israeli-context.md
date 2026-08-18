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
- **המשרוקית (The Whistle)**, the independent fact-checking unit inside Globes and the
  Hebrew-language claim-rating desk. It works to the IFCN code of principles, "בה היא חברה
  משנת 2018" (https://www.globes.co.il/news/article.aspx?did=1001372882). This is the first
  place to check whether a claim has already been adjudicated in Hebrew.
- **FakeReporter** (fakereporter.net), an Israeli disinformation watchdog and public
  reporting route. Note what it is: a watchdog for coordinated inauthentic behaviour and
  influence operations, NOT a claim-rating fact-check desk. Use it to report a network, not
  to look up a verdict.
- International geolocation collectives (Geoconfirmed-style) that covered the conflict.

## Live security incident: authoritative source first

When the media is about something supposedly happening right now (an attack, an alert), the
user's first action should be the primary source, not forensics. Name the channels, because
nobody searches an app store from a description while under fire:

- **oref.org.il**, the Home Front Command site.
- **The official "פיקוד העורף" app**, published by Israel Home Front Command.
- **The verified Telegram channel @PikudHaOref_all** (https://t.me/s/PikudHaOref_all),
  which posts alerts in exactly the form users are trying to authenticate, and can be read
  in a browser with no account.

Third-party alert apps (Tzofar, "צבע אדום" clones) are NOT official. A screenshot of a
third-party app presented as an official alert is a recurring confusion, so check which app
the screenshot actually came from.

This also gives you a comparison target: if a claimed alert does not appear on the official
channel for that timestamp, that is a strong signal on its own. Authenticating a forward
takes time; confirming against an authority does not. Run verification in parallel, but tell
the user not to re-share before the authority confirms.

## Election-period campaign media

Israel now regulates synthetic campaign media directly, and the rule is operational for a
verifier because it makes the LABEL a readable signal.

- The Elections Law for the Twenty-Sixth Knesset (Special Provisions and Legislative
  Amendments), 5786-2026 uses the term "נחזות עמוקה" and provides: "אדם המפרסם תעמולת בחירות
  הכוללת תוכן שנוצר באמצעי דיגיטלי ונחזה להיות מקורי, חייב לציין באופן ברור ובולט שהתוכן לא
  תועד במקור" (https://www.law.co.il/news/2026/07/20/deep-fake-election/).
- The Elections Committee chair published implementing rules, in force since 26 July 2026,
  allowing either a textual statement or "לוגו שצורתו מפורטת בתוספת לכללים, הכולל את הסימון
  \"AI\" ואת הביטוי \"התוכן נוצר באמצעי דיגיטלי ולא תועד במקור\""
  (https://www.law.co.il/news/2026/07/27/deep-fake-and-ai-elections-propaganda-rules/).
- Enforcement is live, not theoretical: "The Central Elections Committee orders Gadi
  Eisenkot, chair of the Yashar party, to take down a campaign video featuring AI-generated
  images of IDF soldiers"
  (https://www.timesofisrael.com/liveblog_entry/elections-panel-orders-eisenkot-to-take-down-ai-campaign-video-showing-idf-soldiers/).

How to route: a complaint about unlabelled or deceptive campaign propaganda goes to the
Central Elections Committee, not to 119 or 105. Describe the rule and the observation; do
not tell the user whether a given publication is lawful.

## Reporting channels (scope each correctly)

- Cyber incidents, including suspicious messages and AI-impersonation attempts: Israel's
  National Cyber Directorate runs the CERT 119 hotline. As the Times of Israel reported, 119
  "is the cybersecurity hotline Israelis can now call if they are concerned that they are
  under cyberattack ... a 24/7 free service where anyone can report a cyberattack or
  suspicion of attack and get immediate help"
  (https://www.timesofisrael.com/dial-119-for-hacker-alert/). This is a reasonable first
  call for an impersonation or suspicious-message incident that is not purely a bank-fraud
  transaction.
- Harm to a minor online: Israel's 105 hotline (Child Online Protection Bureau), reachable by calling 105
  (https://www.gov.il/en/departments/units/105_call_center). Use 105 only when the target
  is a minor; do not route every deepfake victim here. The hotline's published scope is harm,
  violence and crime against children and adolescents in cyberspace, which covers a synthetic
  image or voice used against a minor; the page does not enumerate AI as such, so describe it
  as online harm rather than quoting an AI-specific remit.
- Impersonation fraud to steal money (someone posing as a bank, a credit card company, the
  Bank of Israel, or the police): the Bank of Israel warns the public about exactly this
  pattern (https://www.boi.org.il/en/information-and-service-to-the-public/consumer-enquiries-and-inspections/warning-to-the-public-with-regard-to-fraud-by-impersonating-the-bank-of-israel-or-commercial-banks/).
  Tell the user to contact their bank's fraud line, and to report the cyber incident to the
  119 hotline.
- **An ADULT targeted by synthetic sexual or intimate imagery** (an AI-generated nude or a
  face-swapped sexual clip). Do NOT route this to 105, which is scoped to minors. The
  routes that actually apply:
  - **StopNCII.org** for platform-side takedown. Per its FAQ, "If the 'deepfake' or
    synthetic image is of you, you have access to the image and it is nude/semi nude, then
    you can hash it", and "Your images will never leave your device and they will never be
    saved by us. We will only store the digital fingerprints, also known as hashes." It
    requires that you were over 18 in the image. The on-device hashing matters: the victim
    never uploads the image anywhere.
  - **ISOC-IL's safe-internet helpline** (https://www.isoc.org.il/digital-literacy/report)
    for guidance in Hebrew before taking further steps.
  - **The Israel Police online complaint service on gov.il** for the criminal track, and
    100 for an immediate threat.
  Note that NCMEC's Take It Down service is for under-18s, so a user who guesses between
  the two will usually guess wrong. Match the tool to the victim's age.
- General crime or an immediate threat to safety: contact the Israel Police, 100 in an
  emergency.

## Preserve the evidence before you report (or block)

Every route above works better with an intact artefact, and every hour of delay degrades
it. ISOC's own guidance leads with documenting first: "צלמו מסך (שיהיה תיעוד לאירוע במידה
ותגישו תלונה במשטרה)" (https://www.isoc.org.il/digital-literacy/cybersafe/sextortion).
Tell the user to, before blocking or deleting anything:

- Save the ORIGINAL file, not a fresh screenshot of it.
- Keep the chat thread; do not delete it.
- Record the sender's number or handle, and the message timestamps.
- Screenshot the surrounding conversation, including any forwarding labels.
- Note the date and time they received it.

This is preservation, not certification. This skill does not produce forensic evidence or
expert opinions, and a user with real legal stakes needs a professional.

## Live video calls (a bounded lane)

A "CEO" or a "relative" on a live video call is now a mainstream attack, not a file to
analyse, and it is worth answering rather than deflecting. The decision rule is the one the
audio lane already uses: hang up and call back on a number you already held, and use a
pre-agreed family safe word.

A liveness probe can help, but only in one direction: ask the caller to turn a full
90 degrees in profile, pass a hand across their face, or stand up. Real-time face-swap
systems degrade badly on those. Treat it as convict-only: failing the probe is a strong
signal, passing it proves nothing, because these systems can still blink, smile, turn and
speak on command. Interception, recording, and any real-time classifier remain out of scope.

## Face search: do not run a face through a recognition engine

Do not use a face-recognition or face-search engine at all (PimEyes and similar), and decline
requests to. Purpose does not cure this one: running a face through recognition search is
itself the regulated act, whoever the subject is and whatever you meant to establish.

To verify a CLAIMED KNOWN identity, use the permitted route instead: reverse-search the WHOLE
image rather than a cropped face, and compare it against photographs the person themselves
published, from verified accounts or news archives. That answers "is this the picture they
say it is" without ever performing biometric identification. This is not only etiquette: under Israel's Privacy Protection Law
as amended, a biometric identifier used to identify a person or verify their identity by
computerised means is "מידע בעל רגישות מיוחדת", the strictest category
(https://www.nevo.co.il/law_html/law01/087_001.htm), so running a stranger's face through
recognition search is a regulated act.

Do not over-promise. This skill helps the user assess and document the media and points
them to the right channel. It does not file reports or contact authorities.
