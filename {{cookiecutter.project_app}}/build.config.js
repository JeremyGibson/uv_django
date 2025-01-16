import * as esbuild from 'esbuild'

if (process.env.DEPLOY === 'DEPLOY') {
    console.log('Building Deployment...')
    await esbuild.build({
        logLevel: "info",
        entryPoints: ["{{ cookiecutter.project_app }}/assets/js/src.js"],
        bundle: true,
        outfile: "{{ cookiecutter.project_app }}/static/js/main.js",
    })
} else {
    let ctx = await esbuild.context({
        logLevel: "info",
        entryPoints: ["{{ cookiecutter.project_app }}/assets/js/src.js"],
        bundle: true,
        outfile: "{{ cookiecutter.project_app }}/static/js/main.js",
    })
    await ctx.watch()
}