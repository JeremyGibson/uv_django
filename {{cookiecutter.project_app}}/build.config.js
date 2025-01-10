import * as esbuild from 'esbuild'

if (process.env.DEPLOY === 'DEPLOY') {
    esbuild.build({
        logLevel: "info",
        entryPoints: ["cruso_software/assets/js/src.js"],
        bundle: true,
        outfile: "cruso_software/static/js/main.js",
    }).catch(() => process.exit(1));
} else {
    let ctx = await esbuild.context({
        logLevel: "info",
        entryPoints: ["cruso_software/assets/js/src.js"],
        bundle: true,
        outfile: "cruso_software/static/js/main.js",
    })

    await ctx.watch()
}