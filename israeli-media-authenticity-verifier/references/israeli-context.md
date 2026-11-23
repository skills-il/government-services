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

## Wartime publication limit

If the item may show a recent strike or hit in Israel, no field of a shareable report may state, confirm or deny where it happened, and it must not repeat a claimed place. Write "Location checked, details withheld" and "GPS present, withheld". Military censorship restrictions on publishing strike locations may apply, including when forwarding, so check the current rules before sharing. One reported example is the June 2025 order
(https://www.jpost.com/israel-news/defense-news/article-858194). This skill has not read the
order's official text and does not state how far it reaches into private chats.

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

If you hear a siren or get an official alert, go to the protected space first. This channel
also answers one narrow question, whether a claimed official alert was really issued. Its
absence does not disprove an event and must never be used to tell someone they are safe. Authenticating a forward
takes time; confirming against an authority does not. Run verification in parallel, but tell
the user not to re-share before the authority confirms.

## Election-period campaign media

Israel now regulates synthetic campaign media directly, and the rule is operational for a
verifier because it makes the LABEL a readable signal.

- Section 2א2 of the Elections (Propaganda Methods) Law, added by the Elections Law for the
  Twenty-Sixth Knesset, 5786-2026, uses the term "נחזות עמוקה" and provides that a publisher
  of such election propaganda "יצרף לה גילוי המציין באופן ברור ובולט כי התוכן שבה לא תועד
  במקור" (https://fs.knesset.gov.il/25/law/25_lsr_14147458.pdf).
- **It is a temporary provision**, marked in the consolidated law "הוראת שעה מיום 23.7.2026 ועד
  יום 26.10.2027" (https://he.wikisource.org/wiki/חוק_הבחירות_(דרכי_תעמולה)). Check its status
  after that date. It also states: "הוראות סעיף זה לא יחולו על תעמולת בחירות שפורסמה לראשונה
  לפני יום תחילתו", so propaganda first published before 23 July 2026 is outside this section.
- The Elections Committee chair published implementing rules, in force since 26 July 2026.
  Accepted forms are a statement that all or a named part was digitally created and not
  originally documented, or digitally edited in a way that materially changed it, or "לוגו
  שצורתו מפורטת בתוספת לכללים, הכולל את הסימון \"AI\"" with that wording. "לא ניתן להשתמש
  בלוגו עבור תוכן קולי": audio without a visual element needs a spoken notice at its start
  and end, and a video must carry the notice for as long as the content appears
  (https://www.law.co.il/news/2026/07/27/deep-fake-and-ai-elections-propaganda-rules/).
- AI campaign material can also fall under other propaganda rules. The Committee ordered an
  AI video of IDF soldiers removed as "a prohibited use of public property for election
  propaganda purposes", not for a missing label
  (https://www.timesofisrael.com/liveblog_entry/elections-panel-orders-eisenkot-to-take-down-ai-campaign-video-showing-idf-soldiers/).

How to route: a concern about undisclosed synthetic campaign material goes to the Central
Elections Committee, whose chair decides, not to 119 or 105. Describe the rule and the
observation; do not tell the user whether a given publication is lawful.

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
  Tell the user not to pay. If money or a code has already gone, call the bank's fraud line
  immediately to block the card or account and try to stop the transfer, change exposed
  passwords, then file a police complaint and report to the 119 hotline.
- **An ADULT targeted by synthetic sexual or intimate imagery** (an AI-generated nude or a
  face-swapped sexual clip). Do NOT route this to 105, which is scoped to minors. The
  routes that actually apply:
  - **StopNCII.org** for platform-side takedown. Per its FAQ, "If the 'deepfake' or
    synthetic image is of you, you have access to the image and it is nude/semi nude, then
    you can hash it", and "Your images will never leave your device and they will never be
    saved by us. We will only store the digital fingerprints, also known as hashes." It
    requires that you were over 18 in the image. The on-device hashing matters: the victim
    never uploads the image anywhere. Its limit matters too: "StopNCII.org only works on
    public facing platforms", and "Most messaging platforms use encryption which means
    hashing technologies do not apply". For WhatsApp or Telegram, use in-app reporting, ask
    group admins to remove it, and use the routes below.
  - **The sexual assault support helplines** (https://1202.org.il/support-and-information/support/hotlines/):
    1202 (answered by women), 1203 (answered by men), WhatsApp messages to 052-8361202. The person does not need to prove
    the image is fake to get help.
  - **ISOC-IL's safe-internet helpline** (https://www.isoc.org.il/digital-literacy/report)
    for guidance in Hebrew before taking further steps.
  - **The Israel Police online complaint service on gov.il** for the criminal track, and
    100 for an immediate threat.
  StopNCII is for adults only. If the person may have been under 18 in the image, do not use
  any file-based tool: apply the stop rule and report to 105 or the police.
- General crime or an immediate threat to safety: contact the Israel Police, 100 in an
  emergency.

## Preserve the evidence before you report (or block)

Every route above works better with an intact artefact, and every hour of delay degrades
it. ISOC's own guidance leads with documenting first: "צלמו מסך (שיהיה תיעוד לאירוע במידה
ותגישו תלונה במשטרה)" (https://www.isoc.org.il/digital-literacy/cybersafe/sextortion).
**Exception: possible sexual imagery of a minor, real or AI-generated.** Do not save, copy,
screenshot or forward it. Report it to 105 or the police, say where and when you received it,
and follow their instructions about the file.

For anything else, tell the user to, before blocking or deleting anything:

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
audio lane already uses: hang up and make an ordinary phone call to a number you already
saved, not a call inside the same app, and use a pre-agreed family safe word.

A liveness probe can help, but only in one direction: ask the caller to turn a full
90 degrees in profile, pass a hand across their face, or stand up. Real-time face-swap
systems degrade badly on those. Treat it as convict-only: failing the probe is a strong
signal, passing it proves nothing, because these systems can still blink, smile, turn and
speak on command. Interception, recording, and any real-time classifier remain out of scope.

## Face search: do not run a face through a recognition engine

Do not use a face-recognition or face-search engine at all (PimEyes and similar), and decline
requests to. This skill does not do this, whatever the purpose. Do not send an identifiable face to
any reverse-image, visual-search or multi-engine tool either.

To check a CLAIMED KNOWN identity, search the caption and compare by eye against photographs the person themselves published,
from verified accounts or news archives. Under Israel's Privacy Protection Law as amended, a
biometric identifier used to identify a person or verify their identity by computerised means
is "מידע בעל רגישות מיוחדת", a category with heightened protection
(https://www.nevo.co.il/law_html/law01/087_001.htm).

Do not over-promise. This skill helps the user assess and document the media and points
them to the right channel. It does not file reports or contact authorities.
