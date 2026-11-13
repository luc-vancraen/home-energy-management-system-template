# Home Energy Management System template

**A prompt that lets an AI assistant build a home energy management system (EMS) tailored to your own installation, on your own Linux machine.**

[Nederlandse versie hieronder](#nederlands)

## What it does

You give this template to an AI assistant. The assistant first asks about your installation and wishes, checks your machine, proposes a plan, and only builds after you approve it. The result is a set of ordinary programs on your own computer that can:

- read your digital electricity meter (e.g. a P1 dongle) and keep a history;
- show a dashboard, daily reports and notifications;
- control home batteries, an EV charger and other appliances on solar surplus, price and the 15-minute peak (capacity tariff);
- compare contracts with your real consumption (tariff comparison, monthly "shadow bill") and simulate solar panels and batteries before you buy anything.

The template is based on a system that has been running stably for months in a house in Flanders (Belgium), with home batteries, solar panels, an EV charger and an electric car. It contains the lessons learned there: safety rules, failsafes, an emergency stop, backups that can really be restored, and pitfalls such as daylight saving time.

You do not need to program. You do need to answer questions, sometimes change a setting in an app, and approve the commands the assistant wants to run.

## Starting profiles

You do not need batteries or solar panels to start:

1. **Advice before buying**: what would solar panels, batteries, smart charging or another contract yield with your own consumption? Nothing is controlled.
2. **Insight**: measuring, dashboard and reports only.
3. **Testing a tariff**: compare your contract with dynamic and other contracts, month by month.
4. **Shifting consumption without a battery**: car, water heater, heat pump at cheap or sunny hours.
5. **Full system**: batteries, solar, car, appliances.

## Which AI?

The template is not tied to one AI. It works best with an **AI agent** that can run commands on your Linux machine, for example Claude Code, OpenAI Codex CLI, Gemini CLI or Kimi Code CLI. A **regular chat** (ChatGPT, Claude, Gemini, Kimi, ...) also works: the assistant then gives you one command at a time and you paste the result back. For advice only, a chat in which you can upload your consumption data is enough.

## How to use

1. Read the section "For the user" at the top of the template.
2. **With an agent**: put `hems-template-en.md` (or `hems-template-nl.md`) in an empty folder on your Linux machine, start the agent there and type: `Read hems-template-en.md and follow it.`
3. **In a chat**: upload the file or paste its content as the first message, with the request "Follow this".

The assistant keeps its notes in `AGENTS.md` and an overview of your installation in `installation.md`, so you can continue over several sessions, even with a different AI.

## Files

| File | Content |
|---|---|
| `hems-template-en.md` | The template in English |
| `hems-template-nl.md` | The template in Dutch (same content) |
| `hems-template-en.pdf`, `hems-template-nl.pdf` | The same, as PDF to read or print |
| `tools/mkpdf_template.py` | Script that makes the PDFs (Python, reportlab, DejaVu fonts) |
| `LICENSE` | CC BY-SA 4.0 |

To rebuild a PDF: `python tools/mkpdf_template.py hems-template-en.md hems-template-en.pdf`

## Safety and responsibility

The system can control devices that switch a lot of power. You remain responsible for your installation. The template tells the assistant never to change the electrical installation itself, to respect the main fuse and the limits of every device, to read only before it controls, and to test every control step with low power while you are present. When in doubt, use read-only mode: that is always safe. Check the warranty terms of your devices before allowing third-party control.

## Contributing

Learned something about a device that is not in appendix A yet (another battery, charger or inverter)? Open an issue or a pull request, without personal data. Please change the Dutch and the English version together, so they keep the same content.

## Licence

Made by **luc-vancraen**. Licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/): you may use, share and adapt it, also commercially, if you credit the maker, link to the licence, indicate your changes and share adaptations under the same licence. Provided as is, without warranty.

---

## Nederlands

**Een prompt waarmee een AI-assistent een thuis-energiebeheersysteem (EMS) bouwt op maat van je eigen installatie, op je eigen Linux-machine.**

Je geeft dit template aan een AI-assistent. Die vraagt eerst naar je installatie en wensen, kijkt je machine na, stelt een plan voor en bouwt pas na je akkoord. Het resultaat zijn gewone programma's op je eigen computer die je digitale meter uitlezen, een dashboard, rapporten en meldingen geven, thuisbatterijen, een laadpaal en andere toestellen sturen op zon, prijs en kwartierpiek, en contracten vergelijken met je echte verbruik. Ook zonder batterijen of zonnepanelen kan je starten, bv. met enkel advies vóór aankoop.

Het template is gebaseerd op een systeem dat al maanden stabiel draait in een huis in Vlaanderen, en bevat de lessen die daar geleerd zijn.

**Welke AI?** Het best een AI-agent die commando's kan uitvoeren op je Linux-machine (bv. Claude Code, OpenAI Codex CLI, Gemini CLI, Kimi Code CLI). Een gewone chat (ChatGPT, Claude, Gemini, Kimi, ...) kan ook: de assistent geeft dan telkens één commando en jij plakt het resultaat terug.

**Gebruik**: lees eerst "Voor de gebruiker" bovenaan `hems-template-nl.md`. Met een agent: zet het bestand in een lege map op je Linux-machine, start daar de agent en typ `Lees hems-template-nl.md en volg het.` In een chat: laad het bestand op of plak de inhoud als eerste bericht, met de vraag "Volg dit".

**Veiligheid**: jij blijft verantwoordelijk voor je installatie. Het template laat de assistent nooit iets aan de elektrische installatie wijzigen, eerst enkel uitlezen, en elke sturing eerst met klein vermogen testen terwijl je erbij bent.

**Licentie**: gemaakt door **luc-vancraen**, onder [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.nl). Vrij te gebruiken, delen en aanpassen, ook commercieel, met vermelding van de maker en onder dezelfde licentie. Zonder garantie.
