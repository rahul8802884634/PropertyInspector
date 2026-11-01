# PropertyInspector

Appium framework for the PropertyInspector Android app. The only flow included so far is app launch. New screens can follow the same split: page, flow, test.

## Layout

```
config/config.yaml                 app id, activity, Appium server, launch timeout
framework/core/config_reader.py    loads config.yaml, environment overrides
framework/core/driver_factory.py   starts the Appium session
framework/core/wait.py             shared polling
framework/pages/base_page.py       find() used by every screen
framework/pages/launch_page.py     foreground package and optional ready element
framework/flows/app_launch_flow.py launch steps and LaunchResult
tests/test_app_launch.py           launch checks, plus one real-device test
```

A test should call a flow. A flow should call pages. Pages talk to the driver. Keep locators and taps out of the test file so the next script drops into the same shape.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Edit `config/config.yaml` and set `app_package` and `app_activity` to the real app. `app_path` is optional; leave it empty when the app is already installed.

Environment variables override the yaml file: `APPIUM_SERVER_URL`, `ANDROID_DEVICE_NAME`, `APP_PACKAGE`, `APP_ACTIVITY`, `APP_PATH`, `NO_RESET`, `LAUNCH_TIMEOUT_SECONDS`, `LAUNCH_READY_ACCESSIBILITY_ID`.

## Run

Structure checks (no device):

```bash
pytest
```

Launch on a device or emulator. Appium must already be running and the package in config must be installed (or `app_path` must point at an apk).

```bash
pytest -m device
```

`LAUNCH_READY_ACCESSIBILITY_ID` is optional. When it is set, launch waits until that accessibility id is on screen after the package is in the foreground.

## Adding the next flow

1. Add a page under `framework/pages/` and subclass `BasePage`.
2. Add a flow under `framework/flows/` that calls that page and returns a small result object.
3. Add a test under `tests/` that calls the flow.
4. Put any new app id, timeout, or locator value in `config/config.yaml`.
