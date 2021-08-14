const getRandomLower = () => {
    return String.fromCharCode(Math.floor(Math.random()*26)+97)
}

const getRandomUpper = () => {
    return String.fromCharCode(Math.floor(Math.random()*26)+65)
}

const getRandomNumber = () => {
    return String.fromCharCode(Math.floor(Math.random()*10)+48)
}

const getRandomSymbol = () => {
    const symbols = '!@#+$%&/?*'
    return symbols[Math.floor(Math.random() *symbols.length)]
}

const randomFunctions = {getRandomLower,getRandomUpper,getRandomNumber,getRandomSymbol}
const generatePassword = () => {
    const lenght = 16
    let generatedPassword = ''
    for(let x = 0; x < lenght; x++)
     generatedPassword += Object.values(randomFunctions)[Math.floor(Math.random() * 4)]()
    return generatedPassword
}

const spanResult = document.getElementById('result')
const generateButton = document.getElementById('generate')
const clipboardButton = document.getElementById('clipboard')
generateButton.addEventListener('click',() => {
    spanResult.innerText = generatePassword()
})

clipboard.addEventListener('click',() => {
    const password = spanResult.innerText
    if(!password)
     return
    const textarea = document.createElement('textarea')
    textarea.value = password
    document.body.appendChild(textarea)
    textarea.select()
    document.execCommand('copy')
    textarea.remove()
    console.log("Parola Kopyalandı.")
})