document.getElementById('next-aya-btn').addEventListener('click', function() {
    this.classList.add('move');
    setTimeout(() => {
        this.classList.remove('move');
    }, 1000);

    // تغییر متن دکمه بعد از اولین کلیک
    if (this.textContent === 'شروع تلاوت') {
        this.textContent = 'آیه بعدی';
    }

    fetch('/next_aya')
        .then(response => response.json())
        .then(data => {
            const ayaElement = document.getElementById('aya');
            ayaElement.textContent = data.aya;
            ayaElement.classList.remove('welcome-message'); // Remove the welcome message class
            ayaElement.style.fontFamily = 'hafs'; // Change the font to hafs

            document.getElementById('sura').textContent = 'سوره: ' + data.sura;
            document.getElementById('aya-num').textContent = 'آیه: ' + data.aya_num;
            document.getElementById('khatm-number').textContent = 'ختم شماره: ' + data.khatm_number;
        })
        .catch(error => console.error('Error:', error));
});
