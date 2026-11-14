# Prompt: building a home energy management system (EMS) on your own Linux machine

Template v19.1 - November 2026

## For the user (read this first)

- **What is this?** Instructions for an AI assistant. With them, the assistant builds a system on your Linux machine that reads your energy meter, keeps a record of everything, can control home batteries, an EV charger and other devices, and keeps you informed through a dashboard, reports and notifications. It is based on an existing system that has been running stably for months, supplemented with ideas from well-known open-source projects (evcc, EMHASS, Predbat, SEM, PV Excess Control).
- **Which AI?** The template is not tied to one AI or one company. It works best with an **AI agent**: an AI that can run commands and write files on your computer itself, such as Claude Code, OpenAI Codex CLI, Gemini CLI or Kimi Code CLI. A **regular chat** in the browser or app (ChatGPT, Claude, Gemini, Kimi, ...) also works: the assistant then runs nothing itself, but gives you one command or file at a time; you run it in a terminal on the Linux machine and paste the result back. That works, but it is slower and needs more care. For advice only (profile 1), a chat in which you can upload your consumption data is enough. Choose a strong model: smaller models follow long instructions like these less well; in that case, let it work phase by phase.
- **How do you use it?** With an agent: put this file (`hems-template-en.md`) in an empty folder on the Linux machine, start the agent there and type: "Read hems-template-en.md and follow it." That way the assistant can refer back to it later. In a chat: upload the file or paste its content as the first message, with the request "Follow this".
- **Your own responsibility.** The system controls devices that switch a lot of power. You remain responsible for your installation. The assistant changes nothing in the electrical installation itself (wiring, fuses, inverter settings fixed by the grid operator). Read the warranty terms of your batteries and charger: some manufacturers do not like third-party control. When in doubt: start with reading only, without control commands. That is the safest, but not risk-free by itself: check that the program really writes nothing to a device in that phase (the assistant shows you how).
- **An AI can make mistakes.** Even with this template, the assistant can get things wrong: in code, in calculations or in what a device does. There is no guarantee that the software it builds is correct, safe or compliant with the rules. The safety rules in this template are requirements for what is built, not proof that the built system follows them. That is why observation mode, the low-power tests while you are present and your approval of every step are mandatory. If you doubt what the assistant says about your devices, your installation or the rules, check with the manufacturer, your installer or your grid operator.
- **Permissions.** Most agents ask permission for every command. Do not approve everything automatically while building: you want to see every system change. You run commands with `sudo` (password required) yourself in a separate terminal (some agents also allow this in the session, e.g. by typing `! sudo ...` in Claude Code). Never give the assistant your sudo password in the chat.
- **Numbers in this text** (such as 180 s or 250 W) are starting values that worked in the example system, not laws. The assistant adapts them to your devices.
- **Even if you have (almost) nothing yet.** The template also works without batteries, solar panels or a car. Choose a starting profile up front:
  1. **Advice before buying**: you have nothing yet or are in doubt. Using your own consumption, the assistant calculates what solar panels, batteries (and how many), smart charging, a heat pump or a different contract would yield. Nothing is controlled.
  2. **Insight**: measuring, dashboard and reports only.
  3. **Testing a tariff**: measuring plus a continuous "shadow bill" that compares your current contract with dynamic and other contracts.
  4. **Shifting consumption without a battery**: dynamic tariff, car, water heater, heat pump or pumps at cheap or sunny hours.
  5. **Full system**: batteries, solar, car, appliances.
  You can always move on to the next profile later; what has been built stays.
- **The conversation takes a while.** Phase 1 asks many questions; that is deliberate. Anything you do not know or do not care about may be skipped: the assistant then chooses a safe default and says which one.
- **Over several sessions.** Building takes several days. The assistant keeps track of everything in `AGENTS.md` and `installation.md` in the project folder. Next time, start the agent in the same folder (many agents can also resume the previous conversation) and say where you left off. Note: many agents automatically read a fixed notes file at every session, but not this prompt file. `AGENTS.md` is the common name (e.g. OpenAI Codex CLI and Kimi Code CLI); Claude Code reads `CLAUDE.md` and Gemini CLI `GEMINI.md`. That is why the assistant puts the most important rules and your choices in `AGENTS.md`, and for an agent with a different file name creates a short file with that name that points to `AGENTS.md`. If you work in a regular chat: keep `AGENTS.md` and `installation.md` and upload (or paste) them at the start of every new conversation, together with this template.
- **The system runs without AI.** What gets built are ordinary programs on your own machine. They keep working if you stop using the AI or your subscription ends; you only need the AI to build, adjust or investigate problems. You can also switch AI later: everything is in `AGENTS.md`, `installation.md` and the code.
- **Running costs.** Count on the power consumption of the machine itself (an efficient 10 W mini PC is about 90 kWh per year) and possibly the AI subscription or API costs while building. The rest can be free.

## What do you need?

### Always
- **Need advice only (profile 1)?** Then an ordinary laptop or PC is enough, even if it is not always on: Windows (with WSL, Linux under Windows), a Mac, or the computer of someone who helps. A machine that runs day and night is only needed to measure or control.
- **To measure or control: a Linux machine that runs day and night.** An efficient mini PC (e.g. Intel N100, 5-15 W) or a Raspberry Pi 4/5 with an SSD (no SD card: it wears out from the many writes). At least 4 GB of RAM (8 GB if Home Assistant runs alongside), 64 GB of storage or more. Preferably with a network cable, not over Wi-Fi. If your Home Assistant runs on Home Assistant OS (a separate operating system), the system cannot simply run next to it: see block H ("Where does it run?").
- **Only a Windows PC?** Linux under Windows (WSL 2) can also be used to measure and, under conditions, to control: the PC must run day and night (sleep off), WSL must start automatically with Windows and must not shut down automatically, and Windows Update can restart the PC. A separate, efficient machine remains the recommendation for control. See block H and "Security" in phase 4.
- **Operating system**: a common Linux distribution such as Debian or Ubuntu (server or desktop). You need a user with `sudo` rights.
- **An AI assistant**: preferably an AI agent on that machine (see "Which AI?"), with the subscription or API account it requires, installed according to the maker's official instructions. If you prefer to work from your usual computer: connect to the Linux machine over SSH and start the agent there. With a regular chat you also need a terminal on the Linux machine (directly or over SSH) to run the commands.
- **Access to your router**, to give the devices a fixed IP address (DHCP reservation).
- **Internet** while building (downloading packages). After that the system also works without it, except prices, forecasts and notifications.
- **Time**: count on a few evenings for the basics, and then a few weeks of follow-up and fine-tuning. No programming knowledge is needed; you do need to answer questions, occasionally change a setting in an app and have a command run.

### Depending on your profile
- **Advice before buying**: your consumption data. In Flanders: quarter-hour data from "Mijn Fluvius" (log in with itsme or eID, export as CSV). Otherwise your annual bill and, if you have them, a few recent bills. Possibly quotes for solar panels or batteries.
- **Measuring (all other profiles)**: a digital meter with a reader module (dongle), e.g. a HomeWizard P1 Meter or another dongle that can be read locally. Such a dongle is a small device, not software: the manufacturer's app is only used to set it up, and nothing from the manufacturer needs to be installed on the machine. The data port must be activated (in Flanders via "Mijn Fluvius"). See "Preparing the meter" below. Still an analogue meter (with a rotating disc or counter)? Then: request a digital meter from the grid operator, have an electrician install a clamp meter, or for now only advice based on annual readings.
- **One dongle is enough**, if it shares its measurements locally over the network: then the battery, this system and possibly Home Assistant all read the same source. In the example system there is one HomeWizard on the meter; the batteries get the measurements from that HomeWizard via the Marstek app, and the system reads the same HomeWizard via the local API. Home Assistant is not needed for that. A P1 cable directly to the machine or a brand-specific dongle that only serves its own battery or the cloud does occupy the port: a second reader then needs a splitter or a different dongle.
- **Outside Belgium, the Netherlands and Luxembourg** the port has a different name and works differently (e.g. the HAN port in Scandinavia, an optical port or Smart Meter Gateway in Germany, Linky TIC in France, an in-home display or CAD in the United Kingdom). The assistant looks up the right way to read the meter in your country.
- **Dynamic tariff or tariff comparison**: a free ENTSO-E token for market prices (request it via the ENTSO-E transparency website) and the price formulas of the contracts you want to compare.
- **Measuring solar panels**: an inverter that can be read locally (Modbus, local API), or possibly an ESP32 module (a few euros) for inverters with Bluetooth.
- **Controlling batteries**: batteries with local access (preferably Modbus TCP over a network cable), and access to the manufacturer's app (to enable local access and see the firmware version).
- **Controlling the car**: a charger that can be controlled locally (MQTT, HTTP API, Modbus or OCPP) and its app. For the car's state of charge: an integration such as TeslaMate (Tesla) or a Home Assistant integration; without one it also works, with an estimate.
- **Other appliances**: smart plugs or relays (e.g. Shelly) or an SG-ready input on the heat pump.
- **Notifications by e-mail**: a mail account with SMTP access, preferably with a separate app password.
- **Backup** (recommended): a NAS, external disk or cloud storage.
- **Remote access** (optional): a free VPN such as Tailscale.

### Preparing the meter (you do this yourself, about 15 minutes plus the grid operator's waiting time)
No electrician needed, and the assistant cannot do this for you: these are actions at the meter and in apps.
1. Activate the data port with the grid operator (in Flanders: "Mijn Fluvius", log in with itsme or eID; this can take a few days).
2. Plug the dongle into the port (for P1: the small RJ12 plug under the flap of the digital meter; you do not break a seal). With some meters the port supplies too little power and a USB power supply is needed.
3. Connect the dongle to Wi-Fi (or a network cable) via the manufacturer's app.
4. Find out which local API the dongle has and what it needs, according to the official documentation for that device and firmware. With HomeWizard: API v1 must be enabled in the app; API v2 does not need that switch, but requires a token (obtained once by pressing the button on the meter). Without local access, no system can read the meter locally.
5. Give the dongle a fixed IP address in the router (DHCP reservation).
6. Optional: in the app of your battery or inverter, select the same dongle as the meter, if it supports that.

Then the assistant looks for the dongle on the network, reads one measurement and checks what comes in (see phase 2), before it starts logging.

### What you do not need
- No programming knowledge, no manufacturer cloud subscriptions, no open ports in your router, no changes to the electrical installation.
- No manufacturer software on the machine: you use the apps (meter, battery, charger) on your smartphone to set up the devices; the system talks to the devices itself over the network.
- No Home Assistant: it is optional (see block H).

## Instructions for the AI assistant

You are an AI assistant helping me build a home energy management system (EMS) tailored to my installation on my Linux machine. Below is what the example system does, which options there are and which lessons were learned. My installation is different: so build nothing until phase 1 (questions), phase 2 (checking the machine) and phase 3 (plan) are complete and I have approved the plan.

How you work depends on what you can do:
- **As an agent** (you can run commands and write files on my machine yourself): work directly, but ask permission for every change to the system.
- **In a regular chat** (no access to my machine): give me one command or one complete file at a time, with the folder where it belongs, and say what I should see. Ask me to paste the output back and only continue when it is correct. Never guess what a command returns and never pretend you ran or checked something. Keep files short enough to copy in one go.
- **Without internet access**: say so when you cannot look something up yourself (tariff sheets, regulations, manuals), ask me to provide the source, and never use your prior knowledge as an established fact.
- If your agent uses a fixed notes file other than `AGENTS.md` (e.g. `CLAUDE.md` or `GEMINI.md`), create it with one line that points to `AGENTS.md`, so every session reads the rules.

Way of working during the conversation:
- First ask who is taking part: the **resident** (for whom the system is) and possibly a **helper** (family, neighbour, installer; sometimes remote). For each, ask how technical they are (no experience / some Linux experience / programmer) and which language they speak. Technical questions go to the helper, wishes and choices to the resident. Reports, dashboard and notifications for the resident are in the resident's language; `AGENTS.md` and technical notes in the helper's language. If there is no helper, the resident is both. Adapt your explanations; briefly explain jargon for anyone who is not a programmer.
- Ask the questions block by block. Use multiple-choice questions where possible, with your recommended choice as the first option. Wait for my answer each time.
- If I do not know something, help me find it (app, rating plate, bill, router, manual) or look it up on the network yourself, but only after my approval.
- Skip what does not apply (no car = no EV questions and no EV components).
- **Quick start**: in phase 1, first ask only the questions needed for the starting profile, the meter and the dashboard (usually about ten). Ask the remaining questions of a block only when that module's turn comes. With people without experience, ask every few blocks whether they want to pause; the conversation may span several days.
- **Express mode**: if I want to skip all questions ("just do something"), choose safe defaults: measuring, dashboard and observation mode only, no control. Before anything at all is controlled, these key points must always be confirmed, however briefly: which devices are controlled, maximum power per device, main fuse and number of phases, the sign (charging/discharging) tested at low power, that nothing else controls the device, and that the emergency stop works.
- **Checking answers**: compare my answers with what the measurements show (number of phases, power levels, consumption, contract versus bill). If something does not match, say so kindly and ask what is correct before you build on it.
- **Look things up yourself instead of making me search**: official supplier tariff sheets, grid tariffs, the rules of my region (capacity tariff, net metering, registration of batteries, subsidies) and the manuals of my devices you look up on the internet yourself, at the official source. Always state the source and the date, and let me confirm the most important values. Rules and prices change: never use only your own prior knowledge as fact.

## Phase 1 - Asking about my installation and wishes

### Block A - Starting profile, goals and priorities
- First a short pre-check, before all other questions: do I have a digital meter, is the data port activated, and is there already a dongle on it that can be read locally (and if so, does my battery or inverter already use it)? If not: say right away which profiles are possible now (advice before buying, based on quarter-hour data or the annual bill) and what I need to arrange first (see "Preparing the meter"), so that I do not first fill in all blocks for something that is not yet possible.
- Which starting profile fits (advice before buying / insight / testing a tariff / shifting consumption without a battery / full system)? Profiles may be combined; a common combination is "testing a tariff" + "shifting consumption without a battery" (first see whether a dynamic contract pays off, and meanwhile let the car and heat pump work smartly). Then ask only the questions that belong to the chosen profiles. For "advice before buying": start with block J and ask the other blocks only as far as needed.
- What are my three most important goals? Let me pick three (not a full ranking) from: use as much of my own solar power as possible; lowest possible energy bill; lowest possible 15-minute peak (capacity tariff); as little feed-in as possible; as little CO2 as possible (use power when the grid is greenest); spare the batteries (fewer cycles, not always 100%); keep a reserve for power cuts; the car always charged enough in time; as little intervention as possible ("it should just work").
- Do I want the system to control right away, or first only measure for a while and show what it would do (observation mode)?
- How many notifications do I want: only on problems, a daily report, or also weekly/monthly overviews?
- Budget: may something cost money? E.g. a paid forecasting service, an ESP32 module or Modbus adapter (a few tens of euros), a licence for an existing package. Default: free services only.
- Small installation (e.g. balcony panels or one plug-in battery)? Then the system's own consumption weighs heavily: a 10 W mini PC uses about 90 kWh per year, which can eat up a large part of the gain. Calculate the net gain and suggest lighter options: a device that is on day and night anyway (NAS, router with Docker, existing Home Assistant), an ESP32 solution, or simply let the device's own logic work with only insight added.
- Plans for the coming years: extra panels, extra battery, heat pump, second car, new charger? Then we take that into account now.

### Block B - Country, grid connection and contract
- Country and grid operator (if I do not know them: derive them from the municipality). (Flanders: capacity tariff on the average of the monthly peaks (highest 15-minute peak per month) over the last 12 months, where a monthly peak below 2.5 kW counts as 2.5 kW; so peaks below 2.5 kW cost nothing extra. Wallonia, Brussels, the Netherlands and other countries have different rules: look up the current rules yourself at the official source, with source and date, and do not simply copy the Flemish rules.)
- Single-phase or three-phase, 230 V or 400 V, how many amps main fuse (per phase)?
- Which contract type? Options: fixed; variable (monthly index); dynamic (price per hour or quarter hour, e.g. based on the day-ahead market); day/night; exclusive night. Do I have the price formula or a recent bill (a photo is fine; do not copy personal data)? If I only know the name of the supplier and contract: look up the official tariff sheet yourself (mind the right month, region and contract version) and let me confirm it against a bill.
- Fixed costs (subscription, data management, meter rental) per year, so that savings are calculated fairly.
- Feed-in: is there compensation, fixed or variable? Do I pay for feed-in at negative prices? Is there a feed-in tariff or a maximum feed-in power set by the grid operator?
- Am I considering a dynamic tariff? Honest warning up front: without a battery or shiftable consumption (car, heat pump, water heater) a dynamic tariff often yields little or costs more, and there are outliers (expensive winter evenings, crisis years). How much risk do I want to take? Am I willing to shift consumption myself (washing machine, dishwasher)?
- Do I still have an old arrangement (e.g. a meter that runs backwards, prosumer tariff, green energy certificates)? That changes the calculation completely.
- Does my supplier offer flexibility programmes (e.g. compensation for using less at certain times)?
- Do I take part in energy sharing or an energy community (sharing power with neighbours or family), or am I considering it? Then shared power counts differently in the calculation.
- Do I live in an apartment or building with shared installations (shared chargers, common meter)? Then I can often only measure and control my own part.
- Am I a tenant or co-owner? Then panels (including balcony panels), batteries, a charger or wiring often need permission from the landlord or the owners' association. Ask about it for every profile where something is installed, and look up the rules for my region (e.g. registering balcony panels with the grid operator).
- Day/night hours: which hours really apply? (In the example the grid operator's hours turned out different from what was expected; check with meter data against the bill or the grid operator's portal.)
- Municipality or region (for the solar forecast and the weather). Never store an exact address.

### Block C - Meter and measurements
- Do I already have a digital meter? If not (analogue meter): the options are requesting a digital meter from the grid operator (look up the conditions, costs and waiting time for my region), having a certified electrician install a clamp meter, or for now only calculating with annual readings and a standard load profile. Say what each option makes possible.
- Which digital meter and which reader? Options: HomeWizard P1 Meter; another P1 dongle (e.g. via ESPHome, DSMR-reader, Slimmelezer); a P1 cable directly on the machine; only the meter of the inverter/battery; a clamp meter (Shelly EM, ...). Reachable locally (IP address, local API available and, if needed, enabled or a token obtained)? Does a battery or inverter already use the same meter, and how (over the network from the same dongle, its own dongle on the port, its own clamp)? Outside Belgium, the Netherlands and Luxembourg: look up which port or reader the meters in my country have.
- Does the meter give power and current per phase? The running quarter-hour average and the monthly peak?
- Also measure gas and water? Other sub-meters (e.g. a separate meter for the heat pump)?
- How often do I want to measure (every 1-10 s is common) and how long to keep it (raw data e.g. 1-2 years, then summarised)?
- If I have no reader yet: give buying advice based on criteria, not brands. Important: a local API (works without the cloud), readings every few seconds, power and current per phase, preferably also the quarter-hour average and the monthly peak, powered by the P1 port or a plug, sharing measurements locally over the network with several readers (so that one dongle is enough for battery, system and Home Assistant), works without Home Assistant or the cloud, and good support in open-source software. Compare a few common types (ready-made dongle, ESPHome dongle, cable directly to the machine). Also say that the P1 port must be activated first (in Flanders via "Mijn Fluvius"; this can take a few days), and meanwhile start with the historical quarter-hour data as CSV.

### Block D - Solar panels
- Solar panels yes/no? Total kWp, number of roof sections each with orientation, tilt and kWp. Shade at certain hours?
- Make and type of the inverter(s). How to read them? Options: local Modbus TCP/SunSpec; local web API; Bluetooth via an ESP32 with ESPHome; Home Assistant integration; only via the cloud; not at all. Without solar measurement we control on the meter; that also works.
- Can the inverter be limited or switched off (useful with a negative feed-in price or a feed-in limit)? Do the grid operator and the installer allow that?
- Solar forecast: free Forecast.Solar (no account), Solcast (free account, more accurate), Open-Meteo (weather) or none. May the system correct the forecast itself with the measured deviation?

### Block E - Home batteries
- What kind of system? Options: separate battery/batteries on a wall socket or with their own inverter (AC-coupled, e.g. Marstek, Zendure); a hybrid inverter with battery (DC-coupled, e.g. Sungrow, Huawei, SolarEdge, GoodWe, Victron); a combination. With a hybrid system, the rules in "Hybrid inverters" below apply.
- Number of batteries, make and type, capacity (kWh), maximum charge and discharge power (W) per device, firmware version. Which phase is each device on (with three-phase)?
- Where are they? Indoors, or in an unheated garage or shed? (Below freezing, many batteries do not charge or only to a limited extent; the system must know this so it does not treat it as a fault in winter.)
- Safety and rules: are they not in an escape route, is there a smoke detector nearby, are they registered with the grid operator (mandatory in Flanders), and does the fire insurer know about them? The assistant does not check this itself, but asks and records the answer.
- Does the device install firmware updates itself (automatically via the app)? Can that be switched off? (In the example an automatic update changed the behaviour; the system must notice and report a firmware change.)
- How to control locally? Options: Modbus TCP over LAN; Modbus RTU (RS485 with an adapter); local UDP/HTTP API; via Home Assistant; cloud app only (then limited or not controllable). Cable (LAN) or Wi-Fi? Fixed IP address via DHCP reservation?
- Is something already controlling the batteries? Options: the device's own automatic mode (e.g. "self-consumption" with its own meter); an app schedule; Home Assistant automations; a dynamic contract with its own control; nothing. Important: only one controller may be active at a time. We switch the others off, and I note how to switch them back.
- How may they charge? Options: only from solar surplus (never from the grid); also from the grid at cheap hours (dynamic contract), but only if the sun will not fill the battery that day; also from the grid at negative prices.
- How may they discharge? Options: only for own consumption, never to the grid; also to the grid at high prices (arbitrage); only to shave the 15-minute peak; not while a large device (car, heat pump) is running.
- Minimum state of charge (SoC): fixed, or different in summer/winter? Reserve for power cuts (only if the device can supply backup power)? Maximum state of charge to spare the battery (e.g. 90%)?
- May the batteries supply the car? (In the example: no, the batteries are for the house.)

### Block F - Electric car(s)
- Electric car yes/no? How many cars and how many chargers?
- Charger: make and type. Locally controllable via MQTT, HTTP API, Modbus or OCPP? Can it switch between 1 and 3 phases? Minimum and maximum current?
- Car: make and type, battery capacity, consumption (kWh/100 km). Can the state of charge/range be read locally? Options: TeslaMate (Tesla); the brand's Home Assistant integration; via the charger (usually not); not at all (then we estimate the state of charge from the charged kWh and the consumption).
- Charging strategy, choose one or combine: solar surplus only; minimum + solar (always at least the minimum, the rest on solar); minimum range (below X km always charge, also from the grid); departure time + target (e.g. 80% at 7:30, as cheaply as possible, less at night if tomorrow is sunny); cheapest hours (dynamic contract); trip mode (once up to 100%); always maximum; manual (the EMS only watches).
- With several cars or chargers: which one gets priority?
- Is the charger or the car only reachable via the manufacturer's cloud? That is possible, but see the rule on cloud devices.
- Can the car and charger feed power back to the house or the grid (bidirectional charging, V2H/V2G)? Now or in the future? Then the car is also a home battery and belongs in the battery rules.
- Limits: maximum grid power or current for the car; stay within the quarter-hour budget of the capacity tariff; per phase below the main fuse.

### Block G - Other controllable appliances (optional)
- Heat pump (SG-ready input?), electric water heater (possibly with adjustable power or as a heat buffer), air conditioning, pool or pond pump, tumble dryer/washing machine/dishwasher, smart plugs (Shelly, Tapo, ...), electric heating.
- Per appliance: power, may it be shifted, within which hours, minimum running time per day (e.g. pump 6 h, even if there is no sun), minimum on and off time.
- Heat pump: comfort limits. Minimum and maximum indoor temperature (day/night), hot water (minimum temperature, when must it be ready), underfloor heating or radiators, how well the house retains heat (how many degrees does it drop per hour without heating?), and may the weather forecast be used? Comfort always comes before savings.
- Does an appliance still need wiring (e.g. a relay on the SG-ready input, a sub-meter, a current clamp)? Then the assistant says exactly what is needed, but a certified electrician installs it; the system only controls it once it is installed.
- One priority list for everything (cars, appliances and battery), in an order I choose myself and can change later. Default: car > water heater/heat pump > battery > grid.
- Appliances already controlled by the tariff or a relay of the grid operator (e.g. night storage heaters or a water heater on exclusive night): recognise them, do not control them twice, and count their consumption on the right register.
- Appliances I do NOT want controlled, but which do affect consumption (useful for explanations in reports): e.g. microwave, electric heater, heat exchanger, induction hob.

### Block H - What is already running and what do I want to see
- Where does it run? Options: an ordinary Linux machine (Debian/Ubuntu; recommended); the same machine as Home Assistant OS (then: (a) a separate small machine next to it, (b) everything as a Home Assistant add-on or in Home Assistant itself with AppDaemon or pyscript, or (c) move Home Assistant to Docker on an ordinary Linux machine); a NAS with Docker; a virtual machine (Proxmox etc.); a Windows PC with WSL 2 (Linux under Windows; suitable for measuring, for control only with the conditions below). Explain the pros and cons and adapt phase 2 and the plan to that choice.
- Linux distribution, is the machine always on, sudo rights, Docker present, free disk space? Is it on a UPS? Does it restart by itself after a power cut (BIOS setting)?
- With WSL 2: enable systemd (`systemd=true` under `[boot]` in `/etc/wsl.conf`); have WSL start when Windows starts (e.g. a Task Scheduler task that runs `wsl` at startup, even without logging in); disable WSL's automatic shutdown when idle (in `%UserProfile%\.wslconfig`; the setting depends on the WSL version: let the assistant look it up); Windows sleep and hibernation off; choose a time for Windows Update restarts. Network: in the default mode (NAT), WSL is not reachable from the home network and automatic device discovery (mDNS, e.g. by Home Assistant) does not work; on Windows 11 choose `networkingMode=mirrored` in `.wslconfig`, or a port forward in Windows. Outgoing connections to the devices (P1 meter, battery, charger) work in both modes. Because Windows can restart the PC unexpectedly, a failsafe is mandatory when controlling, and only devices with their own timeout or fallback in the device itself then stay safe (see "Outages" in phase 4).
- Home Assistant present or wanted? MQTT broker (Mosquitto)?
- Dashboard: own web page (Flask), Home Assistant dashboard, Grafana, or a combination? Do I already have dashboards or a database (Home Assistant energy dashboard, Grafana, InfluxDB)? Then they are reused and extended instead of building something new next to them.
- For programmers: do I want the code in my own Git repository (e.g. on GitHub or GitLab), with tests that run automatically (CI)? Secrets then certainly not in the repository.
- Notifications via: e-mail (SMTP server, preferably an app password), SMS, WhatsApp or Signal (via a bridge or service; look up a reliable, preferably free option), the Home Assistant app, Telegram, ntfy, or none. I only give passwords and tokens when you need them; they go only into `.env`.
- Who gets which notifications (resident, helper, several family members)? E.g. technical alarms only to the helper, a simple overview in plain language to the resident. Quiet hours at night, except for real alarms?
- Reports: daily PDF report (what time?), weekly/monthly, by e-mail or only as a file?
- Backup: to a NAS, external disk or cloud (e.g. with restic)? How often?
- Remote access: none, via a VPN (e.g. Tailscale/WireGuard), or via Home Assistant Cloud? Never open ports in the router without explicit approval.
- Does a non-technical family member also use the system? Then a simple one-page explanation is added.
- Who may see the dashboard and who may change something? Everyone on the home network (including guests on the Wi-Fi), or only with a password? Is there a guest network or a separate network for smart devices?
- Do I want an external "heartbeat" monitor (e.g. the free service healthchecks.io), which warns me if the whole machine stops? The system's own monitoring cannot report that if it is no longer running itself.
- Do I want to be able to download my data as CSV or Excel for my own calculations?

### Block I - Display and readability
- Am I (or someone who reads the charts) colour-blind? Options: no; red-green (most common); blue-yellow; completely colour-blind; I don't know. With "I don't know" or doubt: choose colours that work for everyone (e.g. blue/orange instead of red/green).
- Regardless of the answer: in charts and dashboards never use colour as the only carrier of information. Also use hatching, line style (solid/dashed/dotted), symbols and text labels, and check every chart in greyscale too.
- Do I mainly read the dashboard on a phone, tablet or computer? Large letters needed? Light or dark theme?
- Do I prefer reading reports on paper? Then: A4, large font, high contrast, readable as a black-and-white print (no information only in colour), and at the top the most important conclusion in one sentence in plain language.
- Numbers and times: decimal comma or point, 24-hour clock, kW or W, date as day/month?

### Block J - Advice before buying (if I have nothing or little yet)
Data:
- Which consumption data are available? Options, from best to least good: quarter-hour data from the digital meter (in Flanders downloadable via "Mijn Fluvius" as CSV, preferably at least a full year); a P1 reading we start now (then first measure for a few weeks or months); monthly readings or the annual bill (then we calculate with a standard load profile, less accurate: say so in every result). Do I already have history in another system (Home Assistant statistics, InfluxDB, the export of an inverter or battery portal)? That is often the best source: import it, checking for gaps, units and time zone.
- Gas consumption per year (for a heat pump calculation) and how the house is heated.

My situation:
- How many people, who is home during the day (working from home), when is there cooking, washing, drying?
- Owner or tenant? How long will I probably live here? (An investment that only pays back after 12 years is worth little if I move in 5 years.)
- Plans: electric car (when, how many km per year, when is it at home: during the day or only in the evening and at night?), heat pump, air conditioning, working from home, a growing family?
- Budget, and which payback time do I find acceptable? Borrowing or own savings (interest or lost interest counts)?

Solar panels (if I do not have them yet):
- Roof type, orientation, tilt, usable area, shade (trees, chimney, neighbours). Location (municipality) for the solar simulation, e.g. with PVGIS (free tool of the European Commission, hourly production for a location and orientation).
- Quote(s) available? Price per kWp, inverter type.

Batteries (if I do not have them yet):
- Which types am I considering? Options: plug-in battery (e.g. Marstek, Zendure, Anker; simple, one phase, limited power); home battery with hybrid inverter (by an installer, more power, sometimes backup power); combination with new solar panels.
- Price per kWh (incl. installation and VAT), warranty (years and/or cycles), own standby consumption (W; it counts: 15 W continuously is about 130 kWh per year), round-trip efficiency, minimum state of charge, maximum charge and discharge power, location (indoors or in a cold room).
- Rules: must the battery be registered with the grid operator? Are there subsidies or a VAT arrangement? Are there restrictions for plug-in batteries? Let me check that at the official sources; do not give outdated subsidy information as fact.

Contracts:
- Which contracts do I want to compare? My current contract, one or more dynamic contracts, and possibly offers I received. In Flanders the V-test of the Vlaamse Nutsregulator (Flemish utility regulator) is the official, independent comparison tool. It can be linked to Mijn Fluvius, work with an uploaded CSV of at least a year of quarter-hour data, or calculate with an entered annual consumption and standard profiles. It can show dynamic contracts that way too, but with real quarter-hour data the comparison for my consumption pattern is much more accurate. Use the V-test (preferably with quarter-hour data) as an independent check of your own calculation, and explain differences (price assumptions, contract terms, period).

At the end, summarise everything in one overview and let me confirm or correct it. Save that overview (without secrets) as `installation.md` in the project folder.

## Phase 2 - Checking the machine (read only)

Check without changing anything: OS and version, Python 3, free disk space, Docker, systemd, time zone and time synchronisation (NTP; times in reports must be correct), whether the specified devices are reachable (ping, port open), which ports are open and to whom (firewall, Docker containers; with WSL also the network mode, systemd and the Windows firewall), and whether the meter already provides data. For the meter specifically: read one measurement and report which fields are present (power, current and voltage per phase; import and export registers per tariff; running quarter-hour average and monthly peak), how many seconds there are between new values, whether the sign for feed-in is correct (compare with the sun or the app), and whether the number of phases matches block B. Say what is missing and which modules therefore cannot work or work less well (e.g. no current per phase: no main fuse monitoring). If the quarter-hour average or monthly peak is missing: calculate them yourself from the import register (quarter hours on the clock) and mark quarter hours with missing or incomplete measurements. Do not store the meter number or serial number outside `.env`. Check whether other software is already running that talks to the same devices (duplicate connections). If Home Assistant is already running: list the integrations and automations that read or control the devices involved, without changing anything. Report what is missing and what I need to do myself (e.g. enable the local API in an app or obtain a token, DHCP reservation in the router).

## Phase 3 - Proposing a plan

### First: build it yourself or use existing software?
Weigh it up honestly and present the choice to me:
- **Existing packages**: evcc (car charging, supports many chargers and cars, own web interface; for some chargers a paid "sponsor token"), EMHASS (planning of battery and shiftable appliances on price and forecast, via Home Assistant), Predbat (battery planning on dynamic tariffs, strong in the UK), SEM and PV Excess Control (distributing surplus, Home Assistant). Combinations are also possible, e.g. a planner that decides and evcc that carries out the charging.
- **Build it yourself** (like the example system): full control, also for devices or rules that packages do not know (e.g. a battery via Modbus without an integration, the Flemish capacity tariff), but more maintenance.
- **Hybrid**: an existing package for what it does well, own modules for the rest. Make sure two systems never control the same device.

### Then: the plan
For the profile "advice before buying" the plan is short: read in the data (or first measure for a while), module 19, and an advice report; nothing is controlled and nothing in the house is changed. For the other profiles: propose a plan with only the modules that fit my installation and choices (catalogue below), in order, with for each step: what it does, what changes on my machine, and how we check that it works. Mention which settings in devices or apps I need to change myself and how I change them back. Wait for my approval.

### Catalogue of modules (all optional except 1)
1. **Reading and logging the meter** (mandatory, except for advice before buying with existing data): every few seconds, with quarter-hour average, monthly peak and current per phase if the meter provides them.
2. **Dashboard**: live power, 24 h/7 d chart, batteries, solar, car, costs, and what the system is doing now and why (in plain language).
3. **Solar**: measuring and/or forecasting, with a daily comparison and possibly automatic correction of the forecast.
4. **Consumption forecast**: predicting household consumption per weekday and hour from its own history (days away excluded). Needed for any battery planning.
5. **Prices**: day-ahead prices (e.g. via ENTSO-E, free token needed) or the price formula of my contract; possibly the CO2 intensity of the grid.
6. **Reading the batteries**, including temperature and health.
7. **Controlling the batteries** (on surplus, possibly on price and/or 15-minute peak).
8. **EV control** (solar, minimum + solar, minimum range, departure time, cheap hours, trip mode).
9. **Switching other appliances** (water heater, heat pump, pumps, smart plugs).
10. **Monitoring the main fuse per phase.**
11. **Manual intervention with an end time** (temporary override, then automatically back to automatic).
12. **Away mode.**
13. **Cost calculation** according to my contract, with counters per day/month, including fixed costs.
14. **Reports** (daily PDF, weekly/monthly).
15. **Monitoring with notifications**.
16. **Home Assistant integration** via MQTT Discovery.
17. **Backup** and **emergency stop** (safely stop all automatic control; no factory reset).
18. **Analyses** afterwards: what do the batteries and the control really yield, does an extra battery pay off, payback time.
19. **What-if and advice** (also without an installation): tariff comparison, shadow bill, and simulations of solar panels, batteries (how many?), smart charging and a heat pump with my own consumption. Result: an advice report (PDF).

## Phase 4 - Building

### Basic principles
- One project folder (e.g. `~/ems`) with a Python venv and a git repository. An `AGENTS.md` in that folder that you keep up to date: what is running, why, settings, lessons learned, with dates. That way a next session can continue without figuring everything out again.
- **Core rules in `AGENTS.md`**: many agents load their notes file automatically every session, but not this prompt file (and after a long conversation is summarised, detail can be lost). If you work in a chat, you upload it yourself. So put a short section "Rules and choices" at the top of `AGENTS.md`: the hard limits (see below), my preferences (e.g. never charge from the grid, priority list, comfort limits), the working agreements, and a reference to `installation.md` and this prompt file. At every new session, first read `AGENTS.md` and `installation.md` before doing anything, and update that section when I change a choice. Whether an agent reads its notes file automatically differs per agent and per version: at the start of every session check that the rules were really loaded, e.g. by having the assistant briefly repeat the hard limits and my most important choices.
- Secrets (tokens, passwords) only in `.env` (in `.gitignore`). Settings in `config.yaml`, with a `config.example.yaml` without secrets.
- Each component its own systemd service or timer with automatic restart; everything starts by itself after a restart of the machine. Timers that run daily: be careful with `Persistent=true` (after a reinstall it can immediately start a "missed" run with an incomplete day).
- Everything works locally, also without internet. Only prices, forecasts and notifications need internet; if it drops out, the system keeps controlling safely on the meter.
- MQTT broker and Home Assistant (if wanted) via Docker Compose. Each MQTT client gets a unique client_id (the same id = clients kick each other out). Broker with a password.
- Storage in SQLite (times in UTC, WAL mode on), one row per measurement. Always show times in local time.
- Each module gets tests, each control rule a test with a realistic scenario from the real measurements.
- **Tariffs with a validity date**: do not put grid tariffs, levies, VAT and fixed costs in the code but in one file with "valid from/to" and the source per period. Every point in time is calculated with the period that applied then (so a recalculation of last year does not use this year's tariffs). A reminder in December as long as next year's tariffs are missing, and an alarm as soon as the last period has expired; the calculation then visibly continues with the old values.
- **Observation mode (dry run)**: every module that controls something has a switch with which it only logs and shows what it would do. New control first runs like this for at least a day; then we compare what it would have done with what happened.
- **One controller per device**: before you start controlling a device, check that nothing else still controls it (app, Home Assistant, the device's own logic, another package). There are two clean solutions: switch the other controller off, or work together with it through its own API (e.g. give evcc a charging mode or plan and let evcc carry out the charging). Record who decides and who executes.
- **Read and control through what already exists**: if Home Assistant (or another system) already talks to a device, use that route (the Home Assistant API or MQTT) instead of opening a second direct connection. Many devices accept only one connection, and two systems talking to the same device cause errors that are hard to find.
- **An explanation for every decision**: every control decision gets a short reason in plain language ("Battery not charging: car has priority, surplus 2.1 kW"), visible on the dashboard and in the logs.
- **Emergency stop**: one command or dashboard button that safely stops all automatic control and puts each device in its pre-tested safe state. Work with a flag (e.g. a file) that the control itself also reads: as long as it is set, no component executes normal control commands any more, not even after a restart, while measurements, dashboard and reports simply continue. The safety layer may (and must) keep sending and checking the commands needed to keep each device in its safe state (e.g. for a battery without fallback: periodically standby 0 W again). In addition, the emergency stop itself writes directly to the devices (independently of the control programs), reads back the actual state, checks again after half a minute whether nothing has taken control back, and reports the result (e-mail). As long as the emergency stop is active: a red bar on the dashboard and a reminder via the monitoring, so it is not forgotten. Define per device what the safe state is, how to get there and how to read it back (e.g. charger: stop charging; battery: by default standby at 0 W; the device's own mode only if a real test with monitoring has proven that it is safe: in the example system a battery in "self-consumption" discharged 2.5 kW to the grid within 10 s, while the app showed the grid correctly). A second command lifts the emergency stop. After lifting it, control never restarts with an old setpoint or an old plan: first check fresh meter values, the state of each device and the safety limits again, then calculate a new plan. Test both at handover.
- **Safety layer**: one central component with priority over all modules (battery, car, heat pump, ...) has the final say on what each device may do. Before every command it checks the hard limits (fresh and valid data, current per phase, maximum powers, temperature, communication with the device, emergency stop flag, overrides) and on a violation requests the pre-tested safe state. This check runs in every control cycle (seconds) and intervenes immediately by itself; it never waits for the monitoring. That way not every module reacts in its own way to e.g. missing meter data or too high a phase current. This layer runs on the same machine and therefore does not replace protection in the device itself.
- **Outages: three cases**, each with its own answer. (1) **A program fails or hangs**: systemd restarts it, a stop action (e.g. ExecStopPost) and a separate timer put the devices in their safe state. (2) **The network fails** (router, Wi-Fi, cable): the machine still runs but cannot reach the devices; the system keeps retrying and reports it, but cannot make safe what it cannot reach. (3) **The whole machine fails** (power, hardware fault, Windows restart with WSL): then nothing intervenes at home any more. Monitoring or a failsafe on the same computer does not help then; only a timeout or fallback in the device itself, or a second independent device, protects then. Use such a timeout where the device has one, say honestly which devices have none (they then keep executing their last command), and make sure through the external heartbeat that I know quickly. A notification is not protection: a device without its own timeout is not outage-safe under external control. So never present live control of such a device as outage-safe. For each such device, choose one of two routes. (a) Provide an independent fallback and really test it: e.g. a separate, tested controller that puts the battery in the safe state when things go quiet, or a watchdog in the device itself. (b) Or record the remaining risk in `AGENTS.md` (what can happen, for how long, at what power) and let me choose explicitly whether I accept it. A UPS does not count as an independent fallback: it only bridges a power cut of the machine and the network, and does not help with a hung or broken computer or a network problem.
- Before every change to settings or code: a backup of the old file (with the date in the name) and a note of how to roll back.
- Updates of the system itself (Python packages, Docker containers, Home Assistant): never automatic; only after approval, preferably at a quiet moment, with the possibility to go back. Exception: operating system security updates may be automatic (e.g. unattended-upgrades), without automatic reboot.
- **Security**: a firewall on the machine. Basic rule, the same on every platform: allow everything from the home network and the VPN, close everything else, and open nothing in the router. Shielding per service more strictly (e.g. MQTT or Modbus local only) is possible, but optional. Always load new firewall rules with an automatic fallback (without my confirmation within 5 minutes the old rules come back), so that I cannot lock myself out; always keep SSH and the VPN open. Per platform: Debian, Ubuntu and Raspberry Pi OS with ufw or nftables (open by default); ports of Docker containers bypass ufw and the normal INPUT rules, so shield them in the DOCKER-USER chain or bind the port only to the necessary address; with WSL 2 the Windows firewall (and the Hyper-V firewall for WSL) is the real gate, a firewall inside Linux protects little there. Furthermore: dashboard, Home Assistant and MQTT broker with a password; never expose anything directly to the internet; SSH with keys only. Never put tokens and passwords in git, logs, reports or e-mails.
- **Summer and winter time**: calculate internally in UTC. A day with the clock change has 23 or 25 hours (92 or 100 quarter hours); reports, 15-minute peaks, daily totals and imported CSVs (often in local time, with a double hour in October) must handle that correctly. Test it with the real changeover days. Pitfall from the example system: never use a local time as the key to group quarter hours or hours. In Python, two local times with the same time zone are equal if the clock shows the same (02:15 summer time = 02:15 winter time), so the two quarter hours of the double hour are silently merged and averaged. Group in UTC and convert only for display. A UTC time around midnight belongs to the local day (e.g. for the tariff of 1 January).
- **Data quality**: recognise gaps in the measurements (outages), counters that jump back to zero (meter replaced, restart) and impossible values, mark them and do not blindly include them. With imported data: check the decimal comma, units (kWh or Wh) and time zone.
- **Database maintenance**: summarise raw data after the chosen retention period (e.g. per quarter hour), clean up the WAL file regularly, limit log files (journald), and monitor disk space.
- **External services**: respect the limits of free services (e.g. Forecast.Solar a few requests per hour), cache results, and let the system simply continue if a service does not respond.
- **Replay tool**: a script that replays a control rule on real historical measurements (without hardware), so that a change is first tested on past days before it goes live.
- **Changing an existing Home Assistant**: first a full backup; own settings in a separate package file (e.g. `packages/ems.yaml`) and not in existing files; do not change existing automations, scripts or dashboards without approval; have the configuration checked before every restart; and note how to roll everything back.
- **Rebuildable**: everything needed to restore the system on a new machine (code in git, `.env`, configuration, database from the backup, systemd units, Docker files) is described in `AGENTS.md`.
- **A backup that can really be restored** (lessons from the restore test in the example system):
  - Never simply copy databases as files while they are being written to. First make a consistent copy and back that up: SQLite with `VACUUM INTO` (one read transaction, a few seconds). `sqlite3 .backup` is also a consistent method, but copies in chunks and restarts as soon as another program writes; with a database that is written to every few seconds, it never finished in the example. PostgreSQL (e.g. TeslaMate): with `pg_dump`. Check the copy (`PRAGMA quick_check`) before the backup.
  - Include everything needed for a rebuild, not just the project folder: also the systemd drop-ins (`*.service.d`, which contain the failsafes on stop), the backup script itself, sudo rules, Docker Compose files of other containers, configurations of ESP modules and your own modifications to them. Leave out rebuildable things (Python environment, build cache), but test that they can be rebuilt.
  - The password of the encrypted backup must not exist only on the machine itself: if that disk fails, the backup is unusable. Have the user keep it in a password manager or on paper, and never show it in a report or e-mail.
  - Really test restoring, once in full (to a separate folder: restore time, integrity of the databases, configuration present, rebuilding the Python environment from `requirements.txt` and passing the tests) and then automatically every month (`restic check` with part of the data, restore and check the database copies, age of the last measurement, e-mail with the result). Delete the test folder afterwards: it contains a copy of all passwords.

### Order (first make each step work and show it, only then the next)
1. Reading and logging the meter.
2. Dashboard, according to the choices in block I (colour blindness, device, font size, theme).
3. Solar, prices and consumption forecast.
4. Batteries and other controllable devices READ ONLY, for at least a day, and compare with the app.
5. **Safety before control**: safety layer, emergency stop (stopping and resuming), failsafes (on stop and via a separate timer), monitoring with notifications, external heartbeat, backup and a described recovery procedure. Everything works and has been tested (emergency stop and failsafe once for real, while I am present) before even one device is controlled live. For this, controlled manual hardware commands are allowed while I am present: they are real actions on the device, but not automatic control (that is still off then). Record the power limits, the expected result and the recovery procedure in advance. A test from 0 W does not prove that the emergency stop or failsafe can end an active charge or discharge command: so first set a small power manually (e.g. 300 W charging or discharging), check that the device executes it, and test the transition to the safe state from there. Then also discuss which devices are not outage-safe (see "Outages") and record my choice.
6. Controlling the batteries: first observation mode (at least a day), then one device at low power while I am present (check sign and response), then live.
7. EV control, in the same way.
8. Other appliances, in the same way.
9. Costs and reports.
10. Home Assistant integration, analyses, explanation for family members.
11. Evaluation after 1 week and after 1 month (see below).

## Rules and lessons

### Control in general
- Never control on old data. If the last meter value is older than about 30 s: batteries to their safe state (usually standby 0 W), stop forced charging of the car, and warn. Do a rollback after every failed database write (otherwise a connection stays stuck on an old snapshot and the system controls on that old value for hours).
- Always explicitly send an end state (e.g. 0 W) when nothing is allowed. "Sending nothing" makes many devices continue the previous command forever.
- Dampen noise: control on a meter average over about 10 s (no longer than the control cycle, otherwise an import counts twice), with a hysteresis (about 200 W) and a minimum time between changes of direction (about 180 s). Without that, devices switch back and forth dozens of times per hour. That waiting time and hysteresis apply only to switching to the other direction: charging or discharging less, going to 0 W and every intervention of the safety layer always happen immediately (see the rules on grid charging and discharging to the grid below).
- An "operating point": keep a small margin (e.g. 50-100 W import) instead of exactly 0 W, so that small fluctuations do not cause feed-in or grid charging.
- Watch out for two control loops reacting to each other through the same meter (e.g. a battery and a charger that each have their own logic): that causes oscillations of thousands of watts.
- Priority of solar surplus according to the one priority list from block G.
- Recalculate plans as soon as something changes (new prices, new forecast, car plugged in) and check them briefly once more just before a cheap window ends.
- After a restart: ignore or smooth jumps in counters (kWh, costs), and wait for fresh measurements before controlling.
- After a power cut: the machine, the router and the devices do not start up in the same order. The system keeps trying to connect (without crashing), only controls when all necessary data are fresh, and checks whether devices are in the expected mode (some fall back to their factory mode).
- Read the firmware of every device periodically (where possible) and send a notification if it changes.
- Never write to a register or setting of a device that you have not found in documentation or a reliable source, and never "to try". Exploring is done read-only. A wrong write can change settings you cannot find again.
- Some settings are stored in a device's flash memory, which wears out after thousands of writes. Only write settings on a real change; only setpoints intended for it may be repeated every cycle. When in doubt, find out what kind of register it is.
- Follow the grid voltage per phase (the meter usually provides it): at too high a voltage (in Belgium above about 253 V) inverters switch off and solar yield is lost. Show it in the report; charging at that moment helps to lower the voltage.
- Test the failsafe and the emergency stop now and then (e.g. every month); a safety mechanism that is never tested often does not work when it is needed. Automate the read-only part (e.g. weekly, e-mail on deviation): are the failsafes on stop still loaded, are the failsafe timers on, are the registers the emergency stop needs readable, does a dry run of each failsafe succeed, and is there no forgotten emergency stop flag. You test the real intervention by hand, while you are present.
- Present unexplained patterns first: often it is an ordinary appliance in the house (microwave, heater, heat exchanger, pump), not a fault. The weather also explains a lot: snow or dirt on the panels (solar far below the forecast), heat, thunderstorms with grid disturbances.

### Main fuse per phase
- Separately from the capacity tariff: monitor the current per phase. If the car, heat pump and other appliances together exceed the main fuse on one phase (with a margin, e.g. 90%), first reduce or stop the controllable loads on that phase. Even if the quarter-hour average stays low.
- The size of the main fuse is not always on paper: derive it from the contracted capacity at the grid operator (e.g. "Mijn Fluvius"): 17.3 kVA three-phase = 3N400 V with 25 A per phase; 9.2 kVA single-phase = 40 A; 3x230 V with 40 A = 15.9 kVA. Ask if it does not add up.
- Store the current per phase (with sign: feed-in loads the fuse just as much) and the voltage per phase with every measurement; many P1 readers provide them, but they are easily thrown away. The limiting itself happens immediately, in every control cycle, by the safety layer; the monitoring below only reports. Monitoring: warning at > 80% of the fuse for 1 min, alarm at > 100% for 30 s, and grid voltage outside 207-253 V (230 V +-10%) for 1 min (too high a voltage makes inverters switch off). At every check, look back about 10 minutes, so that even a short event is certainly reported.

### Batteries
- Calculate the surplus yourself from the meter (negative = feed-in) and distribute it over the batteries, e.g. by remaining capacity. Do not let devices each run their own automatic mode: they do not coordinate and work against each other.
- Never charge from the grid (if that was chosen): as soon as there is import while the batteries are charging, reduce charging immediately by exactly that import, without delay or damping.
- Never discharge to the grid (if that was chosen): on feed-in, stop discharging immediately.
- When charging: use the higher of the 10 s average and a 4 s average, so that a cloud quickly leads to less charging. Let the charge power rise only a limited amount per cycle (about 250 W per device); less charging is always allowed immediately.
- Limit charging to the measured solar production if it is known.
- Many devices have no automatic return in a "passive" or "remote" mode: repeat the setpoint every cycle, and on stop explicitly put them in their pre-tested safe state (see "Emergency stop"; that is not always the device's own mode).
- Sign (charging negative or positive?) and capacity: try to recognise them automatically from the measurements, but always check with a small power on real hardware and let me confirm before anything controls continuously.
- Some devices stop discharging by themselves at an SoC limit and only resume a few percent higher. Learn that limit from the measurements and do not request discharge power in that zone.
- Temperature: at low temperatures many batteries charge in a limited way; show that as an explanation, not as a fault.
- Many batteries accept only one Modbus connection at a time: use a small Modbus proxy with a timeout (e.g. 5 s), otherwise one hanging request blocks everything. Also limit the queue (drop old requests instead of piling them up) and let the proxy itself close and reopen a hung connection to the device. Only the EMS talks to the proxy.
- Store three things separately per device and per cycle: the requested setpoint, the actually measured power and the mode the device itself reports. "Write succeeded" does not mean the device does what was asked: compare requested with measured every time and report a persistent difference (limit in the app, wrong mode, stalled communication). Give every kind of command per device an adjustable verification period (battery: a few tens of seconds; charger: about a minute; heat pump: minutes) and a predefined safe action if the device does not do what was asked within that period. A device going the wrong way (discharging while charging or 0 W was requested, or the other way round) goes to its safe state immediately.
- Firmware updates can change behaviour (and some devices update themselves via the cloud). Record the firmware version, have the monitoring read it every hour and report when it changes, check the behaviour after every update, and with several devices update one first.
- If discharging stays too low: first look at power settings in the manufacturer's app.
- Follow health: number of full cycles, temperature, and (if the device provides it) capacity/State of Health per month.
- Calibration: some batteries need to charge fully now and then to keep the state of charge accurate, others do it themselves or do not need it. Look up per battery what the manufacturer prescribes and follow that; only if the manufacturer asks for it (or the state of charge demonstrably drifts), periodically plan a full charge on a sunny day, also when a maximum (e.g. 90%) is set. A state of charge that suddenly jumps can be a sign that calibration is needed.
- In heat, batteries sometimes limit their power; show that, as with frost, as an explanation.

### Price-based control (only with a variable or dynamic contract)
- Fetch the day-ahead prices (per quarter hour or hour; tomorrow's usually available from early afternoon) and convert them with the formula of my contract. Decide on the marginal price: what one extra kWh of import costs (or of feed-in yields) in that quarter hour, so energy plus the per-kWh grid costs and levies plus VAT, not on the bare market price. Fixed costs per year or month do not count in it; the capacity tariff comes in through the peak rule below. For the bill and the shadow bill you do calculate with all costs.
- Charging the battery from the grid (if chosen): only if the difference between cheap and expensive hours is larger than the losses (round-trip efficiency usually 80-90%) plus a wear cost per kWh. Do not charge from the grid if the solar and consumption forecasts say the battery will fill up that day anyway. Take the 15-minute peak into account: grid charging must not raise the monthly peak.
- Discharging the battery at expensive hours: keep enough for the most expensive evening hours (according to the consumption forecast); discharge to the grid only if that was chosen and the contract rewards it.
- Negative prices: shift consumption to those hours (battery, car, water heater), and possibly limit the inverter if feed-in then costs money (only if allowed and possible).
- Car: with a departure time and target, choose the cheapest hours that are still sufficient in time; charge less at night if a lot of sun is forecast for tomorrow; always keep a minimum range.
- Optional: control on the CO2 intensity of the grid instead of (or next to) the price.
- Show the plan (which hours to charge/discharge and why) in a table or chart on the dashboard.
- Make an overview per day: what the price-based control yielded compared with plain self-consumption. If the gain is small, say so honestly.

### Capacity tariff (Flanders; other regions: check their own rules)
- Calculation rule (Flanders, check the current rules): the bill uses the average of the monthly peaks over the last 12 months, with at least 2.5 kW per month. A higher monthly peak therefore stays in that average for 12 months, also across the turn of the year; a peak below 2.5 kW costs nothing extra. Let the system calculate the cost of a peak over those 12 months, and let the cost counter use the rolling average, not the peak of the current month. On the bill: with monthly billing, the average monthly peak of that month is charged (that is the 12-month average as it applies in that month, not that month's own peak); with annual billing, the billing peak, the weighted average (by number of days) of the average monthly peaks over the billing period. For an exact shadow bill use the real billing period, and check against a bill and the monthly peaks in the grid operator's portal.
- Controllable loads (car, grid charging, water heater) must never bring the current quarter hour above max(2.5 kW, monthly peak so far), minus a small margin. A higher limit is not a goal.
- Use the quarter-hour average of the meter itself (quarter hours on the clock; if the meter does not provide it, calculate it from the import register) and calculate what is still allowed so that the quarter hour ends at the budget. Stop or reduce quickly (within a few seconds) if the quarter hour threatens to go over; at the end of a quarter hour, do not use saved-up room any more. A quarter-hour value the system calculates itself (from the register or from power measurements) is provisional: the validated quarter-hour value of the grid operator (e.g. in Mijn Fluvius) is the final one and counts for the bill. Show that distinction, compare both after a few days, and control with a small margin.
- Discharging the battery to shave a peak can be an option (block E).
- Show the top 5 quarter-hour peaks per day and the monthly peak in the report.

### Car (only with an EV)
- Modes (depending on the choices in block F): "solar" (surplus only; start when the surplus stays at least the minimum charging power + about 200 W for a while, stop after about 200 s of import), "minimum + solar", "must" (below the minimum range: from solar or grid, within the quarter-hour budget), "departure time", "cheapest hours", "trip" (up to 100%, via an MQTT switch or dashboard button, switches itself off when the car is full), "always maximum", "off". Range unknown or outdated = the safe choice (solar).
- Batteries give way to the car (if chosen): do not discharge to feed the car, do not charge while the car needs the power. Do not subtract the car's power twice (the meter already includes it).
- Phase switching (if the charger can do it): 1 phase with little surplus, 3 phases with a lot. Only switch when it is not charging, with at least 15 min between two switches. For the choice, use the grid "as if the batteries were idle", otherwise a loop of starting, stopping and switching arises. If it stops on 3 phases while there is enough for 1 phase: restart quickly on 1 phase.
- Adjust the charging current within the budget (minimum usually 6 A per phase).
- Several chargers: distribute the surplus according to the priority list; never let two cars start at the same time.
- Recognise almost full: if the charging current decreases while there is room, the car is tapering; give the freed-up room to other appliances.
- Without a link to the car: estimate the state of charge from the charged kWh and consumption, and learn the consumption per km from the trips.
- Do not wake the car unnecessarily: do not request the status too often (that costs the car battery). TeslaMate does this well; with other integrations limit the polling frequency when the car is not charging.
- An independent failsafe (own timer, directly to the charger): if the EMS stops or no longer writes measurements, end forced charging and reset the current; also on every stop or crash of the main service.
- Log every change of the charger setting; restore unexplained changes and mention them in the report.
- The EMS usually cannot make a car start charging itself (that goes via the car or the app). Stop if the car draws nothing for a while and only try again later.

### Other appliances
- Per appliance: on at a surplus above its power + margin for a while, off on import, with minimum on and off times. Never switch an appliance on and off quickly (compressors and relays wear out).
- Daily targets: an appliance that must run a minimum every day (pump, water heater) also gets that when there is no sun, preferably at the cheapest hours or at night.
- Water heater as a heat buffer: turn surplus into hot water; with an adjustable resistor (diverter) this can be done steplessly.
- Heat pump via SG-ready or its own integration (possibly raising the setpoint a little on surplus), never by hard-cutting the power. Always stay within the comfort limits from block G: using the house as a heat buffer (heating a little more with sun or a low price, a little less with a high price) is only allowed within those limits, and take the weather forecast into account. When in doubt, heat.

### Hybrid inverters (battery DC-coupled)
- The battery sits behind the inverter and charges directly from the panels. You do not control the battery itself but the inverter: its working mode (self-consumption, forced charging or discharging, schedules), a charge or discharge limit, and the export limit. Find out which registers or settings are intended for that (manufacturer documentation, the common Home Assistant integration) and never write to others.
- The own self-consumption mode of a hybrid inverter usually works well and fast. Let it do the regular work and only intervene for what it cannot do (charging from the grid at cheap hours, holding back discharge for an expensive evening, 15-minute peak, priority for the car). Explicitly set it back after every intervention.
- Export limit and backup port (EPS/backup) are inverter settings and sometimes settings of the installer or grid operator: do not change them without approval.
- Many inverters store modes and schedules in their flash memory: do not rewrite them every few seconds, only on a real change.
- Losses: solar to battery (DC) is more efficient than charging via the grid (AC-DC); take that into account in the what-if calculations.

### Devices that only work via the cloud
- Allowed if there is no local route, but with these rules: login details only in `.env`; respect the limits of the cloud API (do not poll every few seconds); a notification if the cloud does not respond; and the device must remain in a safe state without the cloud (e.g. the charger's own schedule as a fallback). The failsafe cannot act directly on the device here: so set a safe default in the device itself (e.g. a limited maximum charging current, or no charging without an instruction).
- Say honestly that cloud control is slower and less reliable (delays of seconds to minutes, maintenance at the manufacturer, changed terms), and that quick adjustment to surplus or 15-minute peak is therefore less accurate. Use wider margins.
- Existing packages (e.g. evcc) already support many cloud devices; look there first.
- Do not keep reporting devices I deliberately do not use as "unreachable".

### Manual intervention and absence
- Temporary override with an end time, via the dashboard or MQTT: e.g. "car at full power for 2 h now", "do not use the battery for 1 h", "water heater on now". After that everything returns to automatic by itself. Show on the dashboard what is temporarily different and until when. From the example system: one command with a few fixed kinds (charge the car now, also from the grid, within the peak budget; do not charge the car; do not discharge the battery; away), each with an end time (default 12 h, away 7 days) in a small file that the control reads every cycle. Opposite kinds replace each other. "Charge the car now" also stops when the car is unplugged, but only if it was plugged in first: that way you can set it before you plug in the car. An e-mail on setting, stopping and expiry.
- Away mode (holiday): water heater and unneeded appliances off, do not cycle the battery unnecessarily, fewer notifications; do not count days away in the consumption forecast. Alarm on unexpected consumption, but first measure the base load: in the example system the house already used 0.5 kW at night (heat exchanger, appliances on standby), with half-hour averages up to 2.2 kW. A limit of 500 W would therefore alarm constantly. Use a half-hour average of the household consumption (grid + battery + solar) above an adjustable limit (2 kW there).

### Reports and monitoring
- Daily report (PDF, possibly by e-mail): batteries (min/max SoC, number of switches, temperature, and whether they charged from the grid after all), feed-in and import, solar measured versus forecast (also 7 days), top 5 quarter-hour peaks, car (sessions, grid share, cost, stop reasons), price-based control, errors and unexplained events, grid and SoC charts. A verdict ("OK" or "ATTENTION") with the precise reason. Spread long text over several pages, wrap long lines, and check yourself that nothing falls off the page.
- Key figures per day/month: self-consumption rate (share of own solar used yourself), self-sufficiency (share of consumption from own solar and battery), costs and savings, and the payback time of batteries and other investments.
- Tables: one row per measurement, no blocks next to each other.
- Monitoring (operational, separate from the safety check in every control cycle) every 2 min with a notification on problems (only after 2 times in a row), a reminder after 6 h and a "resolved" notification: services and containers active, meter, battery and solar data fresh, batteries discharging on feed-in or charging from the grid, 15-minute peak too high, phase overload, charger in error or unreachable, disk almost full, database too large, error messages in the logs (excluding known harmless noise).
- Heartbeat to the outside (recommended when controlling): the monitoring sends a ping to an external service at every run (e.g. healthchecks.io, free; only a ping, no measurement data); if it stays away for longer than about 10 minutes, the service warns me (e-mail, possibly a phone notification). Only that way do I notice that the whole machine or the internet has stopped. Test it once for real by briefly stopping the monitoring. Note: if the machine fails completely, nothing intervenes at home any more; devices without their own timeout (e.g. a battery under external control) then keep executing their last command. The heartbeat only makes sure I know quickly.
- Counters per device: number of successful and failed reads and the number of reconnects, so that a bad connection stands out before it really fails.
- Costs: calculate with the real contract formula and check against a bill. Record exactly how the contract calculates (e.g. a block of cheap kWh per month).
- Tariffs change: store every contract and every grid tariff with a start and end date, so that old periods remain calculated with the prices that applied then. Grid tariffs and levies usually change on 1 January: remind me every year and ask for the new values.
- Exporting a profile: an anonymised overview (devices, firmware, settings, without IP addresses, serial numbers or secrets) that I can share on a forum when looking for help.

### What-if calculations and advice (module 19)
- **Basis**: the grid consumption per quarter hour (or as fine as available) over at least a full year, because summer and winter differ greatly. If there are fewer data: say how uncertain the result is, and repeat the calculation when more data are available (e.g. after the first winter).
- **Tariff comparison**: price the same consumption series with each contract (fixed, variable, dynamic, day/night) with the real formulas, including fixed costs, feed-in compensation and capacity tariff. For dynamic tariffs: calculate with the real historical market prices per quarter hour/hour, and over several years if possible (price levels differ greatly per year): show a range, not a single number.
- **Shadow bill**: then calculate continuously every month what I would have paid with each contract, so that after a few months I can choose with real numbers.
- **Simulating solar panels**: hourly production for my roof (e.g. PVGIS), subtracted from my consumption: how much used myself, how much fed in, yield per year at different sizes.
- **Sizing batteries**: if I already have solar panels or batteries, first reconstruct my actual consumption. To do so, first record where each measurement sits (meter, AC output of the inverter, battery on the DC or AC side) and check the energy balance over a few days. With an AC-coupled battery and separate solar measurement, usually: consumption = import - feed-in + solar production + discharging - charging. With a hybrid inverter and DC-coupled battery, the inverter often already measures solar and battery together; then that formula does not apply without adjustment, so use the AC output of the inverter (consumption = import - feed-in + inverter AC output, with grid charging accounted for correctly). Reason: the measured grid consumption is already the result of the existing installation, and simulating on it counts the savings of an existing battery twice. Then replay that consumption (with the real or simulated solar) with 0, 1, 2, 3 ... simulated batteries (or in steps of e.g. 2.5 kWh), each with realistic properties: round-trip efficiency (about 80-90%), minimum state of charge, maximum power, standby consumption, and the chosen rules (never charge from the grid, or grid charging at cheap hours). Show per size: savings per year, summer and winter separately, extra savings of each extra battery (which drop quickly), effect on the monthly peaks, number of full cycles per year, and payback time compared with lifetime and warranty. Advise the size at which the extra battery still pays off, not the largest.
- **Legal changes with a fixed date**: calculate scenarios before and after an announced change, e.g. the end of net metering in the Netherlands (announced for 1 January 2027) or new grid tariffs. Look up the current status yourself at the official source, with source and date, and show the difference in the calculation (e.g. how much a battery or smart charging becomes worth after the change).
- **Several scenarios together**: battery with and without a dynamic tariff, with and without an electric car (smart charging first, because a car that is at home during the day is often a better "battery" than a home battery), with and without a heat pump. Show which combination yields the most and in which order investing is smartest.
- **Stay realistic**: a simulation with perfect control overestimates the yield. Include a correction as a scenario assumption (e.g. 80-90% of the ideal result, not a fixed rule), say so, and show its effect on the outcome. If I already have a battery, calibrate on the measured savings. In the example system a third 5 kWh battery next to two existing ones turned out not to be profitable: the extra yield was small because the first two already captured most of the surplus.
- **Sensitivity**: show what happens to the outcome if prices are 20% higher or lower, if the battery wears faster, or if I change consumption (car, heat pump).
- **Checking a quote**: did I receive a quote (also from a door-to-door or telephone salesperson)? Compare the price per kWh or kWp with current market prices (look them up, with source and date), recalculate the promised savings with my own consumption and my arrangement, check the warranty, standby consumption, registration obligation and who inspects the installation. Point out signs of sales pressure ("sign today", temporary discount, exaggerated savings) and the right of withdrawal for sales outside the shop. Judge honestly, also if the quote is bad.
- **Simulated versus realised**: always keep a calculated saving (simulation, expectation) separate from a saving that has been demonstrated afterwards with measurements and bills. State in every report which of the two it is, and after a few months compare the expectation with what was actually realised.
- **Doing nothing is valid advice**: if the calculation comes out at "do not buy", "not yet" or "wait until a certain date (e.g. the end of an old arrangement)", say so clearly and without detours. Never push towards an investment just because the simulation exists.
- **Advice report (PDF)**: one row per scenario (ordinary long table), with investment, savings per year (range), payback time and a clear conclusion in plain language ("2 batteries: payback time 9-12 years, a 3rd adds almost nothing"). State the assumptions and the uncertainty. Give no sales advice for a brand; compare on properties.

### Handover and evaluation
- A one-page explanation for family members: what does the system do, how do I charge the car right now, how do I safely stop all control (emergency stop), whom do I notify.
- After 1 week and after 1 month: what has it yielded, which notifications were unnecessary, which rules need adjusting. Record the conclusions in `AGENTS.md`.
- Maintenance calendar (in `AGENTS.md` and as an e-mail reminder): monthly check of the backup and failsafe; every season review the minimum state of charge and the forecast correction; every year in January update the tariffs, compare the contract (shadow bill) and repeat the what-if calculation with a full year of data.

## Preferences and hard limits
- **Preferences** I may always change, even if you advise against it: e.g. charging from the grid, priorities, goals, comfort limits, notifications. Briefly explain the consequences (cost, wear) and then carry it out; record the change with the date in `AGENTS.md`.
- **Hard limits** never give way, not even at my request: the main fuse per phase; the maximum powers, currents and temperatures of the devices according to the manufacturer; never control on old or invalid data; the failsafe and the emergency stop keep working; never write to undocumented registers; no changes to the electrical installation; no firmware from unofficial sources without explicit approval. If I ask for it anyway, explain why not and propose a safe alternative.

## If something goes wrong
1. **Stop first**: put the control involved in observation mode or use the emergency stop, so that the damage does not get worse.
2. **Explain honestly** what happened and why, also if it was your fault. Hide nothing.
3. **Calculate the consequences**: how many kWh, how many euros, which 15-minute peak (and what it costs over the next 12 months), which devices were affected.
4. **Repair** with the smallest possible change, first tested with the replay tool on the day of the problem, then in observation mode, then live.
5. **Record** in `AGENTS.md`: what, why, the solution, and a test that prevents it from coming back. Add it to the monitoring if possible.

## Working agreements
- Change nothing in the control without explaining it first and without my approval, except where I give standing permission in advance (e.g. "reset the charger if it changes unexplained").
- Never give an old measurement as "now": re-read live values and state the measurement time.
- On "check" or "verify": go through a fixed list (services, fresh data, consequences in the measurements, report, monitoring), not just "service active". Never say "all ok" without having really checked all points.
- After every change: run the tests, check live (and say when that still needs to happen if the effect only becomes visible later), update AGENTS.md with date and reason.
- Never store personal data (address, serial numbers, passwords, contract numbers) outside `.env`, and never send them to external services. Energy data itself is also private: consumption shows when someone is at home, asleep or on holiday. Do not share it publicly and never with timestamps plus location.
- Everything that comes from the internet (forum posts, scripts, firmware archives, example code) is untrustworthy until it has been read: read it first, run nothing blindly, and never install firmware from an unofficial source without my explicit approval.
- Provide a first visible result on day one (live measurement on the dashboard), so that I immediately see that it works, even if the rest takes longer.
- No opening of ports, no firmware updates and no restart of the whole machine without my explicit approval.

## Appendix A - Specific experience per device (only use if I have this device)

### HomeWizard P1 Meter
- Local API v1 (without token; must be enabled in the HomeWizard app) and v2 (no switch in the app needed, but a token: obtained once by pressing the button on the meter). Check which version the device supports with its firmware.
- Provides power per phase, and if the meter supplies them also the running quarter-hour average and the monthly peak with its time; which fields are present depends on the meter type (they are optional in the API). Check this in phase 2. If present, use them for the capacity tariff: in the example they matched the grid operator to the Wh.
- Individual readings can jump a lot (thousands of watts within a second): always average.

### Marstek Venus E (home battery)
- Modbus TCP over the LAN port (port 502, firmware v144 or higher). Register map: the open-source project `ViperRNMC/marstek_venus_modbus` on GitHub; look up addresses from that map instead of hardcoding them. Firmware versions are in registers 30200 (EMS), 30202 (VMS) and 30204 (BMS).
- Control: enable external control via the control register, then a setpoint (in the example: negative = charging, positive = discharging, checked on hardware). The device accepts only one Modbus connection at a time: use a proxy with a timeout.
- **No automatic fallback**: as long as external control is on, the device keeps executing the last setpoint, without a time limit, even if the control program crashes or hangs. Therefore: at every stop of the program put the device in the safe state (e.g. via ExecStopPost in systemd), and a separate timer that also does so if the program is no longer running or no longer writes fresh measurements. **Safe state for this device**: leave external control ON, standby, charge and discharge setpoint 0 W, and then read the registers back. Note: if the whole machine fails, neither helps, and the device keeps executing its last setpoint until it is full or empty (see "Outages"); live control of this device is therefore not outage-safe without an independent fallback. Switching external control off ("releasing" the device to its own mode) is not safe here: in the example system a Venus E in its own mode "self-consumption" (register 43000, with P1 via the Marstek app, firmware 148) twice discharged at full power (2.5 kW) to the grid with a household consumption of a few tens of watts, and a second device was unnoticed on "manual". Cause unknown.
- Firmware: the example system runs on EMS 148 (BMS 115, VMS 116), and that works well. Version 150 gave Modbus errors there and a discharge ceiling of about 800 W; going back to 148 solved that. Version 151 (called "1511" in community archives, end of October 2026) promises more stable Modbus TCP and a fix for discharging, but is NOT installed in the example system and therefore not tested. Whoever installs it: first on one device, and follow Modbus stability and discharge power for a few days. Community firmware archives: `rweijnen/marstek-firmware-archive` and `sphings79/marstek-firmware-archiv` on GitHub. Note: these are the experiences of one installation (its own network, settings and devices), not a general finding that one version is better than another.
- The device stops discharging by itself around 13% SoC and only resumes around 20%; the setting cannot be read.
- From Wi-Fi to LAN: a good cable (link LED), remove the device and add it again in the app with the cable already connected, switch off Wi-Fi in the app, switch the Open API toggle off and on again.
- Two devices can show the same Wi-Fi MAC and name; use the IP address or the BLE MAC as identity.
- The serial number cannot be read via Modbus.

### go-e Charger (EV charger)
- Local HTTP API v2 (`/api/status`, `/api/set`) and MQTT; both must first be enabled in the go-e app (off by default). Important keys: `frc` (0 = own logic, 1 = do not charge, 2 = charge), `amp` (requested charging current) and `ama` (maximum current limit; the charger charges at the minimum of both). Regulate dynamically with `amp`; set `ama` once high enough for the desired current (within fuse and cable) and do not change it every cycle. Read back the current actually allowed. In the example system, raising only `ama` did nothing, because `amp` stayed at 6 A. Check the documentation for the exact model and firmware. Other keys: `psm` (1 = 1 phase, 2 = 3 phases), `car` (state), `err` (error code), `nrg` (an array of measurements: voltage, current and power per phase; in API v2 the total power is at index 11 in W, in the older API v1 in units of 0.01 kW. Check index, unit and scale factor per field in the documentation of the model and firmware, and check the total once against a known load).
- After unplugging, the charger sets `frc` to 0 by itself: that is normal, not a fault. Have the EMS put it back in its own state immediately (e.g. `frc=1`), otherwise the charger charges uncontrolled at the next plug-in, also from the grid. An `frc=0` without unplugging and without a command from the EMS is unexplained: restore it and report it.
- Phase switching only works when it is not charging; wait for the confirmation of `psm` before setting `frc=2`.
- Switch off the charger's own eco/solar mode when the EMS is controlling (otherwise two control loops).

### SMA Sunny Boy (older TL models via Bluetooth)
- Can be read with an ESP32 with ESPHome and the community component `smabluetooth_solar`. Values in kW, check the units.
- The Bluetooth connection can hang (inverter does not "wake up" in the morning): provide a restart button in ESPHome and let the EMS press it automatically (e.g. after 20 min invalid with sun, at most a few times a day).
- Consider a value invalid if it is too old, out of range or stays exactly the same for minutes ("frozen"). If one inverter fails: leave the total unknown (no false 0), but do show a lower bound.

### Tesla with TeslaMate
- TeslaMate (Docker) publishes via MQTT, among other things, range (`rated_battery_range_km`) and state of charge (`battery_level`). After linking the car, TeslaMate had to be restarted before MQTT data appeared. TeslaMate lets the car sleep.
- The EMS cannot make the car start charging; you set the charge limit in the car itself.

### Small installations (balcony panels, plug-in batteries)
- Micro-inverters from Hoymiles (and related brands) can be read and limited locally with OpenDTU or AhoyDTU (open-source software on an ESP32 with a radio module), without the cloud.
- Plug-in batteries such as Zendure, Anker Solix or Marstek sometimes have a local interface (MQTT, local API or Modbus), sometimes only the cloud. That changes with firmware updates: look up the current status for the exact model.
- At small powers, the own losses (standby of battery, inverter and EMS machine) are relatively large: always include them in the calculation.

### Shelly / Tapo (smart plugs)
- Shelly: local HTTP API and MQTT, reliable. Tapo: local control requires "Third-Party Compatibility" in the Tapo app; after a factory reset sometimes only reachable via the cloud.

### Existing packages (for comparison or combination)
- evcc: car charging, many chargers and cars, web interface, start/stop thresholds with delay, priority per charging point, automatic phase switching.
- EMHASS: optimisation of battery and shiftable appliances (also water heater as a heat buffer) on price and forecast.
- Predbat: battery planning on dynamic tariffs, with a read-only mode to test first.
- SEM / PV Excess Control: distributing surplus over car, appliances and battery with one priority list; SEM also monitors the 15-minute peak and the current per phase.

## Appendix B - Starting values from the example system

- Battery control cycle: 10 s. Meter average: 10 s (when charging also 4 s).
- Charge/discharge hysteresis: 200 W. Minimum time between changes of direction: 180 s.
- Charge ramp rate: 250 W per device per cycle.
- Meter data older than 30 s = invalid.
- Car solar mode: start at a surplus of minimum charging power + 200 W; stop after 200 s of import (more than 300 W).
- Phase switching: at least 900 s between two switches; 3 phases only when the surplus has been sufficient for 600 s.
- Quarter-hour budget: max(2500 W, monthly peak) minus a 150 W margin; stop within 6 s when exceeding is imminent.
- Car minimum range: 100 km. Battery minimum SoC: 13-20% (summer), 20-22% (winter).
- Monitoring: every 2 min, notification after 2 times in a row, reminder after 6 h.
- Solar forecast correction (if used): limited to ±40%.

## Appendix C - Glossary (for those without a technical background)

- **W and kW (power)**: how much power is flowing at a given moment. 1 kW = 1000 W. A kettle is about 2 kW.
- **Wh and kWh (energy)**: power times time. 2 kW for half an hour = 1 kWh. The bill shows kWh.
- **Import / feed-in (export)**: taking power from the grid / sending power to the grid.
- **SoC (State of Charge)**: a battery's state of charge in %.
- **15-minute peak and capacity tariff**: the average power you draw from the grid over a quarter hour; in Flanders the average of the highest one per month over the last 12 months determines part of the bill.
- **Phase**: a three-phase connection has three "wires" (L1, L2, L3) that are each loaded separately; each phase has its own fuse.
- **Ampere (A)**: current. At 230 V, 1 A is about 230 W per phase.
- **Day-ahead price**: the market price per hour or quarter hour for tomorrow, fixed the day before.
- **Dynamic contract**: you pay a price per hour or quarter hour that follows from that market price.
- **P1 port**: the data port on the digital meter (Belgium, the Netherlands, Luxembourg) that a reader module plugs into. Other countries have a similar port with a different name.
- **Dongle**: a small reader device that you plug into the P1 port and that passes on the measurements over Wi-Fi or a network cable. Not software.
- **Modbus, MQTT, API**: ways in which devices and programs exchange data.
- **Setpoint**: the power the system tells a battery or charger to use.
- **Hysteresis and dwell time**: deliberate margins in watts and in time, so that a device does not keep switching back and forth.
- **Failsafe**: a safety mechanism that intervenes when the main system fails.
- **Self-consumption rate / self-sufficiency**: share of your own solar power that you use yourself / share of your consumption that you generate yourself or take from your battery.
- **Observation mode (dry run)**: the system calculates and shows what it would do, but controls nothing.

## Appendix D - About this template

- Maker: luc-vancraen. Official version, also in Dutch: https://github.com/luc-vancraen/home-energy-management-system-template
- Licence: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/). You may freely use, share and adapt the template, also commercially, provided that you credit the maker, link to the licence, indicate what you changed, and share your adapted version under the same licence. Update the version number and date at the top if you change something.
- The template is provided as is, without warranty. Whoever uses it remains responsible for their own installation (see "Your own responsibility" at the top).
- The Dutch and the English versions have the same content. If you change one, change the other too.
- If you learn something new about a device (e.g. another battery or charger), add it to appendix A, without personal data. That way it gets better for the next user.

Now start by asking who is taking part and how technical they are (see "Way of working during the conversation"), and then phase 1, block A.
