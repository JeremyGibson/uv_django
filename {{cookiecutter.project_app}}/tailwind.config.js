// tailwind.config.js
module.exports = {
    content: [
        './apps/**/*.html',
        './apps/**/*.js',
        './{{ cookiecutter.project_app }}/templates/**/*.html',
        './{{ cookiecutter.project_app }}/**/*.html'
    ],
}