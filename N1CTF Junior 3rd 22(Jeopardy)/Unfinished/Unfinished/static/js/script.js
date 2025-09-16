document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        flashMessages.forEach(function (flashElement) {
            const message = flashElement.dataset.message;

            if (message) {
                const alertBox = document.createElement('div');
                alertBox.className = 'alert';
                alertBox.textContent = message;
                document.body.appendChild(alertBox);

                setTimeout(() => {
                    alertBox.classList.add('show');
                }, 10);

                setTimeout(() => {
                    alertBox.classList.remove('show');
                    alertBox.addEventListener('transitionend', () => {
                        if (alertBox.parentNode) {
                            alertBox.parentNode.removeChild(alertBox);
                        }
                    });
                }, 3000);
            }
        });
    }
});
