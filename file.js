async function getToken() {
    const response = await fetch("https://notify.eskiz.uz/api/message/sms/send", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjAyMTg2ODQsImlhdCI6MTcxNzYyNjY4NCwicm9sZSI6InVzZXIiLCJzaWduIjoiOTljMzk0ZTViNDg2YzQyYjNiZWE2M2QwZGU2MmFiOTVmYWVlZmU5YTNlZTRhMDI0ZjZlYjc3MzBmZDJlNGFjNCIsInN1YiI6IjY0NzEifQ.WYWm52Z-ZxjHP6bgSf5EXrY7NgwMs2VuLv3xDMojBr4'
        },
        body: JSON.stringify({
            'mobile_phone': '+998996937308',
            'message': "Al-Xorazmiy o'quv markazi. Yangi guruh tashkillandi. +998 91 396 44 00",
            'from': '4546',
            'callback_url': ''
        })
    })
    const data = await response.json()
    console.log(data)
}

getToken()
