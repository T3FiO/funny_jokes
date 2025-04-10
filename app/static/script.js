document.getElementById('generate-button').addEventListener('click', async () => {
    const text = document.getElementById('prompt-input').value.trim();
    const resultContainer = document.getElementById('result-container');

    resultContainer.innerHTML = '';

    if (!text) {
        resultContainer.style.display = 'block';
        resultContainer.innerHTML = `<p class="error">Пожалуйста, введите текст</p>`;
        return;
    }

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text
            })
        })

        if (!response.ok) {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }

        const data = await response.json();

        const img = document.createElement('img');
        img.src = data.img_url;
        img.alt = data.text;

        const caption = document.createElement('p');
        caption.textContent = data.text;

        resultContainer.appendChild(img);
        resultContainer.appendChild(caption);

        const loadingText = document.createElement('p');
        loadingText.textContent = 'Загрузка изображения...';
        resultContainer.insertBefore(loadingText, img);
        img.onload = () => {
            loadingText.remove();
        };
        img.onerror = () => {
            loadingText.textContent = 'Не удалось загрузить изображение.';
        }


    } catch (error) {
        resultContainer.style.display = 'block';
        resultContainer.innerHTML = `<p class="error">Ошибка: ${error.message}</p>`;
        console.error('Ошибка при создании изображения:', error);
    }
});