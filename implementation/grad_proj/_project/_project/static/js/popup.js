const clickBTN = document.querySelectorAll('#clickBTN');
        const closePopup = document.querySelectorAll('#closePopup');
        const popup = document.getElementById('popup');
        const window_content = document.getElementById('window_content');
        clickBTN.forEach((btn) => {
            btn.addEventListener('click', (e) => {
                popup.style.display='flex';
                const metadata = btn.getAttribute('metadata')
                window_content.innerHTML = metadata;
            })
        })
        closePopup.forEach((btn) => {
            btn.addEventListener('click', (e) => {
                popup.style.display='none';
            })
        })