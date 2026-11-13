# Prompt: een thuis-energiebeheersysteem (EMS) bouwen op je eigen Linux-machine

Template v19 - november 2026

## Voor de gebruiker (lees dit eerst)

- **Wat is dit?** Een opdracht voor een AI-assistent. De assistent bouwt daarmee op jouw Linux-machine een systeem dat je energiemeter uitleest, alles bijhoudt, thuisbatterijen, een laadpaal en andere toestellen kan sturen, en je via een dashboard, rapporten en meldingen op de hoogte houdt. Het is gebaseerd op een bestaand systeem dat al maanden stabiel draait, aangevuld met ideeën uit bekende open-sourceprojecten (evcc, EMHASS, Predbat, SEM, PV Excess Control).
- **Welke AI?** Het template is niet gebonden aan één AI of één bedrijf. Het best werkt een **AI-agent**: een AI die op je computer zelf commando's kan uitvoeren en bestanden kan schrijven, zoals Claude Code, OpenAI Codex CLI, Gemini CLI of Kimi Code CLI. Een **gewone chat** in de browser of app (ChatGPT, Claude, Gemini, Kimi, ...) kan ook: de assistent voert dan zelf niets uit, maar geeft je telkens een commando of bestand; jij voert het uit in een terminal op de Linux-machine en plakt het resultaat terug. Dat werkt, maar is trager en vraagt meer opletten. Voor enkel advies (profiel 1) volstaat een chat waarin je je verbruiksdata kan opladen. Kies een sterk model: lange instructies zoals deze worden door kleinere modellen minder goed gevolgd; laat het dan fase per fase werken.
- **Hoe gebruik je het?** Met een agent: zet dit bestand (`hems-template-nl.md`) in een lege map op de Linux-machine, start daar de agent en typ: "Lees hems-template-nl.md en volg het." Zo kan de assistent er later zelf naar terugkijken. In een chat: laad het bestand op of plak de inhoud als eerste bericht, met de vraag "Volg dit".
- **Eigen verantwoordelijkheid.** Het systeem stuurt toestellen die veel vermogen schakelen. Jij blijft verantwoordelijk voor je installatie. De assistent wijzigt niets aan de elektrische installatie zelf (bekabeling, zekeringen, omvormerinstellingen die de netbeheerder vastlegt). Lees de garantievoorwaarden van je batterijen en laadpaal: sommige fabrikanten zien sturing door derden niet graag. Bij twijfel: eerst enkel uitlezen (dat is altijd veilig).
- **Toestemmingen.** De meeste agents vragen toestemming voor elk commando. Keur tijdens het bouwen niet alles automatisch goed: je wil elke systeemwijziging zien. Commando's met `sudo` (wachtwoord nodig) voer je zelf uit in een aparte terminal (sommige agents laten dat ook toe in de sessie, bv. door `! sudo ...` te typen in Claude Code). Geef de assistent nooit je sudo-wachtwoord in de chat.
- **Getallen in deze tekst** (zoals 180 s of 250 W) zijn startwaarden die in het voorbeeldsysteem werkten, geen wetten. De assistent past ze aan jouw toestellen aan.
- **Ook als je nog (bijna) niets hebt.** Het template werkt ook zonder batterijen, zonnepanelen of auto. Kies vooraan een startprofiel:
  1. **Advies vóór aankoop**: je hebt nog niets of twijfelt. De assistent rekent met je eigen verbruik uit wat zonnepanelen, batterijen (en hoeveel), slim laden, een warmtepomp of een ander contract zouden opbrengen. Er wordt niets gestuurd.
  2. **Inzicht**: enkel meten, dashboard en rapporten.
  3. **Tarief uittesten**: meten plus een doorlopende "schaduwfactuur" die je huidige contract vergelijkt met dynamische en andere contracten.
  4. **Verbruik verschuiven zonder batterij**: dynamisch tarief, auto, boiler, warmtepomp of pompen op goedkope of zonnige uren.
  5. **Volledig systeem**: batterijen, zon, auto, toestellen.
  Je kan later altijd naar een volgend profiel overstappen; wat al gebouwd is blijft.
- **Het gesprek duurt even.** Fase 1 stelt veel vragen; dat is bewust. Alles wat je niet weet of niet belangrijk vindt, mag je overslaan: de assistent kiest dan een veilige standaard en zegt welke.
- **Over meerdere sessies.** Het bouwen loopt over meerdere dagen. De assistent houdt alles bij in `AGENTS.md` en `installatie.md` in de projectmap. Start een volgende keer de agent in dezelfde map (veel agents kunnen ook het vorige gesprek hervatten) en zeg waar je gebleven was. Let op: veel agents lezen bij elke sessie automatisch een vast notitiebestand, maar dit promptbestand niet. `AGENTS.md` is de gangbare naam (o.a. OpenAI Codex CLI en Kimi Code CLI); Claude Code leest `CLAUDE.md` en Gemini CLI `GEMINI.md`. Daarom zet de assistent de belangrijkste regels en jouw keuzes in `AGENTS.md`, en maakt hij voor een agent met een andere bestandsnaam een kort bestand met die naam dat naar `AGENTS.md` verwijst. Werk je in een gewone chat: bewaar `AGENTS.md` en `installatie.md` en laad ze op (of plak ze) bij het begin van elk nieuw gesprek, samen met dit template.
- **Het systeem draait zonder AI.** Wat gebouwd wordt, zijn gewone programma's op je eigen machine. Ze blijven werken als je de AI niet meer gebruikt of je abonnement stopt; de AI heb je enkel nodig om te bouwen, aan te passen of problemen te onderzoeken. Je kan ook later van AI wisselen: alles staat in `AGENTS.md`, `installatie.md` en de code.
- **Kosten van het draaien.** Reken op het stroomverbruik van de machine zelf (een zuinige mini-pc van 10 W is ca. 90 kWh per jaar) en eventueel het abonnement of de API-kosten van de AI tijdens het bouwen. De rest kan gratis.

## Wat heb je nodig?

### Altijd
- **Enkel advies nodig (profiel 1)?** Dan volstaat een gewone laptop of pc, ook als die niet altijd aanstaat: Windows (met WSL, Linux onder Windows), een Mac, of de computer van iemand die helpt. Een machine die dag en nacht aanstaat is pas nodig om te meten of te sturen.
- **Om te meten of te sturen: een Linux-machine die dag en nacht aanstaat.** Een zuinige mini-pc (bv. Intel N100, 5-15 W) of een Raspberry Pi 4/5 met een SSD (geen SD-kaart: die slijt door de vele schrijfacties). Minimaal 4 GB werkgeheugen (8 GB als Home Assistant mee draait), 64 GB opslag of meer. Liefst met een netwerkkabel, niet via wifi. Draait je Home Assistant op Home Assistant OS (een apart besturingssysteem), dan kan het systeem daar niet zomaar naast: zie blok H ("Waar draait het?").
- **Alleen een Windows-pc?** Linux onder Windows (WSL 2) kan ook om te meten en, met voorwaarden, om te sturen: de pc moet dag en nacht aanstaan (slaapstand uit), WSL moet vanzelf starten met Windows en mag niet automatisch afsluiten, en Windows Update kan de pc herstarten. Een aparte, zuinige machine blijft de aanbeveling om te sturen. Zie blok H en "Beveiliging" in fase 4.
- **Besturingssysteem**: een gangbare Linux-distributie zoals Debian of Ubuntu (server of desktop). Je hebt een gebruiker met `sudo`-rechten nodig.
- **Een AI-assistent**: bij voorkeur een AI-agent op die machine (zie "Welke AI?"), met het abonnement of API-account dat die vraagt, geïnstalleerd volgens de officiële handleiding van de maker. Werk je liever vanaf je gewone computer: verbind met de Linux-machine via SSH en start de agent daar. Met een gewone chat heb je daarnaast een terminal op de Linux-machine nodig (rechtstreeks of via SSH) om de commando's uit te voeren.
- **Toegang tot je router**, om de toestellen een vast IP-adres te geven (DHCP-reservatie).
- **Internet** tijdens het bouwen (pakketten downloaden). Daarna werkt het systeem ook zonder, behalve prijzen, voorspellingen en meldingen.
- **Tijd**: reken op een paar avonden voor de basis, en daarna enkele weken opvolgen en bijstellen. Programmeerkennis is niet nodig; je moet wel vragen kunnen beantwoorden, af en toe een instelling in een app wijzigen en een commando laten uitvoeren.

### Afhankelijk van je profiel
- **Advies vóór aankoop**: je verbruiksdata. In Vlaanderen: kwartierdata uit "Mijn Fluvius" (aanmelden met itsme of eID, export als CSV). Anders je jaarafrekening en, als je die hebt, een paar recente facturen. Eventueel offertes voor zonnepanelen of batterijen.
- **Meten (alle andere profielen)**: een digitale meter met een uitleesmodule (dongle), bv. een HomeWizard P1 Meter of een andere dongle die lokaal uit te lezen is. Zo'n dongle is een klein toestel, geen software: de app van de fabrikant dient enkel om hem in te stellen, en op de machine hoeft niets van de fabrikant geïnstalleerd te worden. De gegevenspoort moet geactiveerd zijn (in Vlaanderen via "Mijn Fluvius"). Zie "Meter klaarmaken" hieronder. Nog een analoge meter (met draaischijf of telwerk)? Dan: een digitale meter aanvragen bij de netbeheerder, een stroomtang-meter laten plaatsen door een elektricien, of voorlopig enkel advies op basis van jaarstanden.
- **Eén dongle volstaat**, als hij zijn metingen lokaal via het netwerk deelt: dan lezen batterij, dit systeem en eventueel Home Assistant allemaal dezelfde bron. In het voorbeeldsysteem zit er één HomeWizard op de meter; de batterijen krijgen de metingen via de Marstek-app van die HomeWizard, en het systeem leest dezelfde HomeWizard via de lokale API. Home Assistant is daarvoor niet nodig. Een P1-kabel rechtstreeks naar de machine of een merkgebonden dongle die enkel zijn eigen batterij of de cloud bedient, bezet de poort wel: dan is voor een tweede lezer een splitter of een andere dongle nodig.
- **Buiten België, Nederland en Luxemburg** heet de poort anders en werkt hij anders (bv. de HAN-poort in Scandinavië, een optische poort of Smart Meter Gateway in Duitsland, Linky TIC in Frankrijk, een in-home display of CAD in het Verenigd Koninkrijk). De assistent zoekt de juiste uitleesmogelijkheid voor je land op.
- **Dynamisch tarief of tariefvergelijking**: een gratis ENTSO-E-token voor de marktprijzen (aanvragen via de transparantiewebsite van ENTSO-E) en de prijsformules van de contracten die je wil vergelijken.
- **Zonnepanelen meten**: een omvormer die lokaal uit te lezen is (Modbus, lokale API), of eventueel een ESP32-module (enkele euro's) voor omvormers met Bluetooth.
- **Batterijen sturen**: batterijen met lokale toegang (bij voorkeur Modbus TCP via netwerkkabel), en toegang tot de app van de fabrikant (om lokale toegang aan te zetten en de firmwareversie te zien).
- **Auto sturen**: een laadpaal die lokaal stuurbaar is (MQTT, HTTP-API, Modbus of OCPP) en de app ervan. Voor de laadtoestand van de auto: een koppeling zoals TeslaMate (Tesla) of een Home Assistant-integratie; zonder koppeling gaat het ook, met een schatting.
- **Andere toestellen**: slimme stekkers of relais (bv. Shelly) of een SG-ready-ingang op de warmtepomp.
- **Meldingen per mail**: een mailaccount met SMTP-toegang, bij voorkeur met een apart app-wachtwoord.
- **Back-up** (aanbevolen): een NAS, externe schijf of cloudopslag.
- **Toegang van buitenaf** (optioneel): een gratis VPN zoals Tailscale.

### Meter klaarmaken (doe je zelf, ca. 15 minuten plus de wachttijd van de netbeheerder)
Geen elektricien nodig, en de assistent kan dit niet voor je doen: het zijn handelingen aan de meter en in apps.
1. Gegevenspoort activeren bij de netbeheerder (in Vlaanderen: "Mijn Fluvius", aanmelden met itsme of eID; dat kan enkele dagen duren).
2. De dongle in de poort steken (bij P1: het kleine RJ12-stekkertje onder het klepje van de digitale meter; je breekt geen verzegeling). Bij sommige meters levert de poort te weinig stroom en is een USB-voeding nodig.
3. De dongle met wifi (of netwerkkabel) koppelen via de app van de fabrikant.
4. Nagaan welke lokale API de dongle heeft en wat daarvoor nodig is, volgens de officiële documentatie voor dat toestel en die firmware. Bij HomeWizard: API v1 moet je in de app aanzetten; API v2 heeft die schakelaar niet nodig, maar vraagt een token (eenmalig ophalen door op de knop van de meter te drukken). Zonder lokale toegang kan geen systeem de meter lokaal lezen.
5. De dongle een vast IP-adres geven in de router (DHCP-reservatie).
6. Optioneel: in de app van je batterij of omvormer dezelfde dongle als meter kiezen, als die dat ondersteunt.

Daarna zoekt de assistent de dongle op het netwerk, leest één meting en controleert wat er binnenkomt (zie fase 2), voor het begint te loggen.

### Wat je niet nodig hebt
- Geen programmeerkennis, geen cloudabonnementen van fabrikanten, geen poorten open in je router, geen aanpassingen aan de elektrische installatie.
- Geen software van de fabrikanten op de machine: de apps (meter, batterij, laadpaal) gebruik je op je smartphone om de toestellen in te stellen; het systeem spreekt de toestellen zelf aan via het netwerk.
- Geen Home Assistant: dat is optioneel (zie blok H).

## Opdracht aan de AI-assistent

Je bent een AI-assistent die me helpt op mijn Linux-machine een thuis-energiebeheersysteem (EMS) op maat van mijn installatie te bouwen. Hieronder staat wat het voorbeeldsysteem doet, welke opties er zijn en welke lessen er geleerd zijn. Mijn installatie is anders: bouw daarom niets voordat fase 1 (vragen), fase 2 (machine nakijken) en fase 3 (plan) afgerond zijn en ik het plan heb goedgekeurd.

Hoe je werkt hangt af van wat je kan:
- **Als agent** (je kan zelf commando's uitvoeren en bestanden schrijven op mijn machine): werk rechtstreeks, maar vraag toestemming voor elke wijziging aan het systeem.
- **In een gewone chat** (geen toegang tot mijn machine): geef me telkens één commando of één volledig bestand tegelijk, met de map waar het moet komen, en zeg wat ik zou moeten zien. Vraag me de uitvoer terug te plakken en ga pas verder als die klopt. Raad nooit wat een commando teruggeeft en doe nooit alsof je iets uitgevoerd of nagekeken hebt. Hou bestanden kort genoeg om in één keer te kopiëren.
- **Zonder internettoegang**: zeg het als je iets niet zelf kan opzoeken (tariefkaarten, regels, handleidingen), vraag me de bron te bezorgen, en gebruik je voorkennis nooit als vaststaand feit.
- Gebruikt je agent een ander vast notitiebestand dan `AGENTS.md` (bv. `CLAUDE.md` of `GEMINI.md`), maak dat dan aan met één regel die naar `AGENTS.md` verwijst, zodat elke sessie de regels inleest.

Werkwijze tijdens het gesprek:
- Vraag eerst wie er meedoet: de **bewoner** (voor wie het systeem is) en eventueel een **helper** (familie, buur, installateur; soms op afstand). Vraag voor elk van hen hoe technisch die is (geen ervaring / wat Linux-ervaring / programmeur) en welke taal die spreekt. Technische vragen gaan naar de helper, wensen en keuzes naar de bewoner. Rapporten, dashboard en meldingen voor de bewoner zijn in de taal van de bewoner; `AGENTS.md` en technische notities in de taal van de helper. Is er geen helper, dan is de bewoner beide. Pas je uitleg aan; leg vaktermen kort uit voor wie geen programmeur is.
- Stel de vragen per blok. Gebruik meerkeuzevragen waar dat kan, met jouw aanbevolen keuze als eerste optie. Wacht telkens op mijn antwoord.
- Weet ik iets niet, help me het te vinden (app, typeplaatje, factuur, router, handleiding) of zoek het zelf op het netwerk, maar pas na mijn akkoord.
- Sla over wat niet van toepassing is (geen auto = geen EV-vragen en geen EV-onderdelen).
- **Snelle start**: stel in fase 1 eerst enkel de vragen die nodig zijn voor het startprofiel, de meter en het dashboard (meestal een tiental). De overige vragen van een blok stel je pas wanneer die module aan de beurt is. Vraag bij mensen zonder ervaring om de paar blokken of ze willen pauzeren; het gesprek mag over meerdere dagen lopen.
- **Express-modus**: wil ik alle vragen overslaan ("doe gewoon iets"), kies dan veilige standaarden: enkel meten, dashboard en observatiemodus, niets sturen. Vóór er ook maar iets gestuurd wordt, moeten deze kernpunten altijd bevestigd zijn, hoe kort ook: welke toestellen gestuurd worden, maximaal vermogen per toestel, hoofdzekering en aantal fasen, het teken (laden/ontladen) getest met een klein vermogen, dat niets anders het toestel stuurt, en dat de noodknop werkt.
- **Antwoorden nakijken**: vergelijk mijn antwoorden met wat de metingen tonen (aantal fasen, vermogens, verbruik, contract tegenover factuur). Klopt iets niet, zeg het vriendelijk en vraag wat juist is voor je erop verder bouwt.
- **Zelf opzoeken in plaats van mij te laten zoeken**: officiële tariefkaarten van leveranciers, nettarieven, regels van mijn regio (capaciteitstarief, terugdraaiende teller, aanmelding van batterijen, premies) en handleidingen van mijn toestellen zoek je zelf op het internet op, bij de officiële bron. Vermeld telkens de bron en de datum, en laat mij de belangrijkste waarden bevestigen. Regels en prijzen veranderen: gebruik nooit alleen je eigen voorkennis als feit.

## Fase 1 - Mijn installatie en wensen opvragen

### Blok A - Startprofiel, doelen en prioriteiten
- Eerst een korte voorcheck, vóór alle andere vragen: heb ik een digitale meter, is de gegevenspoort geactiveerd, en zit er al een dongle op die lokaal uit te lezen is (en zo ja, gebruikt mijn batterij of omvormer die al)? Zo niet: zeg meteen welke profielen nu al kunnen (advies vóór aankoop, op basis van kwartierdata of jaarafrekening) en wat ik eerst moet regelen (zie "Meter klaarmaken"), zodat ik niet eerst alle blokken invul voor iets wat nog niet kan.
- Welk startprofiel past (advies vóór aankoop / inzicht / tarief uittesten / verbruik verschuiven zonder batterij / volledig systeem)? Profielen mogen gecombineerd worden; een veel voorkomende combinatie is "tarief uittesten" + "verbruik verschuiven zonder batterij" (eerst kijken of een dynamisch contract loont, en intussen auto en warmtepomp slim laten werken). Stel daarna enkel de vragen die bij de gekozen profielen horen. Bij "advies vóór aankoop": begin met blok J en stel de andere blokken enkel voor zover nodig.
- Wat zijn mijn drie belangrijkste doelen? Laat me er drie kiezen (geen volledige rangschikking) uit: zo veel mogelijk eigen zonnestroom gebruiken; zo laag mogelijke energiefactuur; zo laag mogelijke kwartierpiek (capaciteitstarief); zo weinig mogelijk teruglevering; zo weinig mogelijk CO2 (stroom gebruiken wanneer het net het groenst is); batterijen sparen (minder cycli, niet altijd 100%); reserve houden voor stroomuitval; de auto altijd op tijd genoeg geladen; zo weinig mogelijk ingrijpen ("het moet gewoon werken").
- Wil ik dat het systeem meteen stuurt, of eerst een tijd enkel meet en toont wat het zou doen (observatiemodus)?
- Hoeveel meldingen wil ik: enkel bij problemen, een dagelijks rapport, of ook wekelijkse/maandelijkse overzichten?
- Budget: mag er iets kosten? Bv. een betaalde voorspellingsdienst, een ESP32-module of Modbus-adapter (enkele tientjes), een licentie voor een bestaand pakket. Standaard: enkel gratis diensten.
- Kleine installatie (bv. balkonpanelen of één stekkerbatterij)? Dan weegt het eigen verbruik van het systeem zwaar: een mini-pc van 10 W gebruikt ca. 90 kWh per jaar, wat een groot deel van de winst kan opslorpen. Reken de netto winst uit en stel lichtere opties voor: een toestel dat toch al dag en nacht aanstaat (NAS, router met Docker, bestaande Home Assistant), een ESP32-oplossing, of de eigen logica van het toestel gewoon laten werken met enkel inzicht erbij.
- Plannen voor de komende jaren: extra panelen, extra batterij, warmtepomp, tweede auto, nieuwe laadpaal? Dan houden we daar nu al rekening mee.

### Blok B - Land, aansluiting en contract
- Land en netbeheerder (weet ik die niet: leid ze af uit de gemeente). (Vlaanderen: capaciteitstarief op het gemiddelde van de maandpieken (hoogste kwartierpiek per maand) van de laatste 12 maanden, waarbij een maandpiek onder 2,5 kW als 2,5 kW telt; pieken onder 2,5 kW kosten dus niets extra. Wallonië, Brussel, Nederland en andere landen hebben andere regels: zoek de actuele regels zelf op bij de officiële bron, met bron en datum, en neem de Vlaamse regels niet zomaar over.)
- Eenfasig of driefasig, 230 V of 400 V, hoeveel ampère hoofdzekering (per fase)?
- Welk contracttype? Opties: vast; variabel (maandindex); dynamisch (prijs per uur of kwartier, bv. op basis van de day-ahead-markt); dag/nacht; exclusief nacht. Heb ik de prijsformule of een recente factuur (mag een foto zijn; persoonlijke gegevens niet overnemen)? Ken ik enkel de naam van leverancier en contract: zoek dan zelf de officiële tariefkaart op (let op de juiste maand, regio en contractversie) en laat me die bevestigen tegen een factuur.
- Vaste kosten (abonnement, databeheer, meterhuur) per jaar, zodat de besparingen eerlijk gerekend worden.
- Injectie: is er een vergoeding, vast of variabel? Betaal ik bij negatieve prijzen voor injectie? Is er een injectietarief of een maximum injectievermogen van de netbeheerder?
- Overweeg ik een dynamisch tarief? Eerlijke waarschuwing vooraf: zonder batterij of verschuifbaar verbruik (auto, warmtepomp, boiler) levert een dynamisch tarief vaak weinig op of kost het meer, en er zijn uitschieters (dure winteravonden, crisisjaren). Hoeveel risico wil ik nemen? Ben ik bereid zelf verbruik te verschuiven (wasmachine, vaatwas)?
- Heb ik nog een oude regeling (bv. terugdraaiende teller, prosumententarief, groenestroomcertificaten)? Die verandert de rekensom volledig.
- Doet mijn leverancier aan flexibiliteitsprogramma's (bv. vergoeding om op bepaalde momenten minder te verbruiken)?
- Doe ik mee aan energiedelen of een energiegemeenschap (stroom delen met buren of familie), of overweeg ik dat? Dan telt gedeelde stroom anders in de rekensom.
- Woon ik in een appartement of gebouw met gedeelde installaties (gedeelde laadpalen, gemeenschappelijke meter)? Dan kan ik vaak enkel mijn eigen deel meten en sturen.
- Ben ik huurder of mede-eigenaar? Dan is voor panelen (ook balkonpanelen), batterijen, een laadpaal of bedrading vaak toestemming nodig van de verhuurder of de vereniging van mede-eigenaars. Vraag ernaar voor elk profiel waar iets geplaatst wordt, en zoek de regels voor mijn regio op (bv. aanmelding van balkonpanelen bij de netbeheerder).
- Dag/nacht-uren: welke uren gelden echt? (In het voorbeeld bleken de uren van de netbeheerder anders dan verwacht; controleer met meterdata tegenover de factuur of het portaal van de netbeheerder.)
- Gemeente of streek (voor de zonvoorspelling en het weer). Sla nooit een exact adres op.

### Blok C - Meter en metingen
- Heb ik al een digitale meter? Zo niet (analoge meter): opties zijn een digitale meter aanvragen bij de netbeheerder (zoek de voorwaarden, kosten en wachttijd op voor mijn regio), een stroomtang-meter laten plaatsen door een erkende elektricien, of voorlopig enkel rekenen met jaarstanden en een standaard verbruiksprofiel. Zeg wat elke optie mogelijk maakt.
- Welke digitale meter en welke uitlezing? Opties: HomeWizard P1 Meter; een andere P1-dongle (bv. via ESPHome, DSMR-reader, Slimmelezer); rechtstreekse P1-kabel op de machine; enkel de meter van de omvormer/batterij; een stroomtang-meter (Shelly EM, ...). Lokaal bereikbaar (IP-adres, lokale API beschikbaar en eventueel aangezet of een token opgehaald)? Gebruikt een batterij of omvormer dezelfde meter al, en via welke weg (via het netwerk van dezelfde dongle, een eigen dongle op de poort, een eigen stroomtang)? Buiten België, Nederland en Luxemburg: zoek op welke poort of uitlezing de meters in mijn land hebben.
- Geeft de meter per fase vermogen en stroom? Het lopende kwartiergemiddelde en de maandpiek?
- Gas en water ook meten? Andere tussenmeters (bv. een aparte meter voor de warmtepomp)?
- Hoe vaak wil ik meten (elke 1-10 s is gebruikelijk) en hoe lang bewaren (ruwe data bv. 1-2 jaar, daarna samengevat)?
- Heb ik nog geen uitlezing: geef koopadvies op basis van criteria, niet op merk. Belangrijk: een lokale API (werkt zonder cloud), meetwaarden elke paar seconden, vermogen en stroom per fase, liefst ook het kwartiergemiddelde en de maandpiek, voeding via de P1-poort of een stekker, metingen lokaal via het netwerk delen met meerdere lezers (zodat één dongle volstaat voor batterij, systeem en Home Assistant), werkt zonder Home Assistant of cloud, en goede ondersteuning in open-sourcesoftware. Vergelijk een paar gangbare typen (kant-en-klare dongle, ESPHome-dongle, kabel rechtstreeks naar de machine). Zeg ook dat de P1-poort eerst geactiveerd moet worden (in Vlaanderen via "Mijn Fluvius"; dat kan enkele dagen duren), en start intussen al met de historische kwartierdata als CSV.

### Blok D - Zonnepanelen
- Zonnepanelen ja/nee? Totaal kWp, aantal vlakken met elk oriëntatie, helling en kWp. Schaduw op bepaalde uren?
- Merk en type van de omvormer(s). Hoe uitlezen? Opties: lokale Modbus TCP/SunSpec; lokale web-API; Bluetooth via een ESP32 met ESPHome; Home Assistant-integratie; enkel via de cloud; niet. Zonder zonmeting sturen we op de meter, dat werkt ook.
- Kan de omvormer begrensd of uitgezet worden (handig bij negatieve injectieprijs of een injectielimiet)? Mag dat van de netbeheerder en de installateur?
- Zonvoorspelling: gratis Forecast.Solar (geen account), Solcast (gratis account, nauwkeuriger), Open-Meteo (weer) of geen. Mag het systeem de voorspelling zelf bijsturen met de gemeten afwijking?

### Blok E - Thuisbatterijen
- Wat voor systeem? Opties: losse batterij(en) op het stopcontact of met eigen omvormer (AC-gekoppeld, bv. Marstek, Zendure); een hybride omvormer met batterij (DC-gekoppeld, bv. Sungrow, Huawei, SolarEdge, GoodWe, Victron); een combinatie. Bij een hybride systeem gelden de regels uit "Hybride omvormers" hieronder.
- Aantal batterijen, merk en type, capaciteit (kWh), maximaal laad- en ontlaadvermogen (W) per toestel, firmwareversie. Op welke fase hangt elk toestel (bij driefasig)?
- Waar staan ze? Binnen, of in een onverwarmde garage of berging? (Bij vorst laden veel batterijen niet of maar beperkt; dat moet het systeem weten om het in de winter niet als fout te zien.)
- Veiligheid en regels: staan ze niet in een vluchtweg, is er een rookmelder in de buurt, zijn ze aangemeld bij de netbeheerder (in Vlaanderen verplicht), en weet de brandverzekering ervan? De assistent controleert dat niet zelf, maar vraagt het en noteert het antwoord.
- Installeert het toestel zelf firmware-updates (automatisch via de app)? Kan dat uit? (Een automatische update veranderde in het voorbeeld het gedrag; het systeem moet een firmwarewijziging opmerken en melden.)
- Hoe lokaal sturen? Opties: Modbus TCP via LAN; Modbus RTU (RS485 met een adapter); lokale UDP/HTTP-API; via Home Assistant; enkel cloud-app (dan beperkt of niet stuurbaar). Kabel (LAN) of wifi? Vast IP-adres via DHCP-reservatie?
- Is er al iets dat de batterijen stuurt? Opties: eigen automatische modus van het toestel (bv. "zelfverbruik" met eigen meter); een app-schema; Home Assistant-automatiseringen; een dynamisch contract met eigen sturing; niets. Belangrijk: er mag maar één sturing tegelijk actief zijn. De andere zetten we uit, en ik noteer hoe ik ze terugzet.
- Hoe mogen ze laden? Opties: enkel uit zonne-overschot (nooit uit het net); ook uit het net op goedkope uren (dynamisch contract), maar enkel als de zon de batterij die dag niet vult; ook uit het net bij negatieve prijzen.
- Hoe mogen ze ontladen? Opties: enkel voor eigen verbruik, nooit naar het net; ook naar het net bij hoge prijzen (arbitrage); enkel om de kwartierpiek te drukken; niet ontladen terwijl een groot toestel (auto, warmtepomp) draait.
- Minimum laadtoestand (SoC): vast, of zomer/winter verschillend? Reserve voor stroomuitval (enkel als het toestel noodstroom kan leveren)? Maximum laadtoestand om te sparen (bv. 90%)?
- Mogen de batterijen de auto voeden? (In het voorbeeld: nee, de batterijen zijn voor het huis.)

### Blok F - Elektrische auto(s)
- Elektrische auto ja/nee? Hoeveel auto's en hoeveel laadpalen?
- Laadpaal: merk en type. Lokaal stuurbaar via MQTT, HTTP-API, Modbus of OCPP? Kan hij tussen 1 en 3 fasen schakelen? Minimum- en maximumstroom?
- Auto: merk en type, batterijcapaciteit, verbruik (kWh/100 km). Kan de laadtoestand/range lokaal gelezen worden? Opties: TeslaMate (Tesla); Home Assistant-integratie van het merk; via de laadpaal (meestal niet); niet (dan schatten we de laadtoestand uit de geladen kWh en het verbruik).
- Laadstrategie, kies er een of combineer: enkel op zonne-overschot; minimum + zon (altijd minstens het minimum, de rest op zon); minimum-range (onder X km altijd laden, ook uit het net); vertrektijd + doel (bv. 80% om 7:30, zo goedkoop mogelijk, 's nachts minder als morgen zonnig is); goedkoopste uren (dynamisch contract); reismodus (eenmalig tot 100%); altijd maximaal; handmatig (het EMS kijkt enkel toe).
- Bij meerdere auto's of laadpalen: welke krijgt voorrang?
- Is de laadpaal of de auto enkel via de cloud van de fabrikant bereikbaar? Dat kan, maar zie de regel over cloudtoestellen.
- Kan de auto en laadpaal stroom terugleveren aan het huis of het net (bidirectioneel laden, V2H/V2G)? Nu of in de toekomst? Dan is de auto ook een thuisbatterij en hoort hij in de batterijregels.
- Grenzen: maximaal netvermogen of -stroom voor de auto; binnen het kwartierbudget van het capaciteitstarief blijven; per fase onder de hoofdzekering.

### Blok G - Andere stuurbare toestellen (optioneel)
- Warmtepomp (SG-ready-ingang?), elektrische boiler (eventueel met regelbaar vermogen of als warmtebuffer), airco, zwembad- of vijverpomp, droogkast/wasmachine/vaatwas, slimme stekkers (Shelly, Tapo, ...), elektrische verwarming.
- Per toestel: vermogen, mag het verschoven worden, binnen welke uren, minimum looptijd per dag (bv. pomp 6 u, ook als er geen zon is), minimum aan- en uittijd.
- Warmtepomp: comfortgrenzen. Minimale en maximale binnentemperatuur (dag/nacht), warm water (minimale temperatuur, wanneer moet het klaar zijn), vloerverwarming of radiatoren, hoe goed het huis warmte vasthoudt (hoeveel graden zakt het per uur zonder verwarming?), en mag de weersvoorspelling gebruikt worden? Comfort gaat altijd voor besparing.
- Is er voor een toestel nog bedrading nodig (bv. een relais op de SG-ready-ingang, een tussenmeter, een stroomtang)? Dan zegt de assistent precies wat er nodig is, maar dat plaatst een erkende elektricien; het systeem stuurt het pas als het geplaatst is.
- Eén prioriteitenlijst voor alles (auto's, toestellen en batterij), in een volgorde die ik zelf kies en later kan wijzigen. Standaard: auto > boiler/warmtepomp > batterij > net.
- Toestellen die al door het tarief of een relais van de netbeheerder gestuurd worden (bv. nachtaccumulatoren of een boiler op exclusief nacht): herken ze, stuur ze niet dubbel, en reken hun verbruik op de juiste teller.
- Toestellen die ik NIET wil laten sturen, maar die het verbruik wel beïnvloeden (handig voor verklaringen in rapporten): bv. microgolfoven, elektrisch vuurtje, warmtewisselaar, inductiekookplaat.

### Blok H - Wat draait er al en wat wil ik zien
- Waar draait het? Opties: een gewone Linux-machine (Debian/Ubuntu; aanbevolen); dezelfde machine als Home Assistant OS (dan: (a) een aparte kleine machine ernaast, (b) alles als Home Assistant-add-on of in Home Assistant zelf met AppDaemon of pyscript, of (c) Home Assistant verhuizen naar Docker op een gewone Linux-machine); een NAS met Docker; een virtuele machine (Proxmox e.d.); een Windows-pc met WSL 2 (Linux onder Windows; geschikt om te meten, om te sturen enkel met de voorwaarden hieronder). Leg de voor- en nadelen uit en pas fase 2 en het plan aan die keuze aan.
- Linux-distributie, is de machine altijd aan, sudo-rechten, Docker aanwezig, vrije schijfruimte? Hangt ze aan een UPS? Start ze vanzelf opnieuw na een stroomonderbreking (BIOS-instelling)?
- Bij WSL 2: systemd aanzetten (`systemd=true` onder `[boot]` in `/etc/wsl.conf`); WSL laten starten bij het opstarten van Windows (bv. een taak in Taakplanner die bij het opstarten `wsl` start, ook zonder aanmelden); automatisch afsluiten van WSL bij inactiviteit uitzetten (in `%UserProfile%\.wslconfig`, de instelling hangt af van de WSL-versie: laat de assistent ze opzoeken); slaapstand en sluimerstand van Windows uit; een tijdstip voor Windows Update-herstarts kiezen. Netwerk: in de standaardmodus (NAT) is WSL niet bereikbaar vanaf het thuisnetwerk en werkt het automatisch zoeken van toestellen (mDNS, bv. door Home Assistant) niet; kies op Windows 11 `networkingMode=mirrored` in `.wslconfig`, of een poortdoorverwijzing in Windows. Uitgaande verbindingen naar de toestellen (P1-meter, batterij, laadpaal) werken in beide modi. Omdat Windows de pc onverwacht kan herstarten, is bij sturen een failsafe verplicht, en enkel toestellen met een eigen time-out of terugval in het toestel zelf blijven dan veilig (zie "Uitval" in fase 4).
- Home Assistant aanwezig of gewenst? MQTT-broker (Mosquitto)?
- Dashboard: eigen webpagina (Flask), Home Assistant-dashboard, Grafana, of een combinatie? Heb ik al dashboards of een database (Home Assistant-energiedashboard, Grafana, InfluxDB)? Dan worden die hergebruikt en aangevuld in plaats van ernaast iets nieuws te bouwen.
- Voor programmeurs: wil ik de code in mijn eigen Git-repository (bv. op GitHub of GitLab), met tests die automatisch draaien (CI)? Geheimen dan zeker niet in de repository.
- Meldingen via: mail (SMTP-server, best een app-wachtwoord), sms, WhatsApp of Signal (via een koppeling of dienst; zoek een betrouwbare, liefst gratis optie op), Home Assistant-app, Telegram, ntfy, of geen. Wachtwoorden en tokens geef ik pas als je ze nodig hebt; ze komen enkel in `.env`.
- Wie krijgt welke meldingen (bewoner, helper, meerdere gezinsleden)? Bv. technische alarmen enkel naar de helper, een eenvoudig overzicht in gewone taal naar de bewoner. Stille uren 's nachts, behalve bij echte alarmen?
- Rapporten: dagelijks PDF-rapport (tijdstip?), wekelijks/maandelijks, per mail of enkel als bestand?
- Back-up: naar een NAS, externe schijf of cloud (bv. met restic)? Hoe vaak?
- Toegang van buitenaf: niet, via een VPN (bv. Tailscale/WireGuard), of via Home Assistant Cloud? Nooit poorten openzetten in de router zonder uitdrukkelijk akkoord.
- Gebruikt een niet-technisch gezinslid het systeem ook? Dan komt er een eenvoudige uitleg op één pagina.
- Wie mag het dashboard zien en wie mag iets wijzigen? Iedereen op het thuisnetwerk (ook gasten op de wifi), of enkel met een wachtwoord? Zijn er een gastnetwerk of een apart netwerk voor slimme toestellen?
- Wil ik een externe "levensteken"-bewaking (bv. de gratis dienst healthchecks.io), die me verwittigt als de hele machine stilvalt? De eigen bewaking kan dat niet melden als ze zelf niet meer draait.
- Wil ik mijn data ook als CSV of Excel kunnen downloaden voor eigen berekeningen?

### Blok I - Weergave en leesbaarheid
- Ben ik (of iemand die de grafieken leest) kleurenblind? Opties: nee; rood-groen (meest voorkomend); blauw-geel; volledig kleurenblind; weet ik niet. Bij "weet ik niet" of twijfel: kies kleuren die voor iedereen werken (bv. blauw/oranje in plaats van rood/groen).
- Ongeacht het antwoord: in grafieken en dashboards nooit kleur als enige drager van informatie. Gebruik ook arcering, lijnstijl (vol/gestreept/gestippeld), symbolen en tekstlabels, en controleer elke grafiek ook in grijstinten.
- Lees ik het dashboard vooral op een gsm, tablet of computer? Grote letters nodig? Licht of donker thema?
- Lees ik rapporten liever op papier? Dan: A4, groot lettertype, hoog contrast, leesbaar als zwart-witafdruk (geen informatie enkel in kleur), en bovenaan de belangrijkste conclusie in één zin in gewone taal.
- Getallen en tijden: decimale komma of punt, 24-uursnotatie, kW of W, datum als dag/maand?

### Blok J - Advies vóór aankoop (als ik nog niets of weinig heb)
Data:
- Welke verbruiksdata zijn er? Opties, van best naar minst goed: kwartierdata van de digitale meter (in Vlaanderen te downloaden via "Mijn Fluvius" als CSV, liefst minstens een volledig jaar); een P1-uitlezing die we nu starten (dan eerst enkele weken of maanden meten); maandstanden of de jaarafrekening (dan rekenen we met een standaard verbruiksprofiel, minder nauwkeurig: zeg dat in elk resultaat). Heb ik al historiek in een ander systeem (statistieken van Home Assistant, InfluxDB, de export van een omvormer- of batterijportaal)? Dat is vaak de beste bron: importeer die, met controle op gaten, eenheden en tijdzone.
- Gasverbruik per jaar (voor een warmtepompberekening) en hoe het huis verwarmd wordt.

Mijn situatie:
- Hoeveel personen, wie is overdag thuis (thuiswerk), wanneer wordt er gekookt, gewassen, gedroogd?
- Eigenaar of huurder? Hoe lang blijf ik hier waarschijnlijk wonen? (Een investering die zich pas na 12 jaar terugbetaalt, is weinig waard als ik over 5 jaar verhuis.)
- Plannen: elektrische auto (wanneer, hoeveel km per jaar, wanneer staat hij thuis: overdag of enkel 's avonds en 's nachts?), warmtepomp, airco, thuiswerk, gezinsuitbreiding?
- Budget, en welke terugverdientijd vind ik aanvaardbaar? Lenen of eigen spaargeld (rente of gemiste rente telt mee)?

Zonnepanelen (als ik ze nog niet heb):
- Daksoort, oriëntatie, helling, bruikbare oppervlakte, schaduw (bomen, schouw, buren). Ligging (gemeente) voor de zonnesimulatie, bv. met PVGIS (gratis tool van de Europese Commissie, productie per uur voor een locatie en oriëntatie).
- Offerte(s) beschikbaar? Prijs per kWp, omvormertype.

Batterijen (als ik ze nog niet heb):
- Welke types overweeg ik? Opties: stekkerbatterij (bv. Marstek, Zendure, Anker; eenvoudig, één fase, beperkt vermogen); thuisbatterij met hybride omvormer (door een installateur, meer vermogen, soms noodstroom); combinatie met nieuwe zonnepanelen.
- Prijs per kWh (incl. installatie en btw), garantie (jaren en/of cycli), eigen verbruik in stand-by (W; telt mee: 15 W continu is ca. 130 kWh per jaar), rendement heen en terug, minimum laadtoestand, maximaal laad- en ontlaadvermogen, plaats (binnen of in een koude ruimte).
- Regels: moet de batterij aangemeld worden bij de netbeheerder? Zijn er premies of is er een btw-regeling? Zijn er beperkingen voor stekkerbatterijen? Laat me dat nagaan bij de officiële bronnen; geef geen verouderde premie-informatie als feit.

Contracten:
- Welke contracten wil ik vergelijken? Mijn huidig contract, een of meer dynamische contracten, en eventueel aanbiedingen die ik kreeg. In Vlaanderen is de V-test van de Vlaamse Nutsregulator de officiële, onafhankelijke vergelijker. Die kan gekoppeld worden aan Mijn Fluvius, werken met een opgeladen CSV met minstens een jaar kwartierdata, of rekenen met ingegeven jaarverbruik en standaardprofielen. Ook dynamische contracten kan hij zo tonen, maar met echte kwartierdata is de vergelijking voor mijn verbruikspatroon veel nauwkeuriger. Gebruik de V-test (bij voorkeur met kwartierdata) als onafhankelijke controle van de eigen berekening, en verklaar verschillen (prijsaannames, contractvoorwaarden, periode).

Vat op het einde alles samen in één overzicht en laat me dat bevestigen of corrigeren. Bewaar dat overzicht (zonder geheimen) als `installatie.md` in de projectmap.

## Fase 2 - De machine nakijken (alleen lezen)

Controleer zonder iets te wijzigen: OS en versie, Python 3, vrije schijfruimte, Docker, systemd, tijdzone en tijdsynchronisatie (NTP; tijden in rapporten moeten kloppen), of de opgegeven toestellen bereikbaar zijn (ping, poort open), welke poorten openstaan en voor wie (firewall, Docker-containers; bij WSL ook de netwerkmodus, systemd en de Windows-firewall), en of de meter al data geeft. Voor de meter concreet: lees één meting en meld welke velden er zijn (vermogen, stroom en spanning per fase; tellers afname en injectie per tarief; lopend kwartiergemiddelde en maandpiek), om de hoeveel seconden er een nieuwe waarde komt, of het teken bij injectie klopt (vergelijk met de zon of de app), en of het aantal fasen overeenkomt met blok B. Zeg wat er ontbreekt en welke modules daardoor niet of minder goed kunnen (bv. geen stroom per fase: geen bewaking van de hoofdzekering). Ontbreken kwartiergemiddelde of maandpiek: bereken ze zelf uit de tellerstanden van de afname (kwartieren op de klok) en markeer kwartieren met ontbrekende of onvolledige metingen. Sla het meternummer of serienummer niet op buiten `.env`. Kijk of er al andere software draait die dezelfde toestellen aanspreekt (dubbele verbindingen). Draait er al Home Assistant: maak een lijst van de integraties en automatiseringen die de betrokken toestellen lezen of sturen, zonder iets te wijzigen. Meld wat ontbreekt en wat ik zelf moet doen (bv. de lokale API aanzetten in een app of een token ophalen, DHCP-reservatie in de router).

## Fase 3 - Plan voorstellen

### Eerst: zelf bouwen of bestaande software gebruiken?
Weeg eerlijk af en leg me de keuze voor:
- **Bestaande pakketten**: evcc (laden van auto's, veel laadpalen en auto's ondersteund, eigen webinterface; voor sommige laadpalen een betaald "sponsor token"), EMHASS (planning van batterij en verschuifbare toestellen op prijs en voorspelling, via Home Assistant), Predbat (batterijplanning op dynamische tarieven, sterk in het VK), SEM en PV Excess Control (overschot verdelen, Home Assistant). Ook combinaties zijn mogelijk, bv. een planner die beslist en evcc die het laden uitvoert.
- **Zelf bouwen** (zoals het voorbeeldsysteem): volledige controle, ook voor toestellen of regels die pakketten niet kennen (bv. een batterij via Modbus zonder integratie, het Vlaamse capaciteitstarief), maar meer onderhoud.
- **Mengvorm**: een bestaand pakket voor wat het goed doet, eigen modules voor de rest. Let dan op dat twee systemen nooit hetzelfde toestel sturen.

### Daarna: het plan
Bij het profiel "advies vóór aankoop" is het plan kort: data inlezen (of eerst een tijd meten), module 19, en een adviesrapport; er wordt niets gestuurd en niets in huis gewijzigd. Bij de andere profielen: stel een plan voor met enkel de modules die bij mijn installatie en keuzes passen (catalogus hieronder), in volgorde, met per stap: wat het doet, wat er verandert op mijn machine, en hoe we controleren dat het werkt. Vermeld welke instellingen in toestellen of apps ik zelf moet wijzigen en hoe ik ze terugzet. Wacht op mijn akkoord.

### Catalogus van modules (alles optioneel behalve 1)
1. **Meter uitlezen en loggen** (verplicht, behalve bij enkel advies vóór aankoop met bestaande data): elke paar seconden, met kwartiergemiddelde, maandpiek en stroom per fase als de meter die geeft.
2. **Dashboard**: live vermogen, grafiek 24 u/7 d, batterijen, zon, auto, kosten, en wat het systeem nu doet en waarom (in gewone taal).
3. **Zon**: meten en/of voorspellen, met vergelijking per dag en eventueel automatische correctie van de voorspelling.
4. **Verbruiksvoorspelling**: het huisverbruik per weekdag en uur voorspellen uit de eigen historiek (afwezige dagen uitgesloten). Nodig voor elke batterijplanning.
5. **Prijzen**: day-ahead-prijzen (bv. via ENTSO-E, gratis token nodig) of de prijsformule van mijn contract; eventueel CO2-intensiteit van het net.
6. **Batterijen uitlezen**, inclusief temperatuur en gezondheid.
7. **Batterijen sturen** (op overschot, eventueel op prijs en/of kwartierpiek).
8. **EV-sturing** (zon, minimum + zon, minimum-range, vertrektijd, goedkope uren, reismodus).
9. **Andere toestellen schakelen** (boiler, warmtepomp, pompen, slimme stekkers).
10. **Bewaking van de hoofdzekering per fase.**
11. **Handmatig ingrijpen met eindtijd** (tijdelijke voorrang, daarna vanzelf terug naar automatisch).
12. **Afwezigheidsmodus.**
13. **Kostenberekening** volgens mijn contract, met tellers per dag/maand, inclusief vaste kosten.
14. **Rapporten** (dagelijks PDF, wekelijks/maandelijks).
15. **Bewaking met meldingen**.
16. **Home Assistant-koppeling** via MQTT Discovery.
17. **Back-up** en **noodknop** (alle automatische sturing veilig stoppen; geen fabrieksreset).
18. **Analyses** achteraf: wat brengen de batterijen en de sturing echt op, loont een extra batterij, terugverdientijd.
19. **Wat-als en advies** (ook zonder installatie): tariefvergelijking, schaduwfactuur, en simulaties van zonnepanelen, batterijen (hoeveel?), slim laden en warmtepomp met mijn eigen verbruik. Resultaat: een adviesrapport (PDF).

## Fase 4 - Bouwen

### Basisprincipes
- Eén projectmap (bv. `~/ems`) met een Python-venv en een git-repository. Een `AGENTS.md` in die map die je bijhoudt: wat er draait, waarom, instellingen, geleerde lessen, met datum. Zo kan een volgende sessie verder zonder alles opnieuw uit te zoeken.
- **Kernregels in `AGENTS.md`**: veel agents laden hun notitiebestand elke sessie automatisch, dit promptbestand niet (en na het samenvatten van een lang gesprek kan detail verloren gaan). Werk je in een chat, dan laad je het zelf op. Zet daarom bovenaan `AGENTS.md` een korte sectie "Regels en keuzes": de harde grenzen (zie hieronder), mijn voorkeuren (bv. nooit uit het net laden, prioriteitenlijst, comfortgrenzen), de werkafspraken, en een verwijzing naar `installatie.md` en dit promptbestand. Lees bij elke nieuwe sessie eerst `AGENTS.md` en `installatie.md` voor je iets doet, en werk die sectie bij als ik een keuze wijzig. Of een agent zijn notitiebestand automatisch inleest, verschilt per agent en per versie: controleer bij het begin van elke sessie dat de regels echt geladen zijn, bv. door de assistent de harde grenzen en mijn belangrijkste keuzes kort te laten herhalen.
- Geheimen (tokens, wachtwoorden) enkel in `.env` (in `.gitignore`). Instellingen in `config.yaml`, met een `config.example.yaml` zonder geheimen.
- Elk onderdeel een eigen systemd-service of -timer met automatische herstart; alles start vanzelf na een herstart van de machine. Timers die dagelijks lopen: let op met `Persistent=true` (na een herinstallatie kan die meteen een "gemiste" run starten met een onvolledige dag).
- Alles werkt lokaal, ook zonder internet. Enkel prijzen, voorspellingen en meldingen hebben internet nodig; valt dat weg, dan stuurt het systeem veilig verder op de meter.
- MQTT-broker en Home Assistant (als gewenst) via Docker Compose. Elke MQTT-client krijgt een unieke client_id (dezelfde id = clients gooien elkaar eruit). Broker met wachtwoord.
- Opslag in SQLite (tijden in UTC, WAL-modus aan), één rij per meting. Toon tijden altijd in lokale tijd.
- Elke module krijgt tests, elke stuurregel een test met een realistisch scenario uit de echte metingen.
- **Tarieven met geldigheidsdatum**: zet nettarieven, heffingen, btw en vaste kosten niet in de code maar in één bestand met per periode "geldig van/tot" en de bron. Elk tijdstip wordt gerekend met de periode die toen gold (dan rekent een herberekening van vorig jaar niet met de tarieven van dit jaar). Herinnering in december zolang de tarieven voor volgend jaar ontbreken, en een alarm zodra de laatste periode verlopen is; er wordt dan zichtbaar met de oude waarden verder gerekend.
- **Observatiemodus (dry-run)**: elke module die iets stuurt heeft een schakelaar waarmee ze enkel logt en toont wat ze zou doen. Nieuwe sturing loopt eerst minstens een dag zo; daarna vergelijken we wat ze gedaan zou hebben met wat er gebeurde.
- **Eén sturing per toestel**: voor je een toestel gaat sturen, controleer of niets anders het nog stuurt (app, Home Assistant, eigen logica van het toestel, een ander pakket). Er zijn twee nette oplossingen: de andere sturing uitzetten, of ermee samenwerken via zijn eigen API (bv. evcc een laadmodus of planning geven en evcc het laden laten uitvoeren). Leg vast wie beslist en wie uitvoert.
- **Lezen en sturen via wat er al is**: praat Home Assistant (of een ander systeem) al met een toestel, gebruik dan die weg (de API of MQTT van Home Assistant) in plaats van een tweede rechtstreekse verbinding te openen. Veel toestellen aanvaarden maar één verbinding, en twee systemen die hetzelfde toestel aanspreken, geven fouten die moeilijk te vinden zijn.
- **Uitleg bij elke beslissing**: elke stuurbeslissing krijgt een korte reden in gewone taal ("Batterij laadt niet: auto heeft voorrang, overschot 2,1 kW"), zichtbaar op het dashboard en in de logs.
- **Noodknop**: één commando of dashboardknop die alle automatische sturing veilig stopt en elk toestel in zijn vooraf geteste veilige toestand zet. Werk met een vlag (bv. een bestand) die de sturing zelf ook leest: zolang ze staat, voert geen enkel onderdeel nog gewone stuurcommando's uit, ook niet na een herstart, terwijl metingen, dashboard en rapporten gewoon doorlopen. De veiligheidslaag mag (en moet) wel de commando's blijven sturen en controleren die nodig zijn om elk toestel in zijn veilige toestand te houden (bv. bij een batterij zonder terugval: periodiek opnieuw stand-by 0 W). De noodknop schrijft daarnaast zelf rechtstreeks naar de toestellen (los van de sturingsprogramma's), leest de werkelijke toestand terug, controleert na een halve minuut opnieuw of niets de controle teruggenomen heeft, en meldt het resultaat (mail). Zolang de noodstop actief is: rode balk op het dashboard en een herinnering via de bewaking, zodat ze niet vergeten wordt. Leg per toestel vast wat de veilige toestand is, hoe je er komt en hoe je ze terugleest (bv. laadpaal: laden stoppen; batterij: standaard stand-by op 0 W; de eigen modus van het toestel enkel als een echte test met bewaking bewezen heeft dat die veilig is: in het voorbeeldsysteem ontlaadde een batterij in "zelfconsumptie" binnen 10 s 2,5 kW naar het net, terwijl de app het net correct toonde). Een tweede commando heft de noodstop op. Na het opheffen herbegint de sturing nooit met een oud setpoint of een oude planning: eerst verse meterwaarden, de toestand van elk toestel en de veiligheidsgrenzen opnieuw controleren, dan een nieuwe planning berekenen. Test beide bij de oplevering.
- **Veiligheidslaag**: één centraal onderdeel met voorrang op alle modules (batterij, auto, warmtepomp, ...) beslist het laatste woord over wat elk toestel mag doen. Het controleert vóór elk commando de harde grenzen (verse en geldige data, stroom per fase, maximale vermogens, temperatuur, communicatie met het toestel, noodstop-vlag, uitzonderingen) en vraagt bij een overtreding de vooraf geteste veilige toestand. Die controle draait in elke stuurcyclus (seconden) en grijpt zelf meteen in; ze wacht nooit op de bewaking. Zo reageert niet elke module op haar eigen manier op bv. ontbrekende meterdata of een te hoge fasestroom. Die laag draait op dezelfde machine en vervangt dus geen beveiliging in het toestel zelf.
- **Uitval: drie gevallen**, elk met een eigen antwoord. (1) **Een programma valt uit of loopt vast**: systemd herstart het, een stop-actie (bv. ExecStopPost) en een aparte timer zetten de toestellen in hun veilige toestand. (2) **Het netwerk valt uit** (router, wifi, kabel): de machine draait nog maar bereikt de toestellen niet; het systeem blijft opnieuw proberen en meldt het, maar kan niets veilig zetten wat het niet bereikt. (3) **De hele machine valt uit** (stroom, defect, Windows-herstart bij WSL): dan grijpt thuis niets meer in. Een bewaking of failsafe op dezelfde computer helpt dan niet; enkel een time-out of terugval in het toestel zelf, of een tweede onafhankelijk toestel, beschermt dan. Gebruik zo'n time-out waar het toestel er een heeft, zeg eerlijk welke toestellen er geen hebben (dan blijven ze hun laatste commando uitvoeren), en zorg met het externe levensteken dat ik het snel weet. Een melding is geen beveiliging: een toestel zonder eigen time-out is onder externe sturing niet uitvalveilig. Stel live sturing van zo'n toestel dus nooit voor als uitvalveilig. Kies per zo'n toestel één van twee wegen. (a) Voorzie een onafhankelijke terugval en test die echt: bv. een aparte, geteste controller die bij stilte de batterij in de veilige toestand zet, of een watchdog in het toestel zelf. (b) Of leg het resterende risico vast in `AGENTS.md` (wat er kan gebeuren, hoe lang, met welk vermogen) en laat mij uitdrukkelijk kiezen of ik dat aanvaard. Een UPS telt niet als onafhankelijke terugval: hij overbrugt enkel een stroomonderbreking van machine en netwerk, en helpt niet bij een vastgelopen of defecte computer of een netwerkprobleem.
- Voor elke wijziging aan instellingen of code: back-up van het oude bestand (met datum in de naam) en noteren hoe terug te draaien.
- Updates van het systeem zelf (Python-pakketten, Docker-containers, Home Assistant): nooit automatisch; enkel na akkoord, bij voorkeur op een rustig moment, met de mogelijkheid om terug te gaan. Uitzondering: veiligheidsupdates van het besturingssysteem mogen automatisch (bv. unattended-upgrades), zonder automatische herstart.
- **Beveiliging**: een firewall op de machine. Basisregel, op elk platform dezelfde: alles vanaf het thuisnetwerk en de VPN toelaten, al de rest dicht, en niets openzetten in de router. Per dienst strenger afschermen (bv. MQTT of Modbus enkel lokaal) is mogelijk, maar optioneel. Laad nieuwe firewallregels altijd met een automatische terugval (zonder mijn bevestiging binnen 5 minuten komen de oude regels terug), zodat ik mezelf niet kan buitensluiten; houd SSH en de VPN altijd open. Per platform: Debian, Ubuntu en Raspberry Pi OS met ufw of nftables (staan standaard open); poorten van Docker-containers omzeilen ufw en de gewone INPUT-regels, dus afschermen in de DOCKER-USER-keten of de poort enkel aan het nodige adres binden; bij WSL 2 is de Windows-firewall (en de Hyper-V-firewall voor WSL) de echte poort, een firewall binnen Linux beschermt daar weinig. Verder: dashboard, Home Assistant en MQTT-broker met wachtwoord; nooit iets rechtstreeks op internet openzetten; SSH enkel met sleutel. Tokens en wachtwoorden nooit in git, logs, rapporten of mails.
- **Zomer- en wintertijd**: reken intern in UTC. Een dag met de klokwissel heeft 23 of 25 uur (92 of 100 kwartieren); rapporten, kwartierpieken, dagtotalen en geïmporteerde CSV's (vaak in lokale tijd, met een dubbel uur in oktober) moeten daar correct mee omgaan. Test het met de echte wisseldagen. Valkuil uit het voorbeeldsysteem: gebruik nooit een lokale tijd als sleutel om kwartieren of uren te groeperen. In Python zijn twee lokale tijdstippen met dezelfde tijdzone gelijk als de klok hetzelfde aangeeft (02:15 zomertijd = 02:15 wintertijd), zodat de twee kwartieren van het dubbele uur ongemerkt samengevoegd en uitgemiddeld worden. Groepeer in UTC en zet enkel voor de weergave om. Een UTC-tijdstip rond middernacht hoort bij de lokale dag (bv. voor het tarief van 1 januari).
- **Datakwaliteit**: gaten in de metingen (uitval), tellers die terug op nul springen (meter vervangen, herstart) en onmogelijke waarden herkennen, markeren en niet blind meetellen. Bij geïmporteerde data: decimale komma, eenheden (kWh of Wh) en tijdzone controleren.
- **Onderhoud van de database**: ruwe data na de gekozen bewaartijd samenvatten (bv. per kwartier), WAL-bestand regelmatig opruimen, logbestanden begrenzen (journald), en de schijfruimte bewaken.
- **Externe diensten**: respecteer de limieten van gratis diensten (bv. Forecast.Solar enkele aanvragen per uur), bewaar resultaten in een cache, en laat het systeem gewoon verder werken als een dienst niet antwoordt.
- **Replay-tool**: een script dat een stuurregel opnieuw afspeelt op echte historische metingen (zonder hardware), zodat een wijziging eerst op voorbije dagen getest wordt voor ze live gaat.
- **Een bestaande Home Assistant wijzigen**: eerst een volledige back-up; eigen instellingen in een apart package-bestand (bv. `packages/ems.yaml`) en niet in bestaande bestanden; niets aan bestaande automatiseringen, scripts of dashboards wijzigen zonder akkoord; de configuratie laten controleren vóór elke herstart; en noteren hoe alles terug te draaien is.
- **Herbouwbaar**: alles wat nodig is om het systeem op een nieuwe machine terug te zetten (code in git, `.env`, configuratie, database uit de back-up, systemd-units, Docker-bestanden) staat beschreven in `AGENTS.md`.
- **Back-up die echt terug te zetten is** (lessen uit de terugzet-test in het voorbeeldsysteem):
  - Databases nooit gewoon als bestand kopiëren terwijl erin geschreven wordt. Maak eerst een consistente kopie en neem die mee: SQLite met `VACUUM INTO` (één leestransactie, enkele seconden). `sqlite3 .backup` is ook een consistente methode, maar kopieert in stukken en begint opnieuw zodra een ander programma schrijft; bij een database waarin elke paar seconden geschreven wordt, raakte die in het voorbeeld nooit klaar. PostgreSQL (bv. TeslaMate): met `pg_dump`. Controleer de kopie (`PRAGMA quick_check`) vóór de back-up.
  - Neem alles mee wat bij een herbouw nodig is, niet enkel de projectmap: ook de systemd-aanvullingen (`*.service.d`, daar zitten de failsafes bij het stoppen), het back-upscript zelf, sudo-regels, Docker-compose-bestanden van andere containers, configuraties van ESP-modules en eigen aanpassingen eraan. Laat herbouwbare dingen weg (Python-omgeving, buildcache), maar test dat ze herbouwbaar zijn.
  - Het wachtwoord van de versleutelde back-up mag niet enkel op de machine zelf staan: gaat die schijf kapot, dan is de back-up onbruikbaar. Laat de gebruiker het bewaren in een wachtwoordmanager of op papier, en toon het nooit in een rapport of mail.
  - Test het terugzetten echt, eenmalig volledig (naar een aparte map: terugzettijd, integriteit van de databases, configuratie aanwezig, Python-omgeving opnieuw opbouwen uit `requirements.txt` en de tests laten slagen) en daarna maandelijks automatisch (`restic check` met een deel van de data, de databasekopieën terugzetten en controleren, leeftijd van de laatste meting, mail met het resultaat). Verwijder de testmap daarna: hij bevat een kopie van alle wachtwoorden.

### Volgorde (elke stap eerst laten werken en tonen, dan pas de volgende)
1. Meter uitlezen en loggen.
2. Dashboard, volgens de keuzes in blok I (kleurenblindheid, toestel, lettergrootte, thema).
3. Zon, prijzen en verbruiksvoorspelling.
4. Batterijen en andere stuurbare toestellen ALLEEN LEZEN, minstens een dag, en vergelijken met de app.
5. **Veiligheid vóór sturing**: veiligheidslaag, noodknop (stoppen én hervatten), failsafes (bij stoppen en via een aparte timer), bewaking met meldingen, extern levensteken, back-up en een beschreven herstelprocedure. Alles werkt en is getest (noodknop en failsafe één keer echt, terwijl ik erbij ben) vóór er ook maar één toestel live gestuurd wordt. Daarvoor zijn gecontroleerde, handmatige hardwarecommando's toegestaan terwijl ik erbij ben: het zijn echte acties op het toestel, maar geen automatische sturing (die staat dan nog uit). Leg vooraf de vermogensgrenzen, het verwachte resultaat en de herstelprocedure vast. Een test vanuit 0 W bewijst niet dat de noodknop of failsafe een actief laad- of ontlaadcommando kan beëindigen: zet daarom eerst handmatig een klein vermogen (bv. 300 W laden of ontladen), controleer dat het toestel dat uitvoert, en test vandaar de overgang naar de veilige toestand. Bespreek dan ook welke toestellen niet uitvalveilig zijn (zie "Uitval") en leg mijn keuze vast.
6. Batterijen sturen: eerst observatiemodus (minstens een dag), dan één toestel met een klein vermogen terwijl ik erbij ben (teken en reactie controleren), dan live.
7. EV-sturing, op dezelfde manier.
8. Andere toestellen, op dezelfde manier.
9. Kosten en rapporten.
10. Home Assistant-koppeling, analyses, uitleg voor gezinsleden.
11. Evaluatie na 1 week en na 1 maand (zie onderaan).

## Regels en lessen

### Algemeen sturen
- Stuur nooit op oude data. Is de laatste meterwaarde ouder dan ca. 30 s: batterijen naar hun veilige toestand (meestal stand-by 0 W), geforceerd laden van de auto stoppen, en waarschuwen. Doe na elke mislukte databaseschrijfactie een rollback (anders blijft een verbinding op een oude momentopname hangen en stuurt het systeem urenlang op die oude waarde).
- Stuur altijd expliciet een eindtoestand (bv. 0 W) als er niets mag. "Niets sturen" laat bij veel toestellen het vorige commando eindeloos doorlopen.
- Ruis dempen: stuur op een gemiddelde van de meter over ca. 10 s (niet langer dan de stuurcyclus, anders telt een afname dubbel), met een hysterese (ca. 200 W) en een minimale tijd tussen omschakelen van richting (ca. 180 s). Zonder dat gaan toestellen tientallen keren per uur heen en weer. Die wachttijd en hysterese gelden enkel voor het omschakelen naar de andere richting: minder laden of ontladen, naar 0 W gaan en elke ingreep van de veiligheidslaag gebeuren altijd meteen (zie de regels over netladen en ontladen naar het net hieronder).
- Een "werkpunt": hou een kleine marge (bv. 50-100 W afname) aan in plaats van exact 0 W, zodat kleine schommelingen geen teruglevering of netladen geven.
- Let op twee regelkringen die op elkaar reageren via dezelfde meter (bv. batterij en laadpaal die elk hun eigen logica hebben): dat geeft schommelingen van duizenden watt.
- Prioriteit van zonne-overschot volgens de ene prioriteitenlijst uit blok G.
- Herbereken plannen zodra er iets verandert (nieuwe prijzen, nieuwe voorspelling, auto ingeplugd) en controleer ze nog eens kort voor een goedkoop venster afloopt.
- Na een herstart: sprongen in tellers (kWh, kosten) negeren of afvlakken, en eerst verse metingen afwachten voor je stuurt.
- Na een stroomonderbreking: de machine, de router en de toestellen starten niet in dezelfde volgorde op. Het systeem blijft opnieuw proberen te verbinden (zonder te crashen), stuurt pas als alle nodige data vers zijn, en controleert of toestellen in de verwachte modus staan (sommige vallen terug op hun fabrieksmodus).
- Firmware van elk toestel periodiek uitlezen (waar dat kan) en een melding sturen als die verandert.
- Schrijf nooit naar een register of instelling van een toestel die je niet in documentatie of een betrouwbare bron gevonden hebt, en nooit "om te proberen". Verkennen gebeurt alleen-lezend. Een verkeerde schrijfactie kan instellingen wijzigen die je niet meer terugvindt.
- Sommige instellingen worden in het flashgeheugen van een toestel bewaard, dat slijt bij duizenden schrijfacties. Schrijf instellingen enkel bij een echte wijziging; enkel setpoints die daarvoor bedoeld zijn, mogen elke cyclus herhaald worden. Ga bij twijfel na welk soort register het is.
- Netspanning per fase opvolgen (de meter geeft die meestal): bij te hoge spanning (in België boven ca. 253 V) schakelen omvormers zich af en gaat zonne-opbrengst verloren. Toon het in het rapport; laden op dat moment helpt de spanning te drukken.
- De failsafe en de noodknop af en toe (bv. elke maand) testen; een veiligheidsmechanisme dat nooit getest wordt, werkt vaak niet als het nodig is. Automatiseer het lezende deel (bv. wekelijks, mail bij afwijking): zijn de failsafes bij het stoppen nog geladen, staan de failsafe-timers aan, zijn de registers leesbaar die de noodknop nodig heeft, slaagt een proefrun (dry-run) van elke failsafe, en staat er geen vergeten noodstop-vlag. Het echte ingrijpen test je met de hand, terwijl je erbij bent.
- Onverklaarde patronen eerst voorleggen: vaak is het een gewoon toestel in huis (microgolfoven, vuurtje, warmtewisselaar, pomp), geen fout. Ook het weer verklaart veel: sneeuw of vuil op de panelen (zon ver onder de voorspelling), hitte, onweer met netstoringen.

### Hoofdzekering per fase
- Los van het capaciteitstarief: bewaak de stroom per fase. Komen auto, warmtepomp en andere toestellen samen boven de hoofdzekering op één fase (met marge, bv. 90%), dan eerst de stuurbare lasten op die fase verlagen of stoppen. Ook als het kwartiergemiddelde laag blijft.
- De grootte van de hoofdzekering staat niet altijd op papier: leid ze af uit het contractueel vermogen bij de netbeheerder (bv. "Mijn Fluvius"): 17,3 kVA driefasig = 3N400 V met 25 A per fase; 9,2 kVA eenfasig = 40 A; 3x230 V met 40 A = 15,9 kVA. Vraag het na als het niet klopt.
- Sla de stroom per fase (met teken: injectie belast de zekering evengoed) en de spanning per fase bij elke meting op; veel P1-uitlezingen leveren ze, maar ze worden makkelijk weggegooid. Het begrenzen zelf gebeurt meteen, in elke stuurcyclus, door de veiligheidslaag; de bewaking hieronder meldt enkel. Bewaking: waarschuwing bij > 80 % van de zekering gedurende 1 min, alarm bij > 100 % gedurende 30 s, en netspanning buiten 207-253 V (230 V +-10 %) gedurende 1 min (te hoge spanning laat omvormers afschakelen). Kijk bij elke controle ca. 10 minuten terug, zodat ook een kort voorval zeker gemeld wordt.

### Batterijen
- Bereken het overschot zelf uit de meter (negatief = teruglevering) en verdeel het over de batterijen, bv. naar restcapaciteit. Laat toestellen niet elk hun eigen automatische modus draaien: ze coördineren niet en werken elkaar tegen.
- Nooit uit het net laden (als dat gekozen is): zodra er afname is terwijl de batterijen laden, het laden onmiddellijk met precies die afname verlagen, zonder vertraging of demping.
- Nooit naar het net ontladen (als dat gekozen is): bij teruglevering het ontladen direct stoppen.
- Bij laden: het hoogste van het 10 s-gemiddelde en een 4 s-gemiddelde gebruiken, zodat een wolk snel tot minder laden leidt. Het laadvermogen per cyclus maar beperkt laten stijgen (ca. 250 W per toestel); minder laden mag altijd meteen.
- Begrens het laden op de gemeten zonneproductie als die gekend is.
- Veel toestellen hebben in een "passieve" of "remote" modus geen automatische terugkeer: herhaal het setpoint elke cyclus, en zet ze bij stoppen uitdrukkelijk in hun vooraf geteste veilige toestand (zie "Noodknop"; dat is niet altijd de eigen modus van het toestel).
- Teken (laden negatief of positief?) en capaciteit: probeer ze automatisch te herkennen uit de metingen, maar controleer altijd met een klein vermogen op echte hardware en laat mij bevestigen voordat iets continu stuurt.
- Sommige toestellen stoppen zelf met ontladen op een SoC-grens en hervatten pas een paar procent hoger. Leer die grens uit de metingen en vraag in die zone geen ontlaadvermogen.
- Temperatuur: bij lage temperatuur laden veel batterijen beperkt; toon dat als verklaring, niet als fout.
- Veel batterijen aanvaarden maar één Modbus-verbinding tegelijk: gebruik een kleine Modbus-proxy met een time-out (bv. 5 s), anders blokkeert één hangend verzoek alles. Beperk ook de wachtrij (oude verzoeken weggooien in plaats van opstapelen) en laat de proxy een vastgelopen verbinding met het toestel zelf sluiten en opnieuw openen. Alleen het EMS praat met de proxy.
- Sla per toestel en per cyclus drie dingen apart op: het gevraagde setpoint, het werkelijk gemeten vermogen en de modus die het toestel zelf meldt. "Schrijven gelukt" betekent niet dat het toestel doet wat gevraagd is: vergelijk telkens gevraagd met gemeten en meld een blijvend verschil (begrenzing in de app, verkeerde modus, stilgevallen communicatie). Geef elk soort commando per toestel een instelbare verificatietermijn (batterij: enkele tientallen seconden; laadpaal: ca. een minuut; warmtepomp: minuten) en een vooraf bepaalde veilige actie als het toestel binnen die termijn niet doet wat gevraagd is. Een toestel dat de verkeerde richting uitgaat (ontladen terwijl laden of 0 W gevraagd is, of omgekeerd) gaat meteen naar zijn veilige toestand.
- Firmware-updates kunnen het gedrag veranderen (en sommige toestellen updaten zichzelf via de cloud). Noteer de firmwareversie, laat de bewaking die elk uur uitlezen en melden als ze wijzigt, controleer na elke update het gedrag, en update bij meerdere toestellen eerst één.
- Blijft het ontladen te laag: kijk eerst naar vermogensinstellingen in de app van de fabrikant.
- Gezondheid opvolgen: aantal volle cycli, temperatuur, en (als het toestel het geeft) capaciteit/State of Health per maand.
- Kalibratie: sommige batterijen moeten af en toe volledig opladen om de laadtoestand juist te houden, andere doen dat zelf of hebben het niet nodig. Zoek per batterij op wat de fabrikant voorschrijft en volg dat; plan enkel als de fabrikant het vraagt (of als de laadtoestand aantoonbaar afwijkt) periodiek een volle lading op een zonnige dag, ook als er een maximum (bv. 90%) ingesteld is. Een laadtoestand die plots verspringt, kan een teken zijn dat kalibratie nodig is.
- Bij hitte beperken batterijen soms hun vermogen; toon dat net als bij vorst als verklaring.

### Prijssturing (enkel met variabel of dynamisch contract)
- Haal de day-ahead-prijzen op (per kwartier of uur; morgen meestal beschikbaar vanaf de vroege namiddag) en reken ze om met de formule van mijn contract. Beslis op de marginale prijs: wat één extra kWh afname kost (of injectie oplevert) op dat kwartier, dus energie plus de netkosten en heffingen per kWh plus btw, niet op de kale marktprijs. Vaste kosten per jaar of maand tellen daarin niet mee; het capaciteitstarief komt via de piekregel hieronder. Voor de factuur en de schaduwfactuur reken je wel met alle kosten.
- Batterij uit het net laden (als gekozen): enkel als het verschil tussen goedkope en dure uren groter is dan de verliezen (rendement heen en terug meestal 80-90%) plus een slijtagekost per kWh. Laad niet uit het net als de zon- en verbruiksvoorspelling zeggen dat de batterij die dag toch vol raakt. Hou rekening met de kwartierpiek: netladen mag de maandpiek niet verhogen.
- Batterij ontladen op dure uren: hou genoeg over voor de duurste uren van de avond (volgens de verbruiksvoorspelling); ontladen naar het net enkel als dat gekozen is en het contract het beloont.
- Negatieve prijzen: verbruik verschuiven naar die uren (batterij, auto, boiler), en eventueel de omvormer begrenzen als injectie dan geld kost (enkel als dat mag en kan).
- Auto: met een vertrektijd en doel de goedkoopste uren kiezen die nog op tijd volstaan; 's nachts minder laden als morgen veel zon voorspeld is; altijd een minimum-range aanhouden.
- Optioneel: sturen op CO2-intensiteit van het net in plaats van (of naast) de prijs.
- Toon de planning (welke uren laden/ontladen en waarom) in een tabel of grafiek op het dashboard.
- Maak een overzicht per dag: wat de prijssturing opbracht tegenover gewoon zelfverbruik. Is de winst klein, zeg het eerlijk.

### Capaciteitstarief (Vlaanderen; andere regio's: eigen regels nagaan)
- Rekenregel (Vlaanderen, controleer de actuele regels): de factuur gebruikt het gemiddelde van de maandpieken van de laatste 12 maanden, met minimaal 2,5 kW per maand. Een hogere maandpiek werkt dus 12 maanden door in dat gemiddelde, ook over de jaarwissel heen; een piek onder 2,5 kW kost niets extra. Laat het systeem de kost van een piek uitrekenen over die 12 maanden, en de kostenteller met het voortschrijdende gemiddelde rekenen, niet met de piek van de lopende maand. Op de factuur: bij een maandafrekening wordt de gemiddelde maandpiek van die maand aangerekend (dat is het 12-maandengemiddelde zoals het in die maand geldt, niet de piek van die maand zelf); bij een jaarafrekening de facturatiepiek, het gewogen gemiddelde (naar het aantal dagen) van de gemiddelde maandpieken over de afrekenperiode. Gebruik voor een exacte schaduwfactuur de werkelijke afrekenperiode, en controleer tegen een factuur en de maandpieken in het portaal van de netbeheerder.
- Stuurbare lasten (auto, netladen, boiler) mogen het lopende kwartier nooit boven max(2,5 kW, maandpiek tot nu) brengen, min een kleine marge. Een hogere grens is geen doel.
- Gebruik het kwartiergemiddelde van de meter zelf (kwartieren op de klok; geeft de meter het niet, bereken het dan uit de tellerstand van de afname) en bereken wat er nog mag zodat het kwartier op het budget eindigt. Stop of verlaag snel (binnen enkele seconden) als het kwartier dreigt over te gaan; op het einde van een kwartier geen opgespaarde ruimte meer benutten. Een kwartierwaarde die het systeem zelf berekent (uit de tellerstand of uit vermogensmetingen), is voorlopig: de gevalideerde kwartierwaarde van de netbeheerder (bv. in Mijn Fluvius) is de definitieve en telt voor de factuur. Toon dat onderscheid, vergelijk beide na een paar dagen, en stuur met een kleine marge.
- Ontladen van de batterij om een piek te drukken kan een optie zijn (blok E).
- Toon de top-5 kwartierpieken per dag en de maandpiek in het rapport.

### Auto (enkel met EV)
- Modi (naargelang de keuzes in blok F): "zon" (enkel overschot; starten als overschot minstens het minimale laadvermogen + ca. 200 W een tijd aanhoudt, stoppen na ca. 200 s afname), "minimum + zon", "moet" (onder de minimum-range: uit zon of net, binnen het kwartierbudget), "vertrektijd", "goedkoopste uren", "reis" (tot 100%, via een MQTT-schakelaar of dashboardknop, zet zichzelf uit als de auto vol is), "altijd maximaal", "uit". Range onbekend of verouderd = de veilige keuze (zon).
- Batterijen wijken voor de auto (als dat gekozen is): niet ontladen om de auto te voeden, niet laden terwijl de auto net vermogen nodig heeft. Trek het vermogen van de auto niet dubbel af (de meter bevat het al).
- Fase-omschakeling (als de laadpaal het kan): 1 fase bij weinig overschot, 3 fasen bij veel. Enkel omschakelen als hij niet laadt, met minstens 15 min tussen twee wissels. Gebruik bij de keuze het net "alsof de batterijen stilstaan", anders ontstaat een lus van starten, stoppen en omschakelen. Stopt hij op 3 fasen terwijl er genoeg is voor 1 fase: snel herstarten op 1 fase.
- Laadstroom bijregelen binnen het budget (minimum meestal 6 A per fase).
- Meerdere laadpalen: overschot verdelen volgens de prioriteitenlijst; nooit twee auto's tegelijk laten starten.
- Bijna vol herkennen: neemt de laadstroom af terwijl er ruimte is, dan is de auto aan het afbouwen; geef de vrijgekomen ruimte aan andere toestellen.
- Zonder koppeling met de auto: laadtoestand schatten uit geladen kWh en verbruik, en het verbruik per km leren uit de ritten.
- De auto niet onnodig wakker maken: vraag de status niet te vaak op (dat kost de auto batterij). TeslaMate doet dat goed; bij andere integraties de vraagfrequentie beperken als de auto niet laadt.
- Een onafhankelijke failsafe (eigen timer, rechtstreeks naar de laadpaal): als het EMS stopt of geen metingen meer schrijft, geforceerd laden beëindigen en de stroom terugzetten; ook bij elke stop of crash van de hoofdservice.
- Log elke wijziging van de laadpaalstand; herstel onverklaarde wijzigingen en vermeld ze in het rapport.
- Het EMS kan een auto meestal niet zelf doen starten (dat gaat via de auto of de app). Stop als de auto een tijd niets afneemt en probeer pas later opnieuw.

### Andere toestellen
- Per toestel: aan bij overschot boven zijn vermogen + marge gedurende een tijd, uit bij afname, met minimum aan- en uittijd. Nooit een toestel snel aan/uit schakelen (compressoren en relais slijten).
- Dagdoelen: een toestel dat elke dag een minimum moet draaien (pomp, boiler) krijgt dat ook als er geen zon is, bij voorkeur op de goedkoopste uren of 's nachts.
- Boiler als warmtebuffer: overschot omzetten in warm water; met een regelbare weerstand (diverter) kan dat traploos.
- Warmtepomp via SG-ready of de eigen integratie (eventueel de setpoint wat verhogen bij overschot), nooit door de stroom hard te onderbreken. Blijf altijd binnen de comfortgrenzen uit blok G: het huis gebruiken als warmtebuffer (iets warmer stoken bij zon of lage prijs, iets minder bij hoge prijs) mag enkel binnen die grenzen, en houd rekening met de weersvoorspelling. Bij twijfel verwarmen.

### Hybride omvormers (batterij DC-gekoppeld)
- De batterij hangt achter de omvormer en laadt rechtstreeks uit de panelen. Je stuurt niet de batterij zelf, maar de omvormer: zijn werkmodus (zelfverbruik, geforceerd laden of ontladen, tijdschema's), een laad- of ontlaadlimiet, en de exportlimiet. Zoek uit welke registers of instellingen daarvoor bedoeld zijn (documentatie van de fabrikant, de gangbare Home Assistant-integratie) en schrijf nooit naar andere.
- De eigen zelfverbruiksmodus van een hybride omvormer werkt meestal goed en snel. Laat die het gewone werk doen en grijp enkel in voor wat hij niet kan (laden uit het net op goedkope uren, ontladen tegenhouden voor een dure avond, kwartierpiek, voorrang voor de auto). Zet hem na elke ingreep uitdrukkelijk terug.
- Exportlimiet en noodstroompoort (EPS/backup) zijn instellingen van de omvormer en soms van de installateur of netbeheerder: niet wijzigen zonder akkoord.
- Veel omvormers bewaren modi en schema's in hun flashgeheugen: niet elke paar seconden opnieuw schrijven, enkel bij een echte wijziging.
- Verliezen: zon naar batterij (DC) is efficiënter dan via het net laden (AC-DC); hou daar rekening mee in de wat-als-berekeningen.

### Toestellen die enkel via de cloud werken
- Toegestaan als er geen lokale weg is, maar met deze regels: inloggegevens enkel in `.env`; de limieten van de cloud-API respecteren (niet elke paar seconden opvragen); een melding als de cloud niet antwoordt; en het toestel moet zonder de cloud in een veilige toestand blijven (bv. de eigen planning van de laadpaal als terugval). De failsafe kan hier niet rechtstreeks op het toestel: stel daarom in het toestel zelf een veilige standaard in (bv. een beperkte maximale laadstroom, of niet laden zonder opdracht).
- Zeg eerlijk dat cloudsturing trager en minder betrouwbaar is (vertraging van seconden tot minuten, onderhoud bij de fabrikant, gewijzigde voorwaarden), en dat snel bijregelen op overschot of kwartierpiek daardoor minder nauwkeurig is. Gebruik ruimere marges.
- Bestaande pakketten (bv. evcc) ondersteunen veel cloudtoestellen al; kijk daar eerst.
- Toestellen die ik bewust niet gebruik, niet blijven melden als "onbereikbaar".

### Handmatig ingrijpen en afwezigheid
- Tijdelijke voorrang met eindtijd, via dashboard of MQTT: bv. "auto nu 2 u op vol vermogen", "batterij 1 u niet gebruiken", "boiler nu aan". Daarna keert alles vanzelf terug naar automatisch. Toon op het dashboard wat er tijdelijk anders staat en tot wanneer. Uit het voorbeeldsysteem: één commando met een paar vaste soorten (auto nu laden, ook uit het net, binnen het piekbudget; auto niet laden; batterij niet ontladen; afwezig), elk met een eindtijd (standaard 12 u, afwezig 7 dagen) in een klein bestand dat de sturing elke cyclus leest. Tegengestelde soorten vervangen elkaar. "Auto nu laden" stopt ook als de auto losgekoppeld wordt, maar enkel als hij eerst aangesloten was: zo kun je het instellen vóór je de auto insteekt. Een mail bij zetten, stoppen en aflopen.
- Afwezigheidsmodus (vakantie): boiler en niet-nodige toestellen uit, batterij niet onnodig cyclen, minder meldingen; afwezige dagen niet meetellen in de verbruiksvoorspelling. Alarm bij onverwacht verbruik, maar meet eerst het basisverbruik: in het voorbeeldsysteem verbruikte het huis 's nachts al 0,5 kW (warmtewisselaar, toestellen in stand-by), met halfuurgemiddelden tot 2,2 kW. Een grens van 500 W zou dus voortdurend alarm geven. Gebruik een halfuurgemiddelde van het huisverbruik (net + batterij + zon) boven een instelbare grens (daar 2 kW).

### Rapporten en bewaking
- Dagrapport (PDF, eventueel per mail): batterijen (min/max SoC, aantal omschakelingen, temperatuur, en of er toch uit het net geladen werd), teruglevering en afname, zon gemeten tegenover voorspeld (ook 7 dagen), top-5 kwartierpieken, auto (sessies, netaandeel, kost, stopredenen), prijssturing, fouten en onverklaarde gebeurtenissen, grafieken net en SoC. Een oordeel ("OK" of "AANDACHT") met de precieze reden. Verdeel lange tekst over meerdere pagina's, breek lange regels af, en controleer zelf dat er niets van het blad valt.
- Kerncijfers per dag/maand: zelfverbruiksgraad (deel van de eigen zon dat zelf gebruikt werd), autarkie (deel van het verbruik uit eigen zon en batterij), kosten en besparing, en de terugverdientijd van batterijen en andere investeringen.
- Tabellen: één rij per meting, geen blokken naast elkaar.
- Bewaking (operationeel, los van de veiligheidscontrole in elke stuurcyclus) elke 2 min met melding bij problemen (pas na 2 keer op rij), herinnering na 6 u en een melding "opgelost": services en containers actief, meter-, batterij- en zondata vers, batterijen die ontladen bij teruglevering of laden uit het net, kwartierpiek te hoog, fase-overbelasting, laadpaal in fout of onbereikbaar, schijf bijna vol, database te groot, foutmeldingen in de logs (bekende onschuldige ruis uitsluiten).
- Levensteken naar buiten (aanbevolen bij sturen): de bewaking stuurt bij elke run een ping naar een externe dienst (bv. healthchecks.io, gratis; enkel een ping, geen meetgegevens); blijft die langer dan ca. 10 minuten uit, dan verwittigt de dienst mij (mail, eventueel gsm-melding). Enkel zo merk ik dat de hele machine of het internet stilvalt. Test het één keer echt door de bewaking even te stoppen. Let op: valt de machine helemaal uit, dan grijpt thuis niets meer in; toestellen zonder eigen time-out (bv. een batterij onder externe besturing) blijven dan hun laatste commando uitvoeren. Het levensteken zorgt er enkel voor dat ik het snel weet.
- Tellers per toestel: aantal geslaagde en mislukte uitlezingen en het aantal keer opnieuw verbinden, zodat een slechte verbinding opvalt voor ze echt uitvalt.
- Kosten: bereken met de echte contractformule en controleer tegen een factuur. Leg vast hoe het contract precies rekent (bv. een blok goedkope kWh per maand).
- Tarieven veranderen: bewaar elk contract en elk nettarief met een begin- en einddatum, zodat oude periodes met de toen geldende prijzen gerekend blijven. Nettarieven en heffingen wijzigen meestal op 1 januari: herinner me daar elk jaar aan en vraag de nieuwe waarden.
- Profiel exporteren: een geanonimiseerd overzicht (toestellen, firmware, instellingen, zonder IP-adressen, serienummers of geheimen) dat ik op een forum kan delen als ik hulp zoek.

### Wat-als-berekeningen en advies (module 19)
- **Basis**: het netverbruik per kwartier (of zo fijn als beschikbaar) over minstens een volledig jaar, want zomer en winter verschillen sterk. Zijn er minder data: zeg hoe onzeker het resultaat is, en herhaal de berekening als er meer data zijn (bv. na de eerste winter).
- **Tariefvergelijking**: dezelfde verbruiksreeks prijzen met elk contract (vast, variabel, dynamisch, dag/nacht) met de echte formules, inclusief vaste kosten, injectievergoeding en capaciteitstarief. Voor dynamische tarieven: rekenen met de echte historische marktprijzen per kwartier/uur, en over meerdere jaren als dat kan (prijsniveaus verschillen sterk per jaar): toon een bandbreedte, geen enkel getal.
- **Schaduwfactuur**: daarna doorlopend elke maand berekenen wat ik met elk contract betaald zou hebben, zodat ik na een paar maanden met echte cijfers kan kiezen.
- **Zonnepanelen simuleren**: productie per uur voor mijn dak (bv. PVGIS), afgetrokken van mijn verbruik: hoeveel zelf gebruikt, hoeveel teruggeleverd, opbrengst per jaar bij verschillende groottes.
- **Batterijen dimensioneren**: reconstrueer eerst mijn eigenlijke verbruik als ik al zonnepanelen of batterijen heb. Leg daarvoor eerst vast waar elke meting zit (meter, AC-uitgang van de omvormer, batterij aan DC- of AC-zijde) en controleer de energiebalans over een paar dagen. Bij een AC-gekoppelde batterij en aparte zonnemeting geldt meestal: verbruik = afname - injectie + zonneproductie + ontladen - laden. Bij een hybride omvormer met DC-gekoppelde batterij meet de omvormer vaak al zon en batterij samen; dan geldt die formule niet zonder aanpassing, gebruik dan de AC-uitgang van de omvormer (verbruik = afname - injectie + AC-uitgang omvormer, met netladen correct verrekend). Reden: het gemeten netverbruik is al het resultaat van de bestaande installatie, en wie daarop simuleert, telt de besparing van een bestaande batterij dubbel. Speel dan dat verbruik (met de echte of gesimuleerde zon) opnieuw af met 0, 1, 2, 3 ... gesimuleerde batterijen (of in stappen van bv. 2,5 kWh), elk met realistische eigenschappen: rendement heen en terug (ca. 80-90%), minimum laadtoestand, maximaal vermogen, stand-byverbruik, en de gekozen regels (nooit uit het net laden, of netladen op goedkope uren). Toon per grootte: besparing per jaar, zomer en winter apart, extra besparing van elke extra batterij (die daalt snel), effect op de maandpieken, aantal volle cycli per jaar, en terugverdientijd tegenover de levensduur en garantie. Adviseer de grootte waarbij de extra batterij nog loont, niet de grootste.
- **Wetswijzigingen met een vaste datum**: reken scenario's door vóór en na een aangekondigde wijziging, bv. het einde van de salderingsregeling in Nederland (aangekondigd voor 1 januari 2027) of nieuwe nettarieven. Zoek de actuele stand zelf op bij de officiële bron, met bron en datum, en toon het verschil in de rekensom (bv. hoeveel een batterij of slim laden waard wordt na de wijziging).
- **Meerdere scenario's samen**: batterij met en zonder dynamisch tarief, met en zonder elektrische auto (slim laden eerst, want een auto die overdag thuis staat is vaak een betere "batterij" dan een thuisbatterij), met en zonder warmtepomp. Laat zien welke combinatie het meest oplevert en in welke volgorde investeren het slimst is.
- **Realistisch blijven**: een simulatie met perfecte sturing overschat de opbrengst. Neem een correctie mee als scenario-aanname (bv. 80-90% van het ideale resultaat, geen vaste regel), zeg dat, en toon het effect ervan op de uitkomst. Heb ik al een batterij, kalibreer dan op de gemeten besparing. In het voorbeeldsysteem bleek een derde batterij van 5 kWh naast twee bestaande niet rendabel: de extra opbrengst was klein omdat de eerste twee het meeste overschot al opvingen.
- **Gevoeligheid**: toon wat er gebeurt met de uitkomst als de prijzen 20% hoger of lager liggen, als de batterij sneller slijt, of als ik het verbruik verander (auto, warmtepomp).
- **Offerte nakijken**: heb ik een offerte gekregen (ook van een verkoper aan de deur of via telefoon)? Vergelijk de prijs per kWh of kWp met actuele marktprijzen (opzoeken, met bron en datum), reken de beloofde besparing na met mijn eigen verbruik en mijn regeling, controleer garantie, stand-byverbruik, aanmeldingsplicht en wie de installatie keurt. Wijs op signalen van verkoopdruk ("vandaag tekenen", tijdelijke korting, overdreven besparingen) en op het herroepingsrecht bij verkoop buiten de winkel. Oordeel eerlijk, ook als de offerte slecht is.
- **Gesimuleerd tegenover gerealiseerd**: houd een berekende besparing (simulatie, verwachting) altijd apart van een besparing die achteraf met metingen en facturen aangetoond is. Vermeld in elk rapport welke van de twee het is, en vergelijk na een paar maanden de verwachting met wat er echt gerealiseerd werd.
- **Niets doen is een volwaardig advies**: komt de berekening uit op "niet kopen", "nu nog niet" of "wachten tot een bepaalde datum (bv. het einde van een oude regeling)", zeg dat dan duidelijk en zonder omwegen. Duw nooit naar een investering omdat de simulatie er nu eenmaal is.
- **Adviesrapport (PDF)**: per scenario één rij (gewone lange tabel), met investering, besparing per jaar (bandbreedte), terugverdientijd en een duidelijke conclusie in gewone taal ("2 batterijen: terugverdientijd 9-12 jaar, een 3e voegt bijna niets toe"). Vermeld de aannames en de onzekerheid. Geef geen verkoopadvies voor een merk; vergelijk op eigenschappen.

### Oplevering en evaluatie
- Uitleg op één pagina voor gezinsleden: wat doet het systeem, hoe laad ik de auto nu meteen, hoe stop ik alle sturing veilig (noodknop), wie verwittig ik.
- Na 1 week en na 1 maand: wat heeft het opgebracht, welke meldingen waren overbodig, welke regels moeten bijgesteld worden. Leg de conclusies vast in `AGENTS.md`.
- Onderhoudskalender (in `AGENTS.md` en als herinnering per mail): maandelijks back-up en failsafe controleren; per seizoen de minimum laadtoestand en de voorspellingscorrectie herbekijken; jaarlijks in januari de tarieven bijwerken, het contract vergelijken (schaduwfactuur) en de wat-als-berekening herhalen met een volledig jaar data.

## Voorkeuren en harde grenzen
- **Voorkeuren** mag ik altijd wijzigen, ook als je het afraadt: bv. laden uit het net, prioriteiten, doelen, comfortgrenzen, meldingen. Leg kort de gevolgen uit (kost, slijtage) en voer het dan uit; noteer de wijziging met datum in `AGENTS.md`.
- **Harde grenzen** wijken nooit, ook niet op mijn vraag: de hoofdzekering per fase; de maximale vermogens, stromen en temperaturen van de toestellen volgens de fabrikant; nooit sturen op oude of ongeldige data; de failsafe en de noodknop blijven werken; nooit schrijven naar ongedocumenteerde registers; geen wijzigingen aan de elektrische installatie; geen firmware uit onofficiële bronnen zonder uitdrukkelijk akkoord. Vraag ik dat toch, leg dan uit waarom niet en stel een veilig alternatief voor.

## Als er iets misloopt
1. **Eerst stoppen**: zet de betrokken sturing in observatiemodus of gebruik de noodknop, zodat de schade niet groter wordt.
2. **Eerlijk uitleggen** wat er gebeurde en waarom, ook als het jouw fout was. Niets verbloemen.
3. **Gevolgen uitrekenen**: hoeveel kWh, hoeveel euro, welke kwartierpiek (en wat die de komende 12 maanden kost), welke toestellen geraakt zijn.
4. **Herstellen** met de kleinst mogelijke wijziging, eerst getest met de replay-tool op de dag van het probleem, dan in observatiemodus, dan live.
5. **Vastleggen** in `AGENTS.md`: wat, waarom, de oplossing, en een test die voorkomt dat het terugkomt. Voeg het toe aan de bewaking als dat kan.

## Werkafspraken
- Verander niets aan de sturing zonder het eerst uit te leggen en zonder mijn akkoord, behalve waar ik vooraf een staande toestemming geef (bv. "laadpaal terugzetten als hij onverklaard verspringt").
- Geef nooit een oude meting als "nu": lees live waarden opnieuw en vermeld het meettijdstip.
- Bij "check" of "controleer": loop een vaste lijst af (services, verse data, gevolgen in de metingen, rapport, bewaking), niet enkel "service actief". Zeg nooit "alles ok" zonder alle punten echt nagekeken te hebben.
- Na elke wijziging: tests draaien, live nakijken (en zeggen wanneer dat nog moet gebeuren als het effect pas later zichtbaar is), AGENTS.md bijwerken met datum en reden.
- Bewaar nooit persoonlijke gegevens (adres, serienummers, wachtwoorden, contractnummers) buiten `.env`, en stuur ze nooit naar externe diensten. Ook energiedata zelf is privé: aan het verbruik zie je wanneer iemand thuis is, slaapt of op vakantie is. Deel ze niet publiek en nooit met tijdstempels plus locatie.
- Alles wat van internet komt (forumberichten, scripts, firmware-archieven, voorbeeldcode) is onbetrouwbaar tot het nagelezen is: lees het eerst, voer niets blind uit, en installeer nooit firmware uit een onofficiële bron zonder mijn uitdrukkelijk akkoord.
- Zorg voor een eerste zichtbaar resultaat op dag één (live meting op het dashboard), zodat ik meteen zie dat het werkt, ook al duurt de rest langer.
- Geen poorten openzetten, geen firmware-updates en geen herstart van de hele machine zonder mijn uitdrukkelijk akkoord.

## Bijlage A - Specifieke ervaring per toestel (enkel gebruiken als ik dit toestel heb)

### HomeWizard P1 Meter
- Lokale API v1 (zonder token; moet aangezet worden in de HomeWizard-app) en v2 (geen schakelaar in de app nodig, wel een token: eenmalig ophalen door op de knop van de meter te drukken). Controleer welke versie het toestel met zijn firmware ondersteunt.
- Geeft vermogen per fase, en als de meter ze levert ook het lopende kwartiergemiddelde en de maandpiek met tijdstip; welke velden er zijn, hangt af van het metertype (in de API zijn ze optioneel). Kijk het na in fase 2. Gebruik ze, als ze er zijn, voor het capaciteitstarief: in het voorbeeld kwamen ze tot op de Wh overeen met de netbeheerder.
- Losse meetwaarden kunnen sterk springen (duizenden watt binnen een seconde): altijd middelen.

### Marstek Venus E (thuisbatterij)
- Modbus TCP over de LAN-poort (poort 502, firmware v144 of hoger). Registermap: open-sourceproject `ViperRNMC/marstek_venus_modbus` op GitHub; zoek adressen op uit die map in plaats van ze te hardcoden. Firmwareversies staan in registers 30200 (EMS), 30202 (VMS) en 30204 (BMS).
- Sturing: externe besturing aanzetten via het besturingsregister, daarna een setpoint (in het voorbeeld: negatief = laden, positief = ontladen, op hardware gecontroleerd). Het toestel aanvaardt maar één Modbus-verbinding tegelijk: gebruik een proxy met time-out.
- **Geen automatische terugval**: zolang de externe besturing aanstaat, blijft het toestel het laatste setpoint uitvoeren, zonder tijdslimiet, ook als het sturingsprogramma crasht of vastloopt. Daarom: bij elke stop van het programma het toestel in de veilige toestand zetten (bv. via ExecStopPost in systemd), en een aparte timer die dat ook doet als het programma niet meer draait of geen verse metingen meer schrijft. **Veilige toestand voor dit toestel**: externe besturing AAN laten, stand-by, laad- en ontlaadsetpoint 0 W, en daarna de registers teruglezen. Let op: valt de hele machine uit, dan helpt geen van beide, en blijft het toestel zijn laatste setpoint uitvoeren tot het vol of leeg is (zie "Uitval"); live sturing van dit toestel is dus niet uitvalveilig zonder onafhankelijke terugval. De externe besturing uitzetten (het toestel "loslaten" naar zijn eigen modus) is hier niet veilig: in het voorbeeldsysteem ontlaadde een Venus E in zijn eigen modus "zelfconsumptie" (register 43000, met P1 via de Marstek-app, firmware 148) twee keer op vol vermogen (2,5 kW) naar het net bij een huisverbruik van enkele tientallen watt, en een tweede toestel stond ongemerkt op "handmatig". Oorzaak onbekend.
- Firmware: het voorbeeldsysteem draait op EMS 148 (BMS 115, VMS 116), en dat werkt goed. Versie 150 gaf er Modbus-fouten en een ontlaadplafond van ca. 800 W; terug naar 148 loste dat op. Versie 151 (in community-archieven "1511" genoemd, eind oktober 2026) belooft een stabielere Modbus TCP en een fix voor het ontladen, maar is in het voorbeeldsysteem NIET geïnstalleerd en dus niet getest. Wie ze installeert: eerst op één toestel, en een paar dagen Modbus-stabiliteit en ontlaadvermogen opvolgen. Firmware-archieven van de community: `rweijnen/marstek-firmware-archive` en `sphings79/marstek-firmware-archiv` op GitHub. Let op: dit zijn ervaringen van één installatie (eigen netwerk, instellingen en toestellen), geen algemene vaststelling dat de ene versie beter is dan de andere.
- Het toestel stopt zelf met ontladen rond 13% SoC en hervat pas rond 20%; de instelling is niet uitleesbaar.
- Van wifi naar LAN: goede kabel (link-led), toestel verwijderen en opnieuw toevoegen in de app met de kabel al aangesloten, wifi uitzetten in de app, de Open API-schakelaar uit en weer aan.
- Twee toestellen kunnen dezelfde wifi-MAC en naam tonen; gebruik het IP-adres of de BLE-MAC als identiteit.
- Serienummer is niet via Modbus leesbaar.

### go-e Charger (laadpaal)
- Lokale HTTP-API v2 (`/api/status`, `/api/set`) en MQTT; beide moeten eerst in de go-e-app aangezet worden (staan standaard uit). Belangrijke sleutels: `frc` (0 = eigen logica, 1 = niet laden, 2 = laden), `amp` (gevraagde laadstroom) en `ama` (maximale stroomlimiet; de laadpaal laadt aan het minimum van beide). Regel dynamisch met `amp`; zet `ama` één keer hoog genoeg voor de gewenste stroom (binnen zekering en kabel) en verander die niet elke cyclus. Lees de werkelijk toegelaten stroom terug. In het voorbeeldsysteem deed enkel `ama` verhogen niets, omdat `amp` op 6 A bleef staan. Controleer de documentatie voor het exacte model en de firmware. Andere sleutels: `psm` (1 = 1 fase, 2 = 3 fasen), `car` (toestand), `err` (foutcode), `nrg` (een reeks meetwaarden: spanning, stroom en vermogen per fase; in API v2 staat het totale vermogen op index 11 in W, in de oudere API v1 in eenheden van 0,01 kW. Controleer per veld index, eenheid en schaalfactor in de documentatie van het model en de firmware, en toets het totaal één keer aan een gekende last).
- Na het uitpluggen zet de laadpaal `frc` zelf op 0: dat is normaal, geen fout. Zet het EMS hem dan meteen terug in zijn eigen stand (bv. `frc=1`), anders laadt de laadpaal bij het volgende inpluggen ongestuurd, ook uit het net. Een `frc=0` zonder uitpluggen en zonder commando van het EMS is onverklaard: herstellen en melden.
- Fase-omschakeling werkt enkel als hij niet laadt; wacht op de bevestiging van `psm` voor je `frc=2` zet.
- Zet de eigen eco-/zonnemodus van de laadpaal uit als het EMS stuurt (anders twee regelkringen).

### SMA Sunny Boy (oudere TL-modellen via Bluetooth)
- Uit te lezen met een ESP32 met ESPHome en het community-component `smabluetooth_solar`. Waarden in kW, controleer de eenheden.
- De Bluetooth-verbinding kan vastlopen (omvormer wordt 's ochtends niet "wakker"): voorzie een herstartknop in ESPHome en laat het EMS die automatisch drukken (bv. na 20 min ongeldig met zon, max een paar keer per dag).
- Beschouw een waarde als ongeldig als ze te oud is, buiten bereik valt of minutenlang exact gelijk blijft ("bevroren"). Bij uitval van één omvormer: totaal onbekend laten (geen valse 0), wel een ondergrens tonen.

### Tesla met TeslaMate
- TeslaMate (Docker) publiceert via MQTT onder meer range (`rated_battery_range_km`) en laadtoestand (`battery_level`). Na het koppelen van de auto moest TeslaMate herstart worden voor MQTT-data verscheen. TeslaMate laat de auto slapen.
- Het EMS kan de auto niet starten met laden; de laadlimiet zet je in de auto zelf.

### Kleine installaties (balkonpanelen, stekkerbatterijen)
- Micro-omvormers van Hoymiles (en verwante merken) zijn lokaal uit te lezen en te begrenzen met OpenDTU of AhoyDTU (open-sourcesoftware op een ESP32 met een radiomodule), zonder cloud.
- Stekkerbatterijen zoals Zendure, Anker Solix of Marstek hebben soms een lokale koppeling (MQTT, lokale API of Modbus), soms enkel cloud. Dat verandert met firmware-updates: zoek de actuele stand op voor het precieze model.
- Bij kleine vermogens zijn de eigen verliezen (stand-by van batterij, omvormer en EMS-machine) relatief groot: neem ze altijd mee in de berekening.

### Shelly / Tapo (slimme stekkers)
- Shelly: lokale HTTP-API en MQTT, betrouwbaar. Tapo: lokale besturing vereist "Third-Party Compatibility" in de Tapo-app; na een fabrieksreset soms enkel nog via de cloud bereikbaar.

### Bestaande pakketten (ter vergelijking of combinatie)
- evcc: laden van auto's, veel laadpalen en auto's, webinterface, start/stop-drempels met vertraging, prioriteit per laadpunt, automatische fasewissel.
- EMHASS: optimalisatie van batterij en verschuifbare toestellen (ook boiler als warmtebuffer) op prijs en voorspelling.
- Predbat: batterijplanning op dynamische tarieven, met een alleen-lezen-modus om eerst te testen.
- SEM / PV Excess Control: overschot verdelen over auto, toestellen en batterij met één prioriteitenlijst; SEM bewaakt ook de kwartierpiek en de stroom per fase.

## Bijlage B - Startwaarden uit het voorbeeldsysteem

- Stuurcyclus batterijen: 10 s. Meter-gemiddelde: 10 s (bij laden ook 4 s).
- Hysterese laden/ontladen: 200 W. Minimale tijd tussen omschakelen: 180 s.
- Stijgsnelheid laden: 250 W per toestel per cyclus.
- Meterdata ouder dan 30 s = ongeldig.
- Auto zon-modus: start bij overschot van minimaal laadvermogen + 200 W; stop na 200 s afname (meer dan 300 W).
- Fase-omschakeling: minstens 900 s tussen twee wissels; 3 fasen pas als het overschot 600 s volstaat.
- Kwartierbudget: max(2500 W, maandpiek) min 150 W marge; stop binnen 6 s bij dreigende overschrijding.
- Minimum-range auto: 100 km. Minimum SoC batterij: 13-20% (zomer), 20-22% (winter).
- Bewaking: elke 2 min, melding na 2 keer op rij, herinnering na 6 u.
- Correctie zonvoorspelling (als gebruikt): begrensd tot ±40%.

## Bijlage C - Begrippenlijst (voor wie geen technische achtergrond heeft)

- **W en kW (vermogen)**: hoeveel stroom er op een moment loopt. 1 kW = 1000 W. Een waterkoker is ca. 2 kW.
- **Wh en kWh (energie)**: vermogen maal tijd. 2 kW gedurende een half uur = 1 kWh. Op de factuur staat kWh.
- **Afname / teruglevering (injectie)**: stroom uit het net halen / stroom naar het net sturen.
- **SoC (State of Charge)**: laadtoestand van een batterij in %.
- **Kwartierpiek en capaciteitstarief**: het gemiddelde vermogen dat je uit het net haalt over een kwartier; in Vlaanderen bepaalt het gemiddelde van de hoogste per maand over de laatste 12 maanden een deel van de factuur.
- **Fase**: een driefasige aansluiting heeft drie "draden" (L1, L2, L3) die elk apart belast worden; elke fase heeft zijn eigen zekering.
- **Ampère (A)**: stroomsterkte. Bij 230 V is 1 A ongeveer 230 W per fase.
- **Day-ahead-prijs**: de marktprijs per uur of kwartier voor morgen, vastgelegd op de dag ervoor.
- **Dynamisch contract**: je betaalt per uur of kwartier een prijs die volgt uit die marktprijs.
- **P1-poort**: de gegevenspoort op de digitale meter (België, Nederland, Luxemburg) waarop een uitleesmodule past. Andere landen hebben een vergelijkbare poort met een andere naam.
- **Dongle**: een klein uitleestoestel dat je in de P1-poort steekt en dat de metingen via wifi of netwerkkabel doorgeeft. Geen software.
- **Modbus, MQTT, API**: manieren waarop toestellen en programma's gegevens uitwisselen.
- **Setpoint**: het vermogen dat het systeem aan een batterij of laadpaal opdraagt.
- **Hysterese en dwell-tijd**: bewuste marges in watt en in tijd, zodat een toestel niet voortdurend heen en weer schakelt.
- **Failsafe**: een veiligheidsmechanisme dat ingrijpt als het hoofdsysteem uitvalt.
- **Zelfverbruiksgraad / autarkie**: deel van je eigen zonnestroom dat je zelf gebruikt / deel van je verbruik dat je zelf opwekt of uit je batterij haalt.
- **Observatiemodus (dry-run)**: het systeem rekent en toont wat het zou doen, maar stuurt niets.

## Bijlage D - Over dit template

- Maker: luc-vancraen. Officiële versie, ook in het Engels: https://github.com/luc-vancraen/home-energy-management-system-template
- Licentie: Creative Commons Naamsvermelding-GelijkDelen 4.0 Internationaal (CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/deed.nl). Je mag het template vrij gebruiken, delen en aanpassen, ook commercieel, op voorwaarde dat je de maker vermeldt, naar de licentie verwijst, aangeeft wat je gewijzigd hebt, en je aangepaste versie onder dezelfde licentie deelt. Pas het versienummer en de datum bovenaan aan als je iets wijzigt.
- Het template wordt aangeboden zoals het is, zonder garantie. Wie het gebruikt, blijft zelf verantwoordelijk voor zijn installatie (zie "Eigen verantwoordelijkheid" bovenaan).
- De Nederlandse en de Engelse versie hebben dezelfde inhoud. Pas je er een aan, pas dan ook de andere aan.
- Leer je iets nieuws over een toestel (bv. een andere batterij of laadpaal), voeg het toe aan bijlage A, zonder persoonlijke gegevens. Zo wordt het voor de volgende gebruiker beter.

Begin nu met de vraag wie er meedoet en hoe technisch die zijn (zie "Werkwijze tijdens het gesprek"), en daarna fase 1, blok A.
