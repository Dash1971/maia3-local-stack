# Maia ratings on Discord: evidence for a flattened strength scale

## Purpose and scope

This document summarizes discussion in the Maia Chess Discord server about the relationship between a Maia model's nominal rating and its realized playing strength. It focuses on the claim that the rating scale is **flattened or compressed**: lower-rated settings tend to play above their labels, while higher-rated settings tend to play below them.

Short excerpts are quoted verbatim. Usernames and original capitalization are retained. The surrounding summaries and commentary are interpretive. Links point to the original Discord messages or their immediate context so an authorized server member can inspect the complete posts.

The material spans December 2024 through August 2026 and includes developer explanations, public-bot ratings, a small local Maia2 test, individual playing experiences, and reports about website behavior. These sources differ greatly in evidential strength.

## Summary conclusion

The Discord record supports five conclusions.

1. A Maia rating is principally a **conditioning label**—the population whose moves the model tries to predict—not a guarantee that the resulting bot will achieve that Elo in complete games.
2. At the lower end, averaging over a population appears to remove some individual inconsistency and large errors. This “committee effect” can make low-rated Maia stronger than a typical individual at the same rating.
3. At the higher end, policy-only or nearly policy-only play does not reproduce all the calculation performed by strong humans. Occasional severe tactical errors can outweigh many otherwise plausible moves.
4. These forces push in opposite directions and compress realized playing strengths toward the middle. Older Maia evidence places the apparent crossover around the mid-1500s or 1600s. The Discord evidence does not locate Maia3's crossover precisely.
5. Model version, time control, sampling method, clock use, openings, and website implementation can change the apparent strength. Ratings drawn from different conditions cannot safely be treated as one uniform dataset.

## 1. The clearest explanation of flattening

In December 2024, Maia developer Ashton Anderson explained that the question Maia answers is what *a member of a rating population* might play, not how one stable individual would conduct an entire game. Different people—and even the same person on different days—can choose different moves in the same position.

He summarized the mechanism as:

> “there are two opposite forces”
>
> — Ashton Anderson, 9 December 2024. [Discord message](https://discord.com/channels/1275283861890138122/1275283861890138125/1315539632129314867)

The first force is population averaging. A model predicting the central tendency of many players does not inherit every individual's narrow repertoire, recurring blind spots, tilt, fatigue, or unusually large mistakes. Anderson said this makes lower-rated models stronger than their source population, giving the example:

> “maia 1100 plays around 1500”
>
> — Ashton Anderson, 9 December 2024. [Same discussion](https://discord.com/channels/1275283861890138122/1275283861890138125/1315539632129314867)

The second force is the absence or severe limitation of search. Maia makes an intuitive policy prediction rather than calculating as extensively as a strong human. Anderson separately clarified:

> “the aggregate level of the play is probably lower than 1900 because we aren't using any search right now”
>
> — Ashton Anderson, 9 December 2024. [Same discussion](https://discord.com/channels/1275283861890138122/1275283861890138125/1315539632129314867)

He noted that Maia1900 could have better move-prediction accuracy on 1900-rated players than Maia1100 has on 1100-rated players and still fail to play at 1900. Good moves are more predictable, but full-game strength is unforgiving: a small number of serious errors can dominate the result.

The high-end effect is gradual rather than a hard threshold:

> “as you get to higher and higher rating levels, search becomes more necessary to play at that level”
>
> — Ashton Anderson, 10 December 2024. [Same discussion](https://discord.com/channels/1275283861890138122/1275283861890138125/1315539632129314867)

This is the most coherent explanation of the flattened scale: **population averaging lifts the bottom, while insufficient calculation suppresses the top**.

## 2. Legacy Maia converges toward the middle

An August 2025 discussion compared the long-running original Maia bots:

> “maia1 has lichess ratings better than 1100, maia5 is around 1500-1600, and maia9 is consistently 1600”
>
> — voltronforce0, 12 August 2025. [Discord message](https://discord.com/channels/1275283861890138122/1275283861890138125/1404613845150072942)

The nominal settings correspond approximately to 1100, 1500, and 1900, yet their reported Lichess ratings occupied a much narrower band. Anderson identified three relevant factors:

- the committee effect boosts lower-rated Maia;
- no search depresses the upper end;
- most Maia games were unrated, while rated results also depended on time use, which Maia1 and Maia2 did not model.

When asked why the nominal-1900 Maia did not benefit enough from population averaging, Anderson wrote:

> “my working hypothesis is that the no-search effect is stronger than the committee effect at 1900”
>
> — Ashton Anderson, 13 August 2025. [Same discussion](https://discord.com/channels/1275283861890138122/1275283861890138125/1404613845150072942)

One community member described the combined pattern as:

> “Both appear to be a kind of reversion toward the mean.”
>
> — Brandl, 13 August 2025. [Same discussion](https://discord.com/channels/1275283861890138122/1275283861890138125/1404613845150072942)

Another participant objected that a literal committee of 1900s should outperform one 1900 and suggested that the real problem was the difficulty of selecting strong moves in one shot. That objection is compatible with the broader flattening claim: “committee effect” is a metaphor for population averaging, not a claim about an actual group deliberating over each move.

## 3. Reports that low Maia3 settings feel too strong

In June 2026, users reported that the website's low Maia3 settings felt unexpectedly difficult. One player contrasted the old Maia bots with the new 600 and 800 settings:

> “Now I’ve just narrowly beaten Maia 600, and Maia 800 knocked me completely out.”
>
> — filly, 12 June 2026. [Discord discussion](https://discord.com/channels/1275283861890138122/1296691291517878433/1514940573851713558)

The same post said both settings felt much stronger than their labels. Another player reported a striking reversal between the extremes:

> “I beat Maia 2600 twice again yesterday. But when I take it to 800 it plays stronger.”
>
> — Sionnach the Silver Fox, 12 June 2026. [Same discussion](https://discord.com/channels/1275283861890138122/1296691291517878433/1514940573851713558)

These are subjective experiences, not controlled results. The surrounding discussion also mentioned color-dependent behavior and uncertainty about the website backend. Nevertheless, the reports show that users independently noticed the same qualitative compression described by developers.

Users also made clear why the labels matter in practice:

> “what’s far more important is a balanced yet challenging game. That’s how you learn and stay motivated.”
>
> — filly, 13 June 2026. [Rating thread](https://discord.com/channels/1275283861890138122/1296691291517878433/threads/1515318883643424779)

From this perspective, a label can accurately describe the training population yet still be misleading to someone selecting an opponent of comparable strength.

## 4. Maia3 ratings reported from public bots

A community member compiled the following snapshot from Maia3-79M Lichess bots in rapid or classical games:

| Nominal setting | Reported rating | Games | Difference from label |
|---:|---:|---:|---:|
| 600 | 1053 | 323 | +453 |
| 800 | 1227 | 151 | +427 |
| 1000 | 1727 | 45 | +727 |
| 1200 | 1594 | 35 | +394 |
| 1600 | approximately 1800 | 26 | approximately +200 |

The author explicitly warned:

> “For the others, There aren't enough games.”
>
> — Tortue, 12 June 2026, edited 13 June 2026. [Discord message](https://discord.com/channels/1275283861890138122/1296691291517878433/1514940573851713558)

Every listed bot was above label, including the nominal-1600 condition. The 1000 and 1200 observations were non-monotonic, and the samples above 800 were very small. The table therefore supports low-end overperformance but does not define a reliable curve.

The author framed the older Maia comparison this way:

> “Maia isn’t calibrated to achieve a specific Elo, but to predict and play the average move of players at that level.”
>
> — Tortue, 13 June 2026. [Discord thread](https://discord.com/channels/1275283861890138122/1296691291517878433/threads/1515318883643424779/1515338984648347769)

They cited original Maia1100 at roughly 1550 and Maia1500 at roughly 1660, attributing the surplus to human-like moves without tilt, fatigue, or as many large blunders.

A follow-up provided a larger nominal-600 sample. The embedded Lichess preview showed 624 games and a rapid rating of 1057. The poster also perceived the website version as stronger:

> “I cannot verify the settings because maiachess.com uses an API on an external backend”
>
> — Tortue, 14 June 2026. [Discord message](https://discord.com/channels/1275283861890138122/1296691291517878433/threads/1515318883643424779/1515379443248664626)

The 624-game result gives the nominal-600 overperformance claim more weight. The frontend comparison is much less secure because the actual settings were unknown.

At nominal 1800, a later probability-sampling bot was also above label. Its embedded Lichess preview reported 236 games and a bullet rating of 2085. Its creator explained:

> “The lichess bot I set up plays from the probability distribution”
>
> — ComradeRamen, 18 August 2026. [Discord message](https://discord.com/channels/1275283861890138122/1296691291517878433/1539099187948556358)

This suggests Maia3 remained above label at 1800 in that implementation. It was bullet rather than rapid or classical and used a specified sampling method, so it cannot be merged directly with the earlier observations.

## 5. Upper-end weakness and inconsistency

In June 2026, a community member analyzed a submitted Maia3-2600 game using Maia's own analysis output:

> “there are many moves with 0% probability that Maia 2600 would be capable of playing in this game...”
>
> — Tortue, 17 June 2026. [Discord discussion](https://discord.com/channels/1275283861890138122/1296691291517878433/1516479238981816411)

This raised the possibility that the website was not faithfully playing from the nominal-2600 distribution. Developer Daniel Monroe responded more generally:

> “Current models have trouble modeling play above 2,000 elo, we are working on making this more realistic”
>
> — Daniel Monroe, 17 June 2026. [Discord message](https://discord.com/channels/1275283861890138122/1296691291517878433/1516479238981816411)

The developer statement acknowledges an upper-rating problem but does not assign achieved ratings to particular settings. It also does not prove that strength declines monotonically above 2000.

A later participant connected implausible high-level moves to the lack of tactical lookahead:

> “The point is Nf8 is hard to "prove" to be better unless u look at the positions ahead”
>
> — sshivaji, 26 June 2026. [Same upper-rating discussion](https://discord.com/channels/1275283861890138122/1296691291517878433/1516479238981816411)

That is a community diagnosis, but it matches the earlier developer explanation: strong human moves are increasingly dependent on calculation, while a policy model can select a plausible-looking move that fails tactically.

## 6. A small Maia2 strength report

In March 2026, one user described 80 Maia2-versus-Stockfish games, with 20 games per persona. They summarized the overall result:

> “at elos from 1320 to 1900 Maia2 topped out at 1500 odd.”
>
> — Darren, 10 March 2026. [Discord message](https://discord.com/channels/1275283861890138122/1275283861890138125/1480608488743899399)

The reported table was:

| Persona | Target | Performance Elo | Delta | W–D–L | Reported 95% interval |
|---|---:|---:|---:|---:|---:|
| Archie | 1200 | 1285 | +85 | 8–2–10 | 1137–1434 |
| Clara | 1500 | 1483 | −17 | 9–1–10 | 1335–1631 |
| Desmond | 1700 | 1573 | −127 | 6–1–13 | 1416–1730 |
| Victoria | 1800 | 1418 | −382 | 1–2–17 | 1183–1654 |

This is the clearest Discord evidence for a Maia2 crossover near 1500: the 1200 condition was above label, 1500 was close, and 1700–1800 were below. Its limitations are substantial: only 20 games supported each estimate, the intervals were wide, and the result depended on a particular CoreML build and Stockfish strength calibration.

## 7. The explicit claim that Maia3 is “extremely compressed”

In August 2026, a developer of a separate Maia-like model predicted that long matches between Maia3 settings would reveal much less strength separation than their labels imply:

> “the true strength difference between the 700 setting and the 2700 setting is not even 1000 rating points.”
>
> “The scale is extremely compressed.”
>
> — tord, 15 August 2026. [Discord message](https://discord.com/channels/1275283861890138122/1275283861890138125/1537456016793403516)

The post attributed the weak upper levels mainly to catastrophic tactical blunders. It also described a tradeoff: adding conventional engine search can raise playing strength while reducing human move-matching accuracy.

This is the strongest explicit statement of the compression hypothesis, but it was phrased as a prediction rather than as the result of a published Maia3 match series. The magnitude—less than 1000 realized points across a 2000-point nominal range—should therefore be treated as an informed estimate.

## 8. Playing strength and analysis usefulness are different

The Discord discussion repeatedly separated Maia's value as a move-prediction system from its calibration as a full-game opponent. Anderson wrote:

> “in that way its an even better as an analysis tool than as a bot”
>
> — Ashton Anderson, 13 August 2025. [Discord discussion](https://discord.com/channels/1275283861890138122/1275283861890138125/1404613845150072942)

The underlying point is that population averaging can improve the probability assigned to a human move even if repeated sampling from that population model does not recreate the strength, consistency, or identity of one person. Three related properties must therefore be kept distinct:

- accuracy at predicting human moves;
- strength when playing complete games;
- subjective resemblance to an individual human player.

Flattened playing strength does not imply that the rating condition is useless for analysis. Conversely, good move matching does not establish that the bot's achieved rating equals its conditioning label.

## 9. Evidence hierarchy

### Strongest evidence

- Repeated developer explanations that population prediction and individual playing strength are different quantities.
- Developer acknowledgement that insufficient search depresses the upper end and that current models have difficulty above 2000.
- Long-running original Maia ratings compressed into roughly the middle of their nominal range.
- A nominal-600 Maia3 bot reported at 1057 rapid after 624 games.

### Moderate evidence

- A nominal-1800 probability-sampling Maia3 bot reported at 2085 bullet after 236 games.
- Consistent reports that low Maia settings feel stronger than their labels and that high settings suffer implausible tactical errors.
- The directionally coherent but small Maia2 test.

### Weak or highly conditional evidence

- Maia3 figures at 1000, 1200, and 1600 based on only 26–45 games.
- Individual claims that 800 felt stronger than 2600.
- Comparisons between the website and Lichess bots when backend settings were unknown.
- Any combined curve mixing bullet, rapid, classical, different builds, and different move-selection rules.

## Final interpretation

The Discord record strongly supports the **direction** of rating compression but does not establish a precise universal mapping from nominal Maia rating to achieved Elo.

For original Maia, the discussion points toward realized strengths clustering around approximately 1500–1660 as nominal settings range from 1100 to 1900. The small Maia2 report similarly places its approximate balance point near 1500, with lower conditions above label and higher conditions below.

For Maia3, every public-bot observation quoted in the server—from nominal 600 through 1800—was above label in its reported sample. The nominal-1600 observation was approximately 1800 but rested on only 26 games. The nominal-1800 bot reached 2085 after 236 bullet games using probability sampling. At the upper end, users and developers reported serious problems above 2000, including tactical failures and website moves inconsistent with the selected high-rating distribution.

The most defensible synthesis is:

> **Maia's nominal rating is a behavioral conditioning variable whose realized game strength is compressed toward the middle: low settings are strengthened by population averaging and consistency, while high settings are weakened by insufficient calculation and occasional catastrophic errors.**

The Discord evidence supports that mechanism and direction. It does not identify a precise Maia3 crossover, and it leaves open whether the mapping is simply compressed, locally non-monotonic, or substantially altered by particular frontends and sampling settings.
