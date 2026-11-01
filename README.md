# PropertyInspector

Maestro framework for the PropertyInspector staging app (`com.ticpropertyinspector.app.staging`).

A journey file only lists the screens, in order. Each screen lives in its own file under `shared/`. Test data for a journey stays at the top of that journey. That split is what keeps a new case from turning into one long script.

## What runs

| Run | What it covers |
| --- | --- |
| Smoke | Launches the staging app and saves a screenshot |
| Notes | Opens a case, creates a note, syncs it to legacy, reopens the case, and finds the note |
| Files | Opens a case and enters the files area |

Smoke is the default run. Notes and files are tagged `draft` until the screen steps are in the matching `shared/` file, so a suite run does not pretend those screens are done.

## Layout

```
.maestro/config.yaml                     app id, which folders run, report folder
.maestro/smoke/AppLaunch.yaml            launch smoke
.maestro/e2e/notes/note_e2e.yaml         notes journey and its test data
.maestro/e2e/files/files_e2e.yaml        files journey and its test data
.maestro/shared/app/launch_app.yaml      launch steps, reused by every journey
.maestro/shared/case/                    open and reopen a case
.maestro/shared/notes/                   open the notes list, create a note
.maestro/shared/files/open_files.yaml    open the files area
.maestro/shared/sync/sync_to_legacy.yaml sync the case to legacy
.maestro/shared/helpers/scroll_until.yaml scroll until a label is visible
tools/                                   install the apk and start a run
```

Reports are written to `reports/`.

## Notes journey

The staging case and the note text live in `.maestro/e2e/notes/note_e2e.yaml`:

- Address: Rougsøvej 2, 8940 Randers SV
- Calendar day: 11
- App version: v1.1.3
- Note: "Note Create" / "new note", then "Note Updated" / "updated note"

The journey itself is the list of shared flows: launch, open case, open notes, create note, sync to legacy, reopen case, open notes, scroll to the note title.

## Run

Install Maestro from https://docs.maestro.dev/getting-started/installing-maestro and install the staging build on the device or emulator.

```bat
tools\install-app.bat path\to\staging.apk
tools\run-tests.bat
tools\run-smoke.bat
tools\run-e2e.bat
```

The same smoke command from a shell:

```bash
maestro test .maestro
maestro test .maestro/smoke/AppLaunch.yaml
```

## Add a screen

1. Add the steps in the shared file for that screen, for example `.maestro/shared/notes/create_note.yaml`.
2. Read inputs from the journey `env` block (`NOTE_TITLE`, `PROPERTY_ADDRESS`, and the rest). Do not copy the address or the note text into the screen file.
3. Remove the `draft` tag from the journey once every screen it calls has real steps.

## Add a journey

1. Create a file under `.maestro/e2e/<feature>/`.
2. Put the test data in that file's `env` block.
3. Call shared flows with `runFlow`. Pass a one-off value, such as the scroll target, on that call.
4. Tag it `e2e`. Add `draft` until its screen files are filled in.
