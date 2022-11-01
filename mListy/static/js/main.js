const theme = localStorage.getItem('theme')

if (theme) {
    setTheme(theme)
    btnText.textContent = returnBtnText(theme)
} else {
    setTheme('dark-theme')
    btnText.textContent = 'Light'
}

function returnBtnText(themeName) {
    return themeName === 'dark-theme' ? 'Light' : 'Dark'

}

function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
}

function toggleTheme() {
    if (localStorage.getItem('theme') === 'dark-theme') {
        setTheme('light-theme');
        btnText.textContent = 'Dark'
    } else {
        setTheme('dark-theme');
        btnText.textContent = 'Light'
    }
}