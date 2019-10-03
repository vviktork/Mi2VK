setInterval(function () {
    date = new Date(),
    month_num = date.getMonth()
    day = date.getDate()
    h = date.getHours(),
    m = date.getMinutes(),
    s = date.getSeconds(),
    h = (h < 10) ? '0' + h : h,
    m = (m < 10) ? '0' + m : m,
    s = (s < 10) ? '0' + s : s,
    month=new Array("января", "февраля", "марта", "апреля", "мая", "июня",
     "июля", "августа", "сентября", "октября", "ноября", "декабря");
    document.getElementById('time').innerHTML = day + " " + month[month_num] + " " + date.getFullYear()+ "г." +
    " " + h + ':' + m + ':' + s;
    }, 1000);