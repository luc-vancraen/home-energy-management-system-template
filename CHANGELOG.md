# Changelog

Each version of the template, with the most important changes. Fixed versions with PDFs: see [Releases](https://github.com/luc-vancraen/home-energy-management-system-template/releases).

## v19.1 - November 2026

- "Read only first" is no longer called "always safe": it is the safest start, but check that nothing is written to a device in that phase.
- New paragraph "An AI can make mistakes" at the top: no guarantee that the built software is correct, safe or compliant; the safety rules are requirements, not proof.
- README: quick start in three steps; licence split (CC BY-SA 4.0 for templates and documentation, MIT for the code in `tools/`); this changelog.
- PDFs (14/11, text unchanged): nested lists, such as the five starting profiles and the backup lessons, are now indented under their item instead of flattened.

## v19 - November 2026 (first public version)

Changes compared with v18 (not published):

- Wait time and hysteresis apply only to changing direction; reducing power, going to 0 W and every safety intervention happen immediately.
- go-e charger: `frc=0` after unplugging the car is normal but must be reset immediately; `frc=0` without unplugging is unexplained and reported. The HTTP API v2 and MQTT must first be enabled in the app.
- Capacity tariff: "average monthly peak" clarified as the average over the last 12 months.
- Stale meter data: batteries go to their safe state.
- Cloud-only devices: set a safe default in the device itself (e.g. a limited maximum charging current).
- Wording: tokens, gender-neutral language, closing sentence.

## Before v19

v1 to v18 were internal versions, reviewed several times, in which the template grew from the example system. Among the last changes: go-e `nrg` is an array (total power at index 11); regulate `amp` and keep `ama` fixed; HomeWizard API v1 needs the switch in the app, v2 a token; safety tests are controlled manual hardware commands, also starting from a small active power; a UPS does not count as an independent fallback.
