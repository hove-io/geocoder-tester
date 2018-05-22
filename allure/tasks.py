from datetime import datetime
import invoke
from invoke import task
from os import path

@task
def generate_report(ctx, results_dir):
    print('Generating Allure report...')
    with ctx.cd('allure'):
        if path.exists(f'{ctx.cwd}/allure-report/history'):
            ctx.run(f'mv allure-report/history {results_dir}')
        ctx.run(f'allure generate {results_dir} --clean')


@task(default=True)
def run_tests(ctx):
    dt_now = datetime.utcnow().isoformat()[:19]
    results_dir = f'res_{dt_now}'

    ctx.run(
        f'pytest {ctx.tests_files} --api-url {ctx.api_url} '
        f'--loose-compare --tb=short --alluredir allure/{results_dir}',
        warn=True
    )

    generate_report(ctx, results_dir)
