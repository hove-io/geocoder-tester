from datetime import datetime
import invoke
from invoke import task
from os import path

@task
def generate_report(ctx, results_dir):
    print('Generating Allure report...')
    with ctx.cd('allure'):
        if path.exists('{}/allure-report/history'.format(ctx.cwd)):
            ctx.run('mv allure-report/history {}'.format(results_dir))
        ctx.run('allure generate {} --clean'.format(results_dir))


@task(default=True)
def run_tests(ctx):
    dt_now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    results_dir = 'res_{}'.format(dt_now)

    ctx.run("""
        pytest {tests_files} --api-url {api_url} \
        --loose-compare --tb=short --alluredir allure/{results_dir}
        """.format(
            tests_files=ctx.tests_files,
            api_url=ctx.api_url,
            results_dir=results_dir
        ),
        warn=True
    )

    generate_report(ctx, results_dir)
