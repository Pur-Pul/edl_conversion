from invoke import task

@task
def start(ctx):
    with ctx.cd("src"):
        ctx.run("python main.py")

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def test(ctx):
    ctx.run("pytest src")

@task
def coverage_report(ctx):
    ctx.run("coverage run --branch -m pytest src")
    ctx.run("coverage html")