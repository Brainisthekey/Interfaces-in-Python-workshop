from behave import fixture, use_fixture
from splinter import Browser
from consts import CI_RUN
from page_objects.environment_base import EnvironmentMailObject


@fixture
def selenium_browser_chrome(context):
    # -- HINT: @behave.fixture is similar to @contextlib.contextmanager
    context.browser = Browser("chrome")
    yield context.browser
    # -- CLEANUP-FIXTURE PART:
    context.browser.quit()


def before_all(context):
    use_fixture(selenium_browser_chrome, context)

    context.form_data = {}

    # Page objects
    context.pages = lambda x: None
    context.pages.environment_base = EnvironmentMailObject()


# -- FILE: features/environment.py
def after_step(context, _step):
    if _step.status == "failed":
        if CI_RUN:
            filename = f"/tmp/artifacts/{_step.filename.replace('/', '_')}"
            context.browser.html_snapshot(filename)
            context.browser.screenshot(filename)
        else:
            import sys, pdb
            pdb.Pdb(stdout=sys.__stdout__).set_trace()


def after_scenario(context, scenario):
    context.browser.cookies.delete()
