# miniTopSim
Project of the Seminar "Scientific Programming in Python" at TU Wien, WS 2020/21.

--------------------
1. Code-Organisation
--------------------

Die Verzeichnisstruktur des Projekts:

```
miniTopSim/
    mini_topsim/                # Das Code-Verzeichnis
        __init__.py             # macht aus mini_topsim ein Package
        main.py                 # Main Script und Top-Level-Funktion
        parameters.py           # Modul, das die Parameter als Attribute hat
        ...                     # weitere Module
        parameters.db           # Parameterdatenbank
        tables/                 # Verzeichnis für Tabellen
            ...                 # Tabellen
    work/                       # Verzeichnis für Arbeitsverzeichnisse
        Aufgabe1_basic          # Arbeitsverzeichnis für Aufgabe 1
        Aufgabe2_param          # Arbeitsverzeichnis für Aufgabe 2
        ...                     # Arbeitsverzeichnisse für die weiteren Aufgaben
        templates/              # Verzeichnis für Templates (nicht ändern!)
            run.py              # Skript zum Laufenlassen von miniTopSim
            test_run.py         # Testmodul
```

Damit die Imports funktionieren, müssen Sie das Package lokal installieren. Wechseln Sie in das Überverzeichnis des Projektverzeichnisses (`miniTopSim`) und geben Sie ein:

```bash
pip install -e ./miniTopSim/
```

Es kann auch sein, dass Sie `pip3` statt `pip` sagen müssen, oder dass Sie `pip` erst installieren müssen. Falls Sie mit `pip` nicht erfolgreich sind, ist ein Workaround, das Code-Verzeichnis in `sys.path` aufzunehmen:

```
    import os, sys
    filedir = os.path.dirname(__file__)
    codedir = os.path.join(filedir, '..', ’..’, ’mini_topsim’)
    sys.path.insert(0, codedir)
```

------------------------
2. Aufruf von miniTopSim
------------------------

Rufen Sie miniTopSim immer aus "Ihrem" Arbeitsverzeichnis aus auf (`AufgabeX_xxxx`). Ab der zweiten Stunde soll der Aufruf mit

```bash
python3 run.py beispiel.cfg
```

erfolgen. In `run.py` erfolgen die Imports nach dem Muster von `work/templates/run.py`. Da für alle Aufgaben ein `run.py`-File geschrieben werden muss, wird dieses in den einzelnen Aufgabestellungen nicht extra erwähnt.

`beispiel.cfg` (kann auch anders heißen, siehe Aufgabenstellung, jedenfalls aber mit Endung `.cfg`) ist das Konfigurationsfile (cfg-File), das wie folgt aussieht:

```
[SectionName1]
ParameterName1 = Wert1
ParameterName2 = Wert2
...
[SectionName2]
ParameterNameN+1 = WertN+1
ParameterNameN+2 = WertN+2
...
```

`ParameterName*` sind durch die Namen der Parameter zu ersetzen, `Wert*` durch die Parameterwerte. Die Parameter sind in Gruppen („Sections”) eingeteilt. 

Welche Parameter in welchen Sections einzuführen sind, ist in den einzelnen Aufgaben angegeben. "Einführen" heißt für Sie, dass Sie einen Eintrag in der Parameter-Datenbank (`parameters.db` Datei im Code-Verzeichnis) vornehmen. Die Parameter-Datenbank ist ein Textfile in folgendem Format:

```
[SectionName1]
ParameterName1 = (DefaultWert1, 'Bedingung1', '''Erklärung1''')
ParameterName2 = (DefaultWert2, 'Bedingung2', '''Erklärung2''')
...
[SectionName2]
ParameterNameN+1 = (DefaultWertN+1, 'BedingungN+1', '''ErklärungN+1''')
ParameterNameN+2 = (DefaultWertN+2, 'BedingungN+2', '''ErklärungN+2''')
...
```

Für jeden Parameter sind in einem Tupel der Defaultwert, eine Bedingung und eine Erklärung angegeben. Statt des Defaultwerts kann auch ein Datentyp angegeben sein, dann ist der Parameter obligatorisch mit diesem Datentyp im cfg-File anzugeben. Die Bedingung kann auch None sein, dann wird keine Bedingung überprüft. Ansonsten ist die Bedingung ein gültiger boolscher Python-Ausdruck, in einem String gespeichert. Er kann denselben oder andere Parameternamen (in Großbuchstaben) als Variablen enthalten. Die Erklärung ist ein String, der (bei Verwendung von Triple-Quotes) auch über mehrere Zeilen laufen kann. Wann immer ein neuer Parameter eingeführt wird, muss also auch ein Eintrag in der Parameter-Datenbank erfolgen.

Im Programm werden die Parameter über das `parameters` Modul (Datei `parameters.py`) zur Verfügung gestellt. Dieses wird von den anderen `mini_topsim`-Modulen aus mit

```
from . import parameters as par
```

importiert. Die Parameter stehen dann als Modulvariablen des parameters Moduls zur Verfügung, d.h. sie können unter den Namen `par.ParameterName*` (`ParameterName*` entsprechend dem Parameternamen ersetzen) referenziert werde. Von außerhalb des Code-Verzeichnisses, also insbesondere von Ihrem Arbeitsverzeichnis aus, lautet der Import

```
import mini_topsim.parameters as par
```

---------
3. Testen
---------

Ab der zweiten Stunde sind in den Aufgaben automatisierte Tests durchzuführen. Hierfür verwenden wir Pytest. Nachdem Sie Test-Code geschrieben haben, rufen Sie `pytest` (manchmal auch `pytest3` oder `pytest-3`) in Ihrem Arbeitsverzeichnis auf, dann werden Ihre Tests ausgeführt. Wollen Sie die Tests der anderen Aufgaben auch ausführen (das sollten Sie zumindest tun, bevor Sie mit Ihrer Aufgabe beginnen und bevor Sie diese abgeben), dann starten Sie `pytest` aus `work`. Für das Importieren von Modulen gilt dasselbe wie für das `run.py` Skript.

Tests müssen ein assert Statement enthalten (siehe Vortragsfolien)!

Wenn nichts anderes angegeben ist, besteht ein Test aus einer Simulation, die ein `srf`-File erzeugt. Die letzte Oberfläche soll auf "geringen Abstand" von der letzten Oberfläche des entsprechenden `srf_save`-Files überprüft werden. Letzteres wird durch Kopieren des `srf`-Files einer vorangegangenen Simulation auf ein File mit Endung `.srf_save` erzeugt. Die in den Angaben verlangten Tests stellen ein Minimum dar. Sie können auch weitere Tests definieren. Achten Sie aber darauf, dass diese möglichst nicht zu lange laufen.

-------------------
4. Arbeiten mit git
-------------------

- Sie können den Code jederzeit herunterladen (fetch bzw. pull). Erzeugen Sie einen Branch, auf dem Sie arbeiten. Wählen Sie den Branchnamen ident mit Ihrem Arbeitsverzeichnis (`Aufgabe1_basic` etc.). **Uploaden (pushen) Sie Ihren Branch spätestens um 8:00 am Tag Ihrer Präsentation. Laden Sie zusätzlich die "Abzugebenden Files" bis zu dieser Deadline auf TUWEL hoch.** Führen Sie nach der Präsentation und nach eventuellen Nachbesserungen Ihren Branch mit dem `master` Branch zusammen (merge) und **pushen Sie beide Branches bis spätestens eine Woche nach Ihrer Präsentation**.

- Grundsätzlich nur getesteten, voll funktionsfähigen Code uploaden, insbesondere am `master` Branch. Lokal in Ihrem Branch ist es hingegen ratsam, viele Commits zu machen.

- `png`- und `srf`-Files werden nicht versioniert, d.h. sie werden nicht ins Repository übertragen. Damit von Ihnen generierte `srf`-Files für Vergleichszwecke erhalten bleiben, kopieren Sie sie auf Files mit gleichem Namen aber Endung `.srf_save`, wenn Sie sicher sind, dass sich nichts mehr ändert.

**Lesen Sie sorgfältig die Folien "Working with GitHub" aus dem einleitenden Vortrag.**


----------------------------
5. Hinweise zur Präsentation
----------------------------

Sie sollen Ihre Arbeit in einem ca. 10-15-minütigen Vortrag präsentieren. Halten Sie den Vortrag in erster Linie für Ihre Kollegen und berücksichtigen Sie deren Wissensstand. Ihr Vortrag soll die Aufgabenstellung darlegen, den Code präsentieren und die Ergebnisse der Tests und/oder Simulationen beschreiben. Sie können dazu mehrere Hilfsmittel verwenden, Powerpoint-Präsentation, Spyder/PyCharm/Editor. Kurze Rechnungen können Sie online laufen lassen, bei längeren wird es angebracht sein, die Ergebnisse vorzubereiten.

Damit Ihr Code "präsentierbar" ist, schreiben Sie möglichst übersichtlichen Code und beachten Sie den "Style Guide for Python Code" (http://www.python.org/dev/peps/pep-0008/) und die "Docstring Conventions" (http://www.python.org/dev/peps/pep-0257/).

